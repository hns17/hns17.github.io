# Codex Creative Art Cron

This folder supports the Codex Creative Art automation.

The stable path keeps image generation separate, then uses one publisher
command that is easy to approve persistently:

- `generate_prompt.py` prepares one prompt and one selected drawing skill.
- Codex generates exactly one image with `draw-soft-anime` or
  `draw-cinema-anime`.
- `publish_current_run.py` locates that image, uploads it to GitHub, writes the
  Clobie art markdown, commits/pushes only that markdown file, and sends the
  Discord webhook.

Approve `python3 scripts/creative_art_codex/publish_current_run.py` persistently
in Codex when prompted. That keeps unattended publishing scoped to one command
instead of granting broad access to every shell command.

Do not use `finalize_run.py` as the normal delivery path. Keep it only as a
legacy recovery helper.

Runtime state is written under `.codex-creative-art/`; it should stay
uncommitted.

## Recommended Codex Schedule Shape

1. Run `python3 scripts/creative_art_codex/generate_prompt.py`.
2. Read `.codex-creative-art/current_run.json`.
3. Use exactly the prepared `prompt` and `selected_skill`.
4. Generate exactly one image with the selected skill.
5. Publish with one approval-friendly command:

```bash
python3 scripts/creative_art_codex/publish_current_run.py --webhook-url "$CREATIVE_ART_DISCORD_WEBHOOK_URL"
```

If that command needs approval, choose persistent approval for the command
prefix. Do not regenerate the image for the same run after successful image
generation.

The publisher requires a Discord webhook URL through `--webhook-url`, the
`CREATIVE_ART_DISCORD_WEBHOOK_URL` environment variable, or the macOS Keychain
generic-password service named `creative-art-discord-webhook-url`. It fails
early when the webhook is missing instead of silently skipping delivery.

See [`CODEX_AUTOMATION_PROMPT.md`](/Users/cubix/Desktop/Git/hns17.github.io/scripts/creative_art_codex/CODEX_AUTOMATION_PROMPT.md) for the repo-local automation prompt.

Example metadata JSON:

```json
{
  "title": "하드 SF의 우주 전함",
  "slug": "hard-sf-warship",
  "prompt": "2D anime sci-fi illustration ...",
  "item": {
    "type": "sf",
    "genre": "하드 SF",
    "mood": "작전 직전의 긴장감",
    "species": "우주 전함"
  },
  "selected_skill": {
    "name": "draw-soft-anime",
    "source_model": "Codex draw-soft-anime"
  }
}
```

When publishing fails, rerun `publish_current_run.py` for the same run. Do not
regenerate the image for the same run.

## Legacy Compatibility

`finalize_run.py` remains in this folder only for older runs and manual
recovery. Do not add it back to the hourly automation prompt.

```bash
python3 scripts/creative_art_codex/generate_prompt.py
```

Webhook reaction support is not included. Discord webhooks can send messages and
embeds, but adding a reaction to the sent message requires a bot token.
