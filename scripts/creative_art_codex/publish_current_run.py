#!/usr/bin/env python3
"""Publish the current Codex Creative Art run with one approval-friendly command."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from finalize_run import (
    CURRENT_RUN_PATH,
    FinalizeError,
    ROOT,
    ensure_png,
    github_upload,
    post_discord,
    preflight_github,
    read_json,
    resolve_image_path,
    write_markdown,
    write_result,
)

NETWORK_HINT = (
    "publish_current_run.py needs one approval that allows outbound GitHub, "
    "git push, and Discord webhook access. In Codex, approve this command "
    "persistently for unattended publishing."
)
DEFAULT_KEYCHAIN_SERVICE = "creative-art-discord-webhook-url"


def run_cmd(args: list[str], *, step: str) -> subprocess.CompletedProcess:
    proc = subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True)
    if proc.returncode != 0:
        raise FinalizeError(
            step,
            f"command failed ({proc.returncode}): {' '.join(args)}",
            stdout=proc.stdout,
            stderr=proc.stderr,
        )
    return proc


def run_time(run: dict) -> datetime:
    raw = run.get("created_at")
    if raw:
        try:
            return datetime.fromisoformat(raw).astimezone(ZoneInfo("Asia/Seoul"))
        except ValueError:
            pass
    return datetime.now(ZoneInfo("Asia/Seoul"))


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
        raise FinalizeError(
            "git_diff",
            "failed to inspect staged markdown diff",
            stdout=diff.stdout,
            stderr=diff.stderr,
        )

    run_cmd(
        ["git", "commit", "-m", f"Add Codex Clobie art: {title}", "--", str(relative_path)],
        step="git_commit",
    )
    try:
        run_cmd(["git", "push", "origin", "main"], step="git_push")
    except FinalizeError as exc:
        raise FinalizeError(
            "git_push",
            f"git push failed. {NETWORK_HINT}",
            stdout=exc.stdout,
            stderr=exc.stderr,
        ) from exc
    return True


def already_published(run: dict) -> dict | None:
    result_path = Path(run["run_dir"]) / "publish_result.json"
    if not result_path.exists():
        return None
    result = read_json(result_path)
    if result.get("ok") and result.get("discord", {}).get("ok"):
        return result
    return None


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


def publish(args: argparse.Namespace) -> dict:
    run = read_json(Path(args.run_json))
    if not args.force:
        existing = already_published(run)
        if existing:
            existing["skipped"] = True
            existing["reason"] = "already published"
            return existing

    if not args.webhook_url:
        args.webhook_url = keychain_webhook(args.keychain_service)

    if not args.skip_discord and not args.webhook_url:
        raise FinalizeError(
            "input_validation",
            "missing Discord webhook URL; pass --webhook-url, set CREATIVE_ART_DISCORD_WEBHOOK_URL, "
            f"or store it in macOS Keychain service {args.keychain_service!r}",
        )

    if not args.skip_github_preflight:
        preflight_github()

    image_path, image_selection = resolve_image_path(args, run)
    write_result(run, image_selection, "image_selection.json")

    if args.dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "run_id": run["run_id"],
            "image_path": str(image_path),
            "title": run["title"],
            "slug": run["slug"],
        }

    now = run_time(run)
    png_data = ensure_png(image_path)
    image_url = github_upload(png_data, run, now)
    markdown_path = write_markdown(run, image_url, now)
    committed = False if args.skip_git else commit_only(markdown_path, run["title"])

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
    write_result(run, result, "publish_result.json")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-json", default=str(CURRENT_RUN_PATH))
    parser.add_argument("--image-path")
    parser.add_argument("--webhook-url", default=os.environ.get("CREATIVE_ART_DISCORD_WEBHOOK_URL", ""))
    parser.add_argument("--keychain-service", default=DEFAULT_KEYCHAIN_SERVICE)
    parser.add_argument("--skip-discord", action="store_true")
    parser.add_argument("--skip-git", action="store_true")
    parser.add_argument("--skip-github-preflight", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    result = publish(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        step = "publish"
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
