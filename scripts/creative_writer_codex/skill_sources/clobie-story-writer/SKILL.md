---
name: clobie-story-writer
description: Write Clobie story fragment drafts for the hns17 creative writer schedule. Use for Korean literary short story openings, lyrical or twist-driven story fragments, value-conflict narratives, cosmic-question stories, and Codex scheduled Clobie writing that must produce a draft JSON with an illustration prompt.
---

# Clobie Story Writer

## Purpose

Create one Clobie story fragment and one related illustration for the scheduled writer flow. The story should leave a sentence behind in the reader. It should grow from a poetic statement, a moral pressure, a contradiction, or a reversal. It must not feel like a random premise with no residue.

This skill owns writing and illustration generation only. Do not publish to Discord, write the final markdown article, commit, or push. The schedule handles storage, delivery, and git.

Useful target shapes:

- a lyrical fragment that ends by transforming an earlier image
- a two-person story whose final line reframes the first scene
- a value-conflict story about one person's universe versus the crowd's demand
- a cosmic-question story with long scale and a final turn, without imitating any living or famous author's prose
- a quiet scene where the reversal is emotional rather than plot-heavy

## Input

The scheduler provides `.codex-creative-writer/current_run.json`. Read it before writing. Use:

- `target_type`
- `recent_items`
- `avoid_titles`
- `avoid_devices`
- `tone_seed`
- `story_taste`
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
  "clobie_type": "stories",
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
- Open with an embodied scene, not an explanation.
- Build around one pressure: sacrifice, memory, bloom after winter, private universe, guilt, choice, silence, or irreversible tenderness.
- If using dialogue, each quoted line gets its own paragraph.
- Use sensory detail, but make it serve the decision or reversal.
- Avoid shallow whimsy, lore-only exposition, and cleverness without emotional cost.
- End with a line or short paragraph that reinterprets the story's central image.

## Depth Pattern

Choose one pattern per draft:

- **Lyrical closure**: a relationship or promise begins the story, and the ending condenses into a poetic statement.
- **Value conflict**: a society demands one life for many; the story protects the equal weight of one private universe.
- **Cosmic question**: a question crosses time, scale, or generations; the answer arrives as a reversal rather than an explanation.
- **Intimate twist**: the final fact changes the emotional meaning of an earlier act.

Do not moralize directly. Let the scene prove the value.

## Illustration Prompt

Make the prompt depict one specific moment from the story:

- two people, one person, or one symbolic place from the scene
- clear emotional lighting and composition
- no typography
- no UI, logo, watermark, caption, or text in the image
- suitable for either `draw-soft-anime` or `draw-cinema-anime`

The prompt may be Korean or English, but it must be concrete enough for direct image generation.

The generated illustration should be related to the story article, not a standalone unrelated art prompt. Leave final image upload, markdown insertion, Discord delivery, and git operations to the schedule.
