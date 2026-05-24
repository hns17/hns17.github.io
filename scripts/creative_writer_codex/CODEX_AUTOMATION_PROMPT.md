# Codex Creative Writer Automation Prompt

Run the Codex Creative Writer workflow with one related illustration. Do not use OpenClaw or browser automation.

## Flow

1. Run:

```bash
python3 scripts/creative_writer_codex/prepare_run.py
```

2. Read `.codex-creative-writer/current_run.json`.
3. Use the selected writer skill for both writing and illustration generation:
   - use `$clobie-setting-writer` when `writer_skill` is `clobie-setting-writer`
   - use `$clobie-story-writer` when `writer_skill` is `clobie-story-writer`
4. The selected writer skill must write exactly one valid draft JSON object to the `draft_path` in the run JSON, then generate exactly one related illustration using the run's `selected_art_skill`.
5. Do not let the writer skill publish to Discord, write the final markdown article, commit, or push. The schedule handles those steps.
6. Publish/save/commit/deliver by running exactly one schedule command:

```bash
python3 scripts/creative_writer_codex/publish_current_run.py
```

Run the publisher with `sandbox_permissions="require_escalated"`, a justification asking to allow outbound GitHub upload, git push, and Discord webhook access, and `prefix_rule=["python3", "scripts/creative_writer_codex/publish_current_run.py"]`. If publishing fails, report the failing step and stderr, then rerun only the publisher when appropriate. Do not regenerate the writing or image for the same run after successful image generation.

The publisher reads the Discord webhook from `CREATIVE_WRITER_DISCORD_WEBHOOK_URL`, the macOS Keychain service `creative-writer-discord-webhook-url`, or the ignored local file `.codex-creative-writer/webhook_url`. Do not print webhook values.

After the publisher completes successfully, archive the successful Codex session:

```bash
python3 scripts/creative_writer_codex/archive_successful_session.py
```

Run the archive command with `sandbox_permissions="require_escalated"`, a justification asking to allow moving the successful Codex session into `~/.codex/archived_sessions`, and `prefix_rule=["python3", "scripts/creative_writer_codex/archive_successful_session.py"]`. If the workflow ultimately fails, do not run the archive command; leave a concise failure report with the failing step and stderr.

## Notes

- Preserve the settings/stories balance from the existing OpenClaw job.
- Keep the visible Korean label `이야기 조각`, but keep the internal key `stories`.
- The article must include the related illustration through the publisher.
- Do not commit `.codex-creative-writer` runtime state.
- Preserve unrelated user changes.
