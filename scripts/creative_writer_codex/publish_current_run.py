#!/usr/bin/env python3
"""Publish the current Codex Creative Writer run."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / ".codex-creative-writer"
CURRENT_RUN_PATH = STATE_DIR / "current_run.json"
WRITING_BASE = ROOT / "_clobie_idea" / "_clobie_writing"
IMAGE_ROOT = Path.home() / ".codex" / "generated_images"
IMAGE_REPO = "cubixkernel/clobie-image-container"
DEFAULT_KEYCHAIN_SERVICE = "creative-writer-discord-webhook-url"
LOCAL_WEBHOOK_PATH = STATE_DIR / "webhook_url"
SEOUL = ZoneInfo("Asia/Seoul")
NETWORK_HINT = (
    "publish_current_run.py needs outbound GitHub, git push, and Discord webhook access. "
    "In Codex, approve this command persistently for unattended publishing."
)


class PublishError(RuntimeError):
    def __init__(self, step: str, message: str, *, stdout: str = "", stderr: str = "") -> None:
        super().__init__(message)
        self.step = step
        self.stdout = stdout
        self.stderr = stderr


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_result(run: dict, payload: dict, filename: str) -> Path:
    result_path = Path(run["run_dir"]) / filename
    result_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result_path


def run_cmd(args: list[str], *, step: str) -> subprocess.CompletedProcess:
    proc = subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True)
    if proc.returncode != 0:
        raise PublishError(
            step,
            f"command failed ({proc.returncode}): {' '.join(args)}",
            stdout=proc.stdout,
            stderr=proc.stderr,
        )
    return proc


def classify_gh_failure(stderr: str) -> str:
    lower = stderr.lower()
    if "could not resolve host" in lower or "temporary failure in name resolution" in lower:
        return "dns resolution for github failed"
    if "error connecting to api.github.com" in lower:
        return "network connection to api.github.com failed"
    if "authentication failed" in lower or "http 401" in lower or "http 403" in lower:
        return "github authentication or permission failure"
    return "github api request failed"


def preflight_github() -> None:
    if not shutil.which("gh"):
        raise PublishError("github_preflight", "GitHub CLI is not installed or is not on PATH")
    try:
        run_cmd(["gh", "api", "rate_limit"], step="github_preflight")
    except PublishError as exc:
        reason = classify_gh_failure(exc.stderr)
        raise PublishError(
            "github_preflight",
            f"{reason}. {NETWORK_HINT}",
            stdout=exc.stdout,
            stderr=exc.stderr,
        ) from exc


def image_record(path: Path) -> dict:
    stat = path.stat()
    return {"path": str(path), "mtime": stat.st_mtime, "size": stat.st_size}


def find_generated_image(marker_path: Path) -> tuple[Path, dict]:
    if not marker_path.exists():
        raise FileNotFoundError(f"marker not found: {marker_path}")
    marker_ts = marker_path.stat().st_mtime
    candidates: list[Path] = []
    for path in IMAGE_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        try:
            if path.stat().st_mtime >= marker_ts - 2:
                candidates.append(path)
        except FileNotFoundError:
            continue
    if not candidates:
        raise FileNotFoundError(f"no generated image found under {IMAGE_ROOT} after {marker_path}")
    candidates.sort(key=lambda item: item.stat().st_mtime)
    selected = candidates[-1]
    return selected, {
        "strategy": "marker_mtime_latest",
        "marker_path": str(marker_path),
        "candidate_count": len(candidates),
        "selected": image_record(selected),
        "candidates_tail": [image_record(path) for path in candidates[-5:]],
    }


def resolve_image_path(args: argparse.Namespace, run: dict) -> tuple[Path, dict]:
    if args.image_path:
        image_path = Path(args.image_path).expanduser()
        if not image_path.exists():
            raise FileNotFoundError(f"explicit image path does not exist: {image_path}")
        return image_path, {"strategy": "explicit_image_path", "selected": image_record(image_path)}
    return find_generated_image(Path(run["marker_path"]))


def ensure_png(image_path: Path) -> bytes:
    data = image_path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return data

    sips = shutil.which("sips")
    if not sips:
        raise RuntimeError(f"image is not PNG and sips is unavailable: {image_path}")

    with tempfile.TemporaryDirectory(prefix="codex-writer-img-") as tmp:
        src = Path(tmp) / f"src{image_path.suffix or '.bin'}"
        out = Path(tmp) / "out.png"
        src.write_bytes(data)
        run_cmd([sips, "-s", "format", "png", str(src), "--out", str(out)], step="image_convert")
        return out.read_bytes()


def safe_slug(value: str) -> str:
    lowered = value.strip().lower()
    slug = "".join(ch if ch.isalnum() else "-" for ch in lowered)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug[:80].strip("-") or "clobie-writing"


def yaml_string(value: str) -> str:
    return json.dumps(value or "", ensure_ascii=False)


def validate_draft(run: dict, draft: dict) -> dict:
    required = run.get("draft_contract", {}).get("required_fields") or []
    missing = [field for field in required if field not in draft or draft[field] in ("", None, [])]
    if missing:
        raise PublishError("draft_validation", f"draft is missing required field(s): {', '.join(missing)}")
    if draft.get("clobie_type") != run.get("target_type"):
        raise PublishError(
            "draft_validation",
            f"draft clobie_type {draft.get('clobie_type')!r} does not match run target {run.get('target_type')!r}",
        )
    if not isinstance(draft.get("tags"), list) or not all(isinstance(tag, str) for tag in draft["tags"]):
        raise PublishError("draft_validation", "draft tags must be a list of strings")
    draft["slug"] = safe_slug(str(draft.get("slug") or draft["title"]))
    draft["body_markdown"] = strip_publisher_fields(str(draft["body_markdown"]), str(draft["title"]), str(draft["genre"]))
    return draft


def strip_publisher_fields(body: str, title: str, genre: str) -> str:
    body = re.sub(r"^---.*?---\s*", "", body.strip(), flags=re.DOTALL)
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].strip() == f"# {title}":
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].strip() in {f"장르: {genre}", genre}:
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    return "\n".join(lines).strip()


def github_upload(png_data: bytes, run: dict, draft: dict, now: datetime) -> str:
    prompt = draft["illustration_prompt"]
    prompt_hash = hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:10]
    image_hash = hashlib.sha1(png_data).hexdigest()[:10]
    out_path = (
        f"generated/writing/{now:%Y}/{now:%m}/{now:%d}/"
        f"{draft['slug']}-{prompt_hash}-{image_hash}.png"
    )
    payload_obj = {
        "message": f"Upload Codex generated writing art {now:%Y-%m-%d}",
        "content": base64.b64encode(png_data).decode("ascii"),
    }

    existing = subprocess.run(
        ["gh", "api", f"repos/{IMAGE_REPO}/contents/{out_path}"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    if existing.returncode == 0:
        try:
            payload_obj["sha"] = json.loads(existing.stdout).get("sha")
            payload_obj["message"] = f"Update Codex generated writing art {now:%Y-%m-%d}"
        except Exception:
            pass

    payload = json.dumps(payload_obj)
    proc = subprocess.run(
        ["gh", "api", f"repos/{IMAGE_REPO}/contents/{out_path}", "--method", "PUT", "--input", "-"],
        cwd=str(ROOT),
        input=payload,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        reason = classify_gh_failure(proc.stderr)
        raise PublishError(
            "github_upload",
            f"{reason}: repos/{IMAGE_REPO}/contents/{out_path}. {NETWORK_HINT}",
            stdout=proc.stdout,
            stderr=proc.stderr,
        )

    parsed = json.loads(proc.stdout)
    download_url = parsed.get("content", {}).get("download_url")
    if not download_url:
        raise PublishError("github_upload", "GitHub upload did not return download_url", stdout=proc.stdout)
    return download_url


def build_markdown(run: dict, draft: dict, image_url: str, now: datetime) -> str:
    tags = [tag for tag in draft["tags"] if tag.strip()][:8]
    tag_lines = "\n".join(f"  - {yaml_string(tag)}" for tag in tags)
    selected_art = run.get("selected_art_skill", {})
    front_matter = "\n".join(
        [
            "---",
            f"title: {yaml_string(draft['title'])}",
            f"date: {now:%Y-%m-%d %H:%M:%S +0900}",
            f"clobie_type: {yaml_string(draft['clobie_type'])}",
            f"genre: {yaml_string(draft['genre'])}",
            f"summary: {yaml_string(draft['summary'])}",
            "tags:",
            tag_lines,
            f"image_url: {yaml_string(image_url)}",
            f"image_alt: {yaml_string(draft['image_alt'])}",
            f"illustration_prompt: {yaml_string(draft['illustration_prompt'])}",
            f"source_writer_skill: {yaml_string(run.get('writer_skill', ''))}",
            f"source_art_skill: {yaml_string(selected_art.get('name', ''))}",
            "---",
            "",
        ]
    )
    body = "\n".join(
        [
            f"# {draft['title']}",
            "",
            f"장르: {draft['genre']}",
            "",
            f"![{draft['image_alt']}]({image_url})",
            "",
            draft["body_markdown"].strip(),
            "",
        ]
    )
    text = front_matter + body
    if yaml is not None:
        raw_fm = text.split("---", 2)[1]
        yaml.safe_load(raw_fm)
    return text


def unique_markdown_path(draft: dict, now: datetime) -> Path:
    date_dir = WRITING_BASE / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    base = draft["slug"]
    path = date_dir / f"{base}.md"
    if not path.exists():
        return path
    for index in range(2, 100):
        candidate = date_dir / f"{base}-{index}.md"
        if not candidate.exists():
            return candidate
    raise PublishError("write_markdown", f"could not find available filename for slug: {base}")


def write_markdown(run: dict, draft: dict, image_url: str, now: datetime) -> Path:
    path = unique_markdown_path(draft, now)
    path.write_text(build_markdown(run, draft, image_url, now), encoding="utf-8")
    return path


def commit_only(markdown_path: Path, title: str) -> bool:
    relative_path = markdown_path.relative_to(ROOT)
    run_cmd(["git", "add", str(relative_path)], step="git_add")
    diff = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--", str(relative_path)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    if diff.returncode == 0:
        return False
    if diff.returncode not in {0, 1}:
        raise PublishError("git_diff", "failed to inspect staged markdown diff", stdout=diff.stdout, stderr=diff.stderr)
    run_cmd(["git", "commit", "-m", f"Add Clobie writing: {title}", "--", str(relative_path)], step="git_commit")
    try:
        run_cmd(["git", "push", "origin", "main"], step="git_push")
    except PublishError as exc:
        raise PublishError(
            "git_push",
            f"git push failed. {NETWORK_HINT}",
            stdout=exc.stdout,
            stderr=exc.stderr,
        ) from exc
    return True


def page_url(markdown_path: Path) -> str:
    rel = markdown_path.relative_to(WRITING_BASE).with_suffix("")
    return "https://hns17.github.io/clobie/writing/" + "/".join(rel.parts) + "/"


def discord_content(draft: dict, markdown_path: Path, image_url: str) -> str:
    parts = [
        f"**{draft['title']}**",
        f"{draft['genre']}",
        "",
        draft["summary"],
        "",
        page_url(markdown_path),
        image_url,
    ]
    content = "\n".join(parts).strip()
    if len(content) <= 1900:
        return content
    return content[:1880].rstrip() + "\n..."


def post_discord(webhook_url: str, draft: dict, image_url: str, markdown_path: Path) -> dict:
    payload = {
        "content": discord_content(draft, markdown_path, image_url),
        "embeds": [{"title": draft["title"], "image": {"url": image_url}}],
        "allowed_mentions": {"parse": []},
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url + "?wait=true",
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "CodexCreativeWriter/1.0 (+https://github.com/hns17/hns17.github.io)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = res.read().decode("utf-8", errors="replace")
        return {"ok": 200 <= res.status < 300, "status": res.status, "body": body}


def keychain_webhook(service: str) -> str:
    if not service:
        return ""
    proc = subprocess.run(
        ["security", "find-generic-password", "-w", "-s", service],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def local_webhook() -> str:
    if not LOCAL_WEBHOOK_PATH.exists():
        return ""
    return LOCAL_WEBHOOK_PATH.read_text(encoding="utf-8").strip()


def already_published(run: dict) -> dict | None:
    result_path = Path(run["run_dir"]) / "publish_result.json"
    if not result_path.exists():
        return None
    result = read_json(result_path)
    if result.get("ok") and result.get("discord", {}).get("ok"):
        return result
    return None


def publish(args: argparse.Namespace) -> dict:
    run = read_json(Path(args.run_json))
    if not args.force:
        existing = already_published(run)
        if existing:
            existing["skipped"] = True
            existing["reason"] = "already published"
            return existing

    draft = validate_draft(run, read_json(Path(args.draft_json or run["draft_path"])))
    if args.dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "run_id": run["run_id"],
            "title": draft["title"],
            "slug": draft["slug"],
            "clobie_type": draft["clobie_type"],
            "selected_art_skill": run.get("selected_art_skill", {}),
        }

    if not args.webhook_url:
        args.webhook_url = keychain_webhook(args.keychain_service) or local_webhook()
    if not args.skip_discord and not args.webhook_url:
        raise PublishError(
            "input_validation",
            "missing Discord webhook URL; pass --webhook-url, set CREATIVE_WRITER_DISCORD_WEBHOOK_URL, "
            f"store it in macOS Keychain service {args.keychain_service!r}, "
            f"or write it to {LOCAL_WEBHOOK_PATH}",
        )
    if not args.skip_github_preflight:
        preflight_github()

    image_path, image_selection = resolve_image_path(args, run)
    write_result(run, image_selection, "image_selection.json")
    now = datetime.now(SEOUL)
    image_url = github_upload(ensure_png(image_path), run, draft, now)
    markdown_path = write_markdown(run, draft, image_url, now)
    committed = False if args.skip_git else commit_only(markdown_path, draft["title"])
    discord = {"ok": False, "skipped": True}
    if not args.skip_discord:
        discord = post_discord(args.webhook_url, draft, image_url, markdown_path)

    result = {
        "ok": True,
        "run_id": run["run_id"],
        "image_path": str(image_path),
        "image_url": image_url,
        "markdown_path": str(markdown_path),
        "page_url": page_url(markdown_path),
        "committed": committed,
        "discord": discord,
    }
    write_result(run, result, "publish_result.json")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-json", default=str(CURRENT_RUN_PATH))
    parser.add_argument("--draft-json")
    parser.add_argument("--image-path")
    parser.add_argument("--webhook-url", default=os.environ.get("CREATIVE_WRITER_DISCORD_WEBHOOK_URL", ""))
    parser.add_argument("--keychain-service", default=DEFAULT_KEYCHAIN_SERVICE)
    parser.add_argument("--skip-discord", action="store_true")
    parser.add_argument("--skip-git", action="store_true")
    parser.add_argument("--skip-github-preflight", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    print(json.dumps(publish(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        step = "publish"
        stdout = ""
        stderr = ""
        if isinstance(exc, PublishError):
            step = exc.step
            stdout = exc.stdout
            stderr = exc.stderr
        failure = {"ok": False, "step": step, "error": str(exc), "stdout": stdout, "stderr": stderr}
        try:
            run = read_json(CURRENT_RUN_PATH)
            write_result(run, failure, "publish_error.json")
        except Exception:
            pass
        print(f"publish failed at step={step}: {exc}", file=sys.stderr)
        if stdout:
            print(f"stdout:\n{stdout}", file=sys.stderr)
        if stderr:
            print(f"stderr:\n{stderr}", file=sys.stderr)
        sys.exit(1)
