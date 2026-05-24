---
name: clobie-setting-writer
description: Write Clobie setting concept drafts for the hns17 creative writer schedule. Use for Korean worldbuilding, game setting concepts, mechanics-driven fantasy or SF settings, and Codex scheduled Clobie writing that must produce a draft JSON with an illustration prompt.
---

# Clobie Setting Writer

## Purpose

Create one Clobie setting concept and one related illustration for the scheduled writer flow. A setting must be worth rereading: a world, place, system, faction, or rule whose mechanics expose a human cost. Do not produce a pleasant but weightless gimmick. Every setting should answer: what must people choose, lose, or become because this rule exists?

This skill owns writing and illustration generation only. Do not publish to Discord, write the final markdown article, commit, or push. The schedule handles storage, delivery, and git.

## Input

The scheduler provides `.codex-creative-writer/current_run.json`. Read it before writing. Use:

- `target_type`
- `recent_items`
- `avoid_titles`
- `avoid_devices`
- `tone_seed`
- `draft_path`
- `selected_art_skill`

Avoid repeating the latest 12 works in title, core device, setting device, or emotional premise.

## Output Contract

Write exactly one JSON object to the `draft_path` from the run JSON. The file must be UTF-8 and valid JSON.

Required shape:

```json
{
  "title": "Korean title",
  "slug": "english-kebab-slug",
  "clobie_type": "settings",
  "genre": "Korean genre label",
  "summary": "One concise Korean summary for archive cards",
  "tags": ["tag1", "tag2", "tag3"],
  "body_markdown": "Markdown body without front matter, H1, genre line, or image markdown",
  "illustration_prompt": "Scene prompt for one related illustration. No text, logo, watermark, or UI.",
  "image_alt": "Korean alt text"
}
```

Do not write front matter. Do not include a top-level `#` heading. Do not include `장르:` at the top. The schedule publisher adds those.

After writing the JSON draft, generate exactly one illustration using the `illustration_prompt` and the selected art skill from the run JSON:

- use `draw-soft-anime` when `selected_art_skill.name` is `draw-soft-anime`
- use `draw-cinema-anime` when `selected_art_skill.name` is `draw-cinema-anime`

Do not generate more than one image for the same run unless explicitly asked to recover a failed image step.

## Writing Standard

- Write in Korean.
- Length target: about 200-500 Korean words.
- Prefer one strong governing idea over many decorative concepts.
- Build around a value conflict, not only a visual hook.
- Let the setting imply stories, choices, and consequences.
- Use concrete institutions, rituals, resources, taboos, jobs, or systems.
- Include at least one unsettling or bittersweet cost.
- Avoid generic archive/library/memory/weather motifs unless the run context demands them.
- Avoid empty proper nouns. A coined name must reveal function, history, or social pressure.

## Structure

Use this body pattern unless the run context strongly suggests another:

1. Opening paragraph: the setting's impossible rule, described through lived reality.
2. Middle paragraph: the human/social cost and the central conflict.
3. Play frame paragraph: what the player, protagonist, or viewpoint role must manage.
4. `## 주요 시스템 (Mechanics)` section with a numbered list of 4 mechanics.

Mechanics must connect to the moral pressure of the setting. They are not UI features; they are playable consequences.

## Illustration Prompt

Make the prompt depict one specific moment from the setting:

- one readable focal subject or place
- clear mood and lighting
- no typography
- no UI, logo, watermark, caption, or text in the image
- suitable for either `draw-soft-anime` or `draw-cinema-anime`

The prompt may be Korean or English, but it must be concrete enough for direct image generation.

The generated illustration should be related to the setting article, not a standalone unrelated art prompt. Leave final image upload, markdown insertion, Discord delivery, and git operations to the schedule.
