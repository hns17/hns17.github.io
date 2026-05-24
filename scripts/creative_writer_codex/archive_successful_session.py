#!/usr/bin/env python3
"""Archive the Codex session for a successfully published Creative Writer run."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / ".codex-creative-writer"
CURRENT_RUN_PATH = STATE_DIR / "current_run.json"
CODEX_HOME = Path.home() / ".codex"
SESSIONS_DIR = CODEX_HOME / "sessions"
ARCHIVED_DIR = CODEX_HOME / "archived_sessions"
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def session_id_from_image_path(image_path: str) -> str:
    path = Path(image_path)
    for part in reversed(path.parts):
        if UUID_RE.match(part):
            return part
    raise RuntimeError(f"could not find session id in image path: {image_path}")


def find_session_file(session_id: str) -> Path | None:
    matches = sorted(SESSIONS_DIR.rglob(f"*{session_id}.jsonl"))
    return matches[-1] if matches else None


def main() -> None:
    run = read_json(CURRENT_RUN_PATH)
    result = read_json(Path(run["run_dir"]) / "publish_result.json")

    if not result.get("ok"):
        raise RuntimeError("publish_result.json is not ok; refusing to archive session")
    if not result.get("discord", {}).get("ok"):
        raise RuntimeError("discord publish did not succeed; refusing to archive session")

    session_id = session_id_from_image_path(str(result["image_path"]))
    source = find_session_file(session_id)
    if source is None:
        print(json.dumps({"ok": True, "skipped": True, "reason": "session_not_found", "session_id": session_id}))
        return

    ARCHIVED_DIR.mkdir(parents=True, exist_ok=True)
    target = ARCHIVED_DIR / source.name
    if target.exists():
        source.unlink()
        print(json.dumps({"ok": True, "skipped": True, "reason": "already_archived", "session_id": session_id}))
        return

    shutil.move(str(source), str(target))
    print(json.dumps({"ok": True, "session_id": session_id, "archived_path": str(target)}))


if __name__ == "__main__":
    main()
