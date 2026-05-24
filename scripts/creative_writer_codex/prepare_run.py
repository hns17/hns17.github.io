#!/usr/bin/env python3
"""Prepare one Codex Creative Writer run.

The script keeps scheduler decisions deterministic and small:
- inspect current Clobie writing docs
- choose settings/stories by balance
- collect recent items to avoid repetition
- choose the writer skill and illustration skill
- write runtime JSON for the Codex automation prompt
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import yaml
except Exception:  # pragma: no cover - fallback is only for constrained envs.
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
WRITING_BASE = ROOT / "_clobie_idea" / "_clobie_writing"
STATE_DIR = ROOT / ".codex-creative-writer"
RUNS_DIR = STATE_DIR / "runs"
CURRENT_RUN_PATH = STATE_DIR / "current_run.json"
SEOUL = ZoneInfo("Asia/Seoul")

WRITER_SKILLS = {
    "settings": "clobie-setting-writer",
    "stories": "clobie-story-writer",
}

ART_SKILLS = [
    {
        "name": "draw-soft-anime",
        "source_model": "Codex draw-soft-anime",
        "description": "soft atmospheric anime illustration",
    },
    {
        "name": "draw-cinema-anime",
        "source_model": "Codex draw-cinema-anime",
        "description": "cinematic cel anime illustration",
    },
]

TONE_SEEDS = {
    "settings": [
        "한 사회가 편리함을 얻는 대신 개인의 이름을 조금씩 잃는 구조",
        "살아남기 위한 제도가 누군가의 우주를 침묵시키는 구조",
        "가장 아름다운 자원이 가장 잔인한 비용으로만 생성되는 세계",
        "공동체를 지키는 규칙이 개인의 선택권과 충돌하는 장소",
        "구원처럼 보이는 시스템이 기억, 몸, 관계 중 하나를 담보로 요구하는 설정",
    ],
    "stories": [
        "두 사람이 긴 겨울을 지나 하나의 문장으로 서로를 이해하게 되는 이야기",
        "다수를 위한 희생이라는 말 앞에서 한 사람의 우주를 지키는 이야기",
        "마지막 질문의 답이 지식이 아니라 사랑이나 거절의 형태로 돌아오는 이야기",
        "개화와 결빙의 이미지가 마지막 문장에서 뒤집히는 이야기",
        "작은 선택 하나가 거대한 우주적 결말을 조용히 바꾸는 이야기",
    ],
}

STORY_TASTE = [
    "서정적인 문장과 선명한 가치관이 함께 있어야 한다.",
    "반전은 정보 트릭보다 감정의 의미가 바뀌는 쪽을 우선한다.",
    "개인의 우주와 모두의 우주가 같은 무게를 가진다는 감각을 존중한다.",
    "시적인 문장은 장식이 아니라 인물의 결말에서 자연스럽게 도착해야 한다.",
    "아이작 아시모프의 '최후의 질문'처럼 큰 질문을 다룰 수 있지만 문체를 모방하지 않는다.",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def fallback_front_matter(raw_fm: str) -> dict:
    """Extract the fields the scheduler needs when old YAML is malformed."""
    data: dict[str, object] = {}
    lines = raw_fm.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            index += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        if key == "tags" and value == "":
            tags: list[str] = []
            index += 1
            while index < len(lines):
                tag_match = re.match(r"^\s*-\s*(.+?)\s*$", lines[index])
                if not tag_match:
                    break
                tags.append(tag_match.group(1).strip().strip("\"'"))
                index += 1
            data[key] = tags
            continue
        data[key] = value.strip().strip("\"'")
        index += 1
    return data


def parse_front_matter(path: Path) -> tuple[dict, str, str | None]:
    text = read_text(path)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not match:
        return {}, text, "missing_front_matter"
    raw_fm, body = match.group(1), match.group(2)
    if yaml is None:
        return {}, body, "pyyaml_unavailable"
    try:
        data = yaml.safe_load(raw_fm) or {}
    except Exception as exc:
        return fallback_front_matter(raw_fm), body, f"yaml_error: {exc}"
    if not isinstance(data, dict):
        return {}, body, "front_matter_not_mapping"
    return data, body, None


def compact_body(body: str, limit: int = 520) -> str:
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    return body[:limit]


def markdown_docs() -> list[dict]:
    docs: list[dict] = []
    for path in WRITING_BASE.rglob("*.md"):
        if not path.is_file():
            continue
        fm, body, error = parse_front_matter(path)
        stat = path.stat()
        raw_date = fm.get("date")
        sort_date = str(raw_date) if raw_date else ""
        docs.append(
            {
                "path": str(path.relative_to(ROOT)),
                "title": str(fm.get("title") or path.stem),
                "clobie_type": str(fm.get("clobie_type") or ""),
                "genre": str(fm.get("genre") or ""),
                "tags": fm.get("tags") if isinstance(fm.get("tags"), list) else [],
                "date": sort_date,
                "mtime": stat.st_mtime,
                "excerpt": compact_body(body),
                "parse_error": error,
            }
        )
    return docs


def choose_target_type(counts: dict[str, int]) -> str:
    settings = counts.get("settings", 0)
    stories = counts.get("stories", 0)
    if settings < stories:
        return "settings"
    if stories < settings:
        return "stories"
    return random.choice(["settings", "stories"])


def choose_art_skill(target_type: str) -> dict:
    if target_type == "stories":
        weights = [0.68, 0.32]
    else:
        weights = [0.45, 0.55]
    return random.choices(ART_SKILLS, weights=weights, k=1)[0]


def keyword_candidates(items: list[dict]) -> list[str]:
    values: list[str] = []
    for item in items:
        values.append(item.get("title", ""))
        values.append(item.get("genre", ""))
        values.extend(str(tag) for tag in item.get("tags", [])[:4])
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        cleaned = re.sub(r"\s+", " ", str(value)).strip()
        if cleaned and cleaned not in seen:
            out.append(cleaned)
            seen.add(cleaned)
    return out[:40]


def main() -> None:
    now = datetime.now(SEOUL)
    docs = markdown_docs()
    counts = {
        "settings": sum(1 for item in docs if item.get("clobie_type") == "settings"),
        "stories": sum(1 for item in docs if item.get("clobie_type") == "stories"),
    }
    target_type = choose_target_type(counts)
    selected_art_skill = choose_art_skill(target_type)

    recent_items = sorted(
        docs,
        key=lambda item: (item.get("date") or "", float(item.get("mtime") or 0)),
        reverse=True,
    )[:12]

    run_seed = f"{now.isoformat()}:{target_type}:{random.random()}"
    run_id = f"{now:%Y%m%d_%H%M%S}_{hashlib.sha1(run_seed.encode('utf-8')).hexdigest()[:8]}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    draft_path = run_dir / "draft.json"
    marker_path = run_dir / "image_marker.txt"
    marker_path.write_text(now.isoformat() + "\n", encoding="utf-8")

    run = {
        "ok": True,
        "run_id": run_id,
        "created_at": now.isoformat(),
        "root": str(ROOT),
        "writing_base": str(WRITING_BASE),
        "run_dir": str(run_dir),
        "draft_path": str(draft_path),
        "marker_path": str(marker_path),
        "target_type": target_type,
        "target_label": "설정" if target_type == "settings" else "이야기 조각",
        "writer_skill": WRITER_SKILLS[target_type],
        "selected_art_skill": selected_art_skill,
        "counts": counts,
        "recent_items": recent_items,
        "avoid_titles": [item.get("title", "") for item in recent_items],
        "avoid_devices": keyword_candidates(recent_items),
        "tone_seed": random.choice(TONE_SEEDS[target_type]),
        "story_taste": STORY_TASTE,
        "draft_contract": {
            "required_fields": [
                "title",
                "slug",
                "clobie_type",
                "genre",
                "summary",
                "tags",
                "body_markdown",
                "illustration_prompt",
                "image_alt",
            ],
            "clobie_type": target_type,
            "body_excludes": ["front matter", "top-level H1", "genre line", "image markdown"],
        },
    }

    payload = json.dumps(run, ensure_ascii=False, indent=2) + "\n"
    CURRENT_RUN_PATH.write_text(payload, encoding="utf-8")
    (run_dir / "run.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
