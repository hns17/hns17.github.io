# Codex Automation Prompt Template

Use this shape for the hourly creative art schedule.

## Flow

1. Run `python3 scripts/creative_art_codex/generate_prompt.py`.
2. Read `.codex-creative-art/current_run.json`.
3. Use exactly its prepared `prompt` and randomly selected `selected_skill`.
4. Generate exactly one image:
   - use `draw-soft-anime` when `selected_skill.name` is `draw-soft-anime`
   - use `draw-cinema-anime` when `selected_skill.name` is `draw-cinema-anime`
5. Do not run `scripts/creative_art_codex/finalize_run.py`.
6. Publish with one explicit command:

```bash
python3 scripts/creative_art_codex/publish_current_run.py
```

Run that command with `sandbox_permissions="require_escalated"`, a justification
asking to allow outbound GitHub, git push, and Discord webhook access, and
`prefix_rule=["python3", "scripts/creative_art_codex/publish_current_run.py"]`.
When prompted, persistently approve that prefix so future hourly runs can publish
without stopping for separate GitHub, git, and Discord approvals. If publishing
fails, report the failing step and stderr, then rerun only the publish command
when appropriate. The publisher reads the Discord webhook from
`CREATIVE_ART_DISCORD_WEBHOOK_URL` or the macOS Keychain service
`creative-art-discord-webhook-url`. Do not regenerate the image for the same run.
After the publisher completes successfully, archive the successful Codex session
by running:

```bash
python3 scripts/creative_art_codex/archive_successful_session.py
```

Run that archive command with `sandbox_permissions="require_escalated"`, a
justification asking to allow moving the successful Codex session into
`~/.codex/archived_sessions`, and
`prefix_rule=["python3", "scripts/creative_art_codex/archive_successful_session.py"]`.
If the workflow ultimately fails, do not run the archive command; leave a concise
failure report with the failing step and stderr so it remains visible for
follow-up.

## Metadata Shape

```json
{
  "title": "작품 제목",
  "slug": "art-slug",
  "prompt": "이미지 생성에 실제로 사용한 장면 프롬프트",
  "item": {
    "type": "character",
    "genre": "도시 판타지",
    "mood": "잔잔한 긴장감",
    "species": "인간",
    "scene_mode_label": ""
  },
  "selected_skill": {
    "name": "draw-soft-anime",
    "source_model": "Codex draw-soft-anime"
  }
}
```

## Notes

- Do not use OpenClaw or browser automation.
- Do not use ChatGPT custom GPT URLs.
- Do not print the Discord webhook URL.
- Keep `.codex-creative-art/` uncommitted runtime state.
- Preserve unrelated user changes.
