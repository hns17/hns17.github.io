#!/usr/bin/env python3
"""Publish one Codex Creative Art result.

This script can operate in two modes:

1. Legacy run mode: consume `.codex-creative-art/current_run.json` produced by
   `generate_prompt.py`.
2. Native Codex schedule mode: accept explicit metadata from a JSON file or CLI
   arguments, then publish the image and markdown post.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / ".codex-creative-art"
RUNS_DIR = STATE_DIR / "runs"
CURRENT_RUN_PATH = STATE_DIR / "current_run.json"
ART_BASE = ROOT / "_clobie_idea" / "_clobie_art"
IMAGE_REPO = "cubixkernel/clobie-image-container"
IMAGE_ROOT = Path.home() / ".codex" / "generated_images"
ACTIVE_RUN: dict | None = None
NETWORK_HINT = (
    "finalize_run.py needs outbound network access for GitHub upload, git push, "
    "and Discord delivery. In Codex, rerun this finalize step with network escalation; "
    "do not regenerate the image."
)


class FinalizeError(RuntimeError):
    def __init__(self, step: str, message: str, *, stderr: str = "", stdout: str = "") -> None:
        super().__init__(message)
        self.step = step
        self.stderr = stderr
        self.stdout = stdout


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_slug(value: str) -> str:
    lowered = value.strip().lower()
    slug = "".join(ch if ch.isalnum() else "-" for ch in lowered)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug or "codex-art"


def run_cmd(
    args: list[str],
    cwd: Path | None = None,
    input_text: str | None = None,
    *,
    step: str = "command",
) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        input=input_text,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise FinalizeError(
            step,
            f"command failed ({proc.returncode}): {' '.join(args)}",
            stdout=proc.stdout,
            stderr=proc.stderr,
        )
    return proc


def classify_gh_failure(stderr: str) -> str:
    lower = stderr.lower()
    if "error connecting to api.github.com" in lower:
        return "network connection to api.github.com failed"
    if "could not resolve host" in lower or "temporary failure in name resolution" in lower:
        return "dns resolution for github failed"
    if "authentication failed" in lower or "http 401" in lower or "http 403" in lower:
        return "github authentication or permission failure"
    return "github api request failed"


def preflight_github() -> None:
    if not shutil.which("gh"):
        raise FinalizeError(
            "github_preflight",
            "GitHub CLI is not installed or is not on PATH",
        )
    try:
        run_cmd(["gh", "api", "rate_limit"], step="github_preflight")
    except FinalizeError as exc:
        reason = classify_gh_failure(exc.stderr)
        raise FinalizeError(
            "github_preflight",
            f"{reason}. {NETWORK_HINT}",
            stdout=exc.stdout,
            stderr=exc.stderr,
        ) from exc


def write_result(run: dict, payload: dict, filename: str) -> Path:
    result_path = Path(run["run_dir"]) / filename
    result_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result_path


def image_record(path: Path) -> dict:
    stat = path.stat()
    return {
        "path": str(path),
        "mtime": stat.st_mtime,
        "size": stat.st_size,
    }


def find_generated_image(marker_path: Path) -> tuple[Path, dict]:
    if not marker_path.exists():
        raise FileNotFoundError(f"marker not found: {marker_path}")
    marker_ts = marker_path.stat().st_mtime
    candidates: list[Path] = []
    for path in IMAGE_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        try:
            if path.stat().st_mtime >= marker_ts - 2:
                candidates.append(path)
        except FileNotFoundError:
            continue
    if not candidates:
        raise FileNotFoundError(f"no generated image found under {IMAGE_ROOT} after {marker_path}")
    candidates.sort(key=lambda p: p.stat().st_mtime)
    selected = candidates[-1]
    return selected, {
        "strategy": "marker_mtime_latest",
        "marker_path": str(marker_path),
        "marker_mtime": marker_ts,
        "candidate_count": len(candidates),
        "selected": image_record(selected),
        "candidates_tail": [image_record(path) for path in candidates[-5:]],
    }


def find_latest_generated_image() -> tuple[Path, dict]:
    candidates: list[Path] = []
    for path in IMAGE_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        candidates.append(path)
    if not candidates:
        raise FileNotFoundError(f"no generated image found under {IMAGE_ROOT}")
    candidates.sort(key=lambda p: p.stat().st_mtime)
    selected = candidates[-1]
    return selected, {
        "strategy": "global_latest",
        "candidate_count": len(candidates),
        "selected": image_record(selected),
        "candidates_tail": [image_record(path) for path in candidates[-5:]],
    }


def resolve_image_path(args: argparse.Namespace, run: dict) -> tuple[Path, dict]:
    if args.image_path:
        image_path = Path(args.image_path).expanduser()
        if not image_path.exists():
            raise FileNotFoundError(f"explicit image path does not exist: {image_path}")
        return image_path, {
            "strategy": "explicit_image_path",
            "selected": image_record(image_path),
        }
    if run.get("marker_path"):
        return find_generated_image(Path(run["marker_path"]))
    return find_latest_generated_image()


def ensure_png(image_path: Path) -> bytes:
    data = image_path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return data

    sips = shutil.which("sips")
    if not sips:
        raise RuntimeError(f"image is not PNG and sips is unavailable: {image_path}")

    with tempfile.TemporaryDirectory(prefix="codex-art-img-") as tmp:
        src = Path(tmp) / f"src{image_path.suffix or '.bin'}"
        out = Path(tmp) / "out.png"
        src.write_bytes(data)
        run_cmd([sips, "-s", "format", "png", str(src), "--out", str(out)])
        return out.read_bytes()


def github_upload(png_data: bytes, run: dict, now: datetime) -> str:
    prompt_hash = hashlib.sha1(run["prompt"].encode("utf-8")).hexdigest()[:10]
    image_hash = hashlib.sha1(png_data).hexdigest()[:10]
    out_path = (
        f"generated/{now:%Y}/{now:%m}/{now:%d}/"
        f"{run['slug']}-{prompt_hash}-{image_hash}.png"
    )
    payload = json.dumps(
        {
            "message": f"Upload Codex generated art {now:%Y-%m-%d}",
            "content": base64.b64encode(png_data).decode("ascii"),
        }
    )

    existing_sha = None
    existing = subprocess.run(
        ["gh", "api", f"repos/{IMAGE_REPO}/contents/{out_path}"],
        text=True,
        capture_output=True,
    )
    if existing.returncode == 0:
        try:
            existing_sha = json.loads(existing.stdout).get("sha")
        except Exception:
            existing_sha = None
    if existing_sha:
        payload = json.dumps(
            {
                "message": f"Update Codex generated art {now:%Y-%m-%d}",
                "content": base64.b64encode(png_data).decode("ascii"),
                "sha": existing_sha,
            }
        )

    try:
        proc = run_cmd(
            ["gh", "api", f"repos/{IMAGE_REPO}/contents/{out_path}", "--method", "PUT", "--input", "-"],
            input_text=payload,
            step="github_upload",
        )
    except FinalizeError as exc:
        if exc.step == "github_upload":
            reason = classify_gh_failure(exc.stderr)
            raise FinalizeError(
                "github_upload",
                f"{reason}: repos/{IMAGE_REPO}/contents/{out_path}. {NETWORK_HINT}",
                stdout=exc.stdout,
                stderr=exc.stderr,
            ) from exc
        raise
    parsed = json.loads(proc.stdout)
    download_url = parsed.get("content", {}).get("download_url")
    if not download_url:
        raise RuntimeError("GitHub upload did not return download_url")
    return download_url


def build_manual_run(args: argparse.Namespace) -> dict:
    if args.metadata_json:
        data = read_json(Path(args.metadata_json))
    else:
        if not args.prompt:
            raise FinalizeError(
                "input_validation",
                "native schedule mode requires --prompt or --metadata-json",
            )
        data = {
            "title": args.title or "Codex Creative Art",
            "slug": args.slug,
            "prompt": args.prompt,
            "item": {
                "type": args.art_type or "art",
                "genre": args.genre or "",
                "mood": args.mood or "",
                "species": args.species or "",
                "scene_mode_label": args.scene_mode_label or "",
            },
            "selected_skill": {
                "name": args.source_tool or "codex-imagegen",
                "source_model": args.source_model or "Codex image generation",
            },
        }

    prompt = data.get("prompt")
    if not prompt:
        raise FinalizeError("input_validation", "metadata is missing required field: prompt")

    now = datetime.now(ZoneInfo("Asia/Seoul"))
    run_stamp = now.strftime("%Y%m%d_%H%M%S")
    run_id = f"{run_stamp}_{hashlib.sha1(prompt.encode('utf-8')).hexdigest()[:8]}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    title = data.get("title") or "Codex Creative Art"
    slug = data.get("slug") or safe_slug(f"{title}-{run_stamp}")
    item = data.get("item") or {}
    selected_skill = data.get("selected_skill") or {}
    run = {
        "ok": True,
        "run_id": run_id,
        "created_at": now.isoformat(),
        "root": str(ROOT),
        "run_dir": str(run_dir),
        "item": item,
        "prompt": prompt,
        "selected_skill": {
            "name": selected_skill.get("name", "codex-imagegen"),
            "source_model": selected_skill.get("source_model", "Codex image generation"),
        },
        "title": title,
        "slug": slug,
        "template": data.get("template", ""),
        "metadata_source": str(args.metadata_json) if args.metadata_json else "cli",
    }
    (run_dir / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return run


def load_run(args: argparse.Namespace) -> dict:
    if args.metadata_json or args.prompt:
        return build_manual_run(args)
    run_json = Path(args.run_json)
    if run_json.exists():
        return read_json(run_json)
    return build_manual_run(args)


def yaml_string(value: str) -> str:
    return json.dumps(value or "", ensure_ascii=False)


def tags_for(run: dict) -> list[str]:
    item = run["item"]
    labels = {
        "character": "캐릭터",
        "creature": "생물",
        "scene": "장면",
        "sf": "SF",
    }
    tags = [labels.get(item.get("type"), item.get("type", "art"))]
    for value in [
        item.get("genre"),
        item.get("species"),
        item.get("scene_mode_label"),
        run.get("selected_skill", {}).get("name"),
    ]:
        if value and value not in tags:
            tags.append(value)
    return tags


def body_for(run: dict) -> str:
    item = run["item"]
    genre = item.get("genre") or "창작 이미지"
    mood = item.get("mood") or "고요한 분위기"
    species = item.get("species")
    if item.get("type") == "character":
        return f"{genre}의 배경 위로 {species} 캐릭터의 실루엣과 표정을 담은 작품입니다.\n{mood}이 장면 전체에 은근하게 남습니다.\n"
    if item.get("type") == "creature":
        return f"{genre}의 분위기 속에서 {species}의 낯선 형태와 질감을 포착한 작품입니다.\n개체 중심의 구도와 {mood}이 조용한 여운을 만듭니다.\n"
    if item.get("type") == "sf":
        return f"{genre}의 공간 속에 {species}의 거대한 존재감을 배치한 SF 키 비주얼입니다.\n{mood}이 구조물의 규모감을 더 또렷하게 만듭니다.\n"
    return f"{genre}의 공간과 빛을 중심으로 구성한 장면 이미지입니다.\n{mood}이 배경의 깊이와 정서를 부드럽게 이어줍니다.\n"


def write_markdown(run: dict, image_url: str, now: datetime) -> Path:
    date_dir = ART_BASE / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    path = date_dir / f"{run['slug']}.md"
    item = run["item"]
    selected_skill = run.get("selected_skill", {})
    tags = tags_for(run)
    tag_lines = "\n".join(f"  - {yaml_string(tag)}" for tag in tags)
    front_matter = "\n".join(
        [
            "---",
            f"title: {yaml_string(run['title'])}",
            f"date: {now:%Y-%m-%d %H:%M:%S +0900}",
            f"clobie_type: {yaml_string(item.get('type', 'art'))}",
            f"genre: {yaml_string(item.get('genre', ''))}",
            f"mood: {yaml_string(item.get('mood', ''))}",
            "tags:",
            tag_lines,
            f"image_url: {yaml_string(image_url)}",
            f"prompt: {yaml_string(run['prompt'])}",
            f"source_tool: {yaml_string(selected_skill.get('name', 'codex-imagegen'))}",
            f"source_model: {yaml_string(selected_skill.get('source_model', 'Codex image generation'))}",
            'chatgpt_share_url: ""',
            "---",
            "",
            body_for(run).rstrip(),
            "",
        ]
    )
    path.write_text(front_matter, encoding="utf-8")
    return path


def maybe_commit(path: Path, title: str) -> bool:
    run_cmd(["git", "add", str(path)], cwd=ROOT)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(ROOT))
    if diff.returncode == 0:
        return False
    run_cmd(["git", "commit", "-m", f"Add Codex Clobie art: {title}"], cwd=ROOT)
    try:
        run_cmd(["git", "push"], cwd=ROOT, step="git_push")
    except FinalizeError as exc:
        raise FinalizeError(
            "git_push",
            f"git push failed. {NETWORK_HINT}",
            stdout=exc.stdout,
            stderr=exc.stderr,
        ) from exc
    return True


def post_discord(webhook_url: str, run: dict, image_url: str, markdown_path: Path) -> dict:
    if not webhook_url:
        return {"ok": False, "skipped": True, "reason": "missing webhook url"}
    content = "\n\n".join(
        [
            run["template"],
            f"프롬프트\n{run['prompt']}",
            f"링크\n이미지 링크: {image_url}",
        ]
    )
    payload = {
        "content": content,
        "embeds": [
            {
                "title": run["title"],
                "image": {"url": image_url},
            }
        ],
        "allowed_mentions": {"parse": []},
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url + "?wait=true",
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "CodexCreativeArt/1.0 (+https://github.com/hns17/hns17.github.io)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            body = res.read().decode("utf-8", errors="replace")
            return {"ok": 200 <= res.status < 300, "status": res.status, "body": body}
    except Exception as exc:
        error_payload = {
            "content": f"[IMAGE_CRON_DELIVERY_ERROR] 이미지 링크 전송 실패. 원인: {exc}",
            "allowed_mentions": {"parse": []},
        }
        error_data = json.dumps(error_payload, ensure_ascii=False).encode("utf-8")
        error_req = urllib.request.Request(
            webhook_url,
            data=error_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "CodexCreativeArt/1.0 (+https://github.com/hns17/hns17.github.io)",
            },
            method="POST",
        )
        try:
            urllib.request.urlopen(error_req, timeout=30).read()
        except Exception:
            pass
        raise


def main() -> None:
    global ACTIVE_RUN
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-json", default=str(CURRENT_RUN_PATH))
    parser.add_argument("--metadata-json")
    parser.add_argument("--image-path")
    parser.add_argument("--title")
    parser.add_argument("--slug")
    parser.add_argument("--prompt")
    parser.add_argument("--art-type")
    parser.add_argument("--genre")
    parser.add_argument("--mood")
    parser.add_argument("--species")
    parser.add_argument("--scene-mode-label")
    parser.add_argument("--source-tool")
    parser.add_argument("--source-model")
    parser.add_argument("--webhook-url", default=os.environ.get("CREATIVE_ART_DISCORD_WEBHOOK_URL", ""))
    parser.add_argument("--skip-discord", action="store_true")
    parser.add_argument("--skip-git", action="store_true")
    parser.add_argument("--skip-github-preflight", action="store_true")
    args = parser.parse_args()

    run = load_run(args)
    ACTIVE_RUN = run
    if not args.skip_github_preflight:
        preflight_github()
    image_path, image_selection = resolve_image_path(args, run)
    write_result(run, image_selection, "image_selection.json")
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    png_data = ensure_png(image_path)
    image_url = github_upload(png_data, run, now)
    markdown_path = write_markdown(run, image_url, now)
    committed = False if args.skip_git else maybe_commit(markdown_path, run["title"])
    discord = {"ok": False, "skipped": True}
    if not args.skip_discord:
        discord = post_discord(args.webhook_url, run, image_url, markdown_path)

    result = {
        "ok": True,
        "run_id": run["run_id"],
        "image_path": str(image_path),
        "image_url": image_url,
        "markdown_path": str(markdown_path),
        "committed": committed,
        "discord": discord,
    }
    write_result(run, result, "final_result.json")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        run = ACTIVE_RUN

        step = "finalize"
        stderr = ""
        stdout = ""
        if isinstance(exc, FinalizeError):
            step = exc.step
            stderr = exc.stderr
            stdout = exc.stdout

        failure = {
            "ok": False,
            "step": step,
            "error": str(exc),
            "stdout": stdout,
            "stderr": stderr,
        }
        if run:
            write_result(run, failure, "final_error.json")
        print(f"finalize failed at step={step}: {exc}", file=sys.stderr)
        if stdout:
            print(f"stdout:\n{stdout}", file=sys.stderr)
        if stderr:
            print(f"stderr:\n{stderr}", file=sys.stderr)
        sys.exit(1)
