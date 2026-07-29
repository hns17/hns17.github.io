# Graphics Series Automation Prompt

Write exactly one engine-independent graphics-series article in sequence.

## Required reading

Read these files completely before editing:

1. `AGENTS.md`
2. `POST_STYLE_GUIDE.md`
3. `GRAPHICS_POST_GUIDE.md`
4. `GRAPHICS_SERIES_PLAN.md`
5. `_data/graphics_series.yml`

Treat `GRAPHICS_SERIES_PLAN.md` as the source of truth for topic order and
`GRAPHICS_POST_GUIDE.md` as the source of truth for writing, research, image and validation rules.

## Selection

1. Find the earliest unchecked item in `GRAPHICS_SERIES_PLAN.md`.
2. Do not select a later item.
3. Search `_posts/Graphics/Series` for the selected `series_id`.
4. If a matching draft or image folder already exists, treat the item as under user review.
5. In that case, make no file changes, do not resume the draft, and report that explicit user approval is required.
6. Create a draft only when every earlier item is checked and the selected item has no existing draft.
7. Process exactly one series item in this run.

## Research and narrative

- Start from why the topic is needed in computer graphics.
- Use the sequence `problem → historical context → solution → limitation → next question`.
- Prefer original papers, standards, official institutional records and primary technical documentation.
- Verify dates, names, formulas and claimed contributions.
- Link named experiments, illusions, demos and papers at their first mention in the body.
- A reference-list entry alone does not replace the first-mention link.
- For a central static example, include a licensed local visual or link its official original and proof page.
- For a motion-dependent example, link an official interactive demo or animation and tell the reader what to observe.
- Do not create empty placeholder articles or out-of-sequence posts merely to provide a link.
- Keep the article engine-independent. Do not add Unity or another engine's settings or workflow.

## Images

- Plan the visuals before drafting the full body.
- Include at least one locally stored explanatory image.
- Prefer original SVG diagrams, controlled comparison renders, graphs and pipeline diagrams.
- Do not use decorative images to satisfy the requirement.
- Do not hotlink a new article's final image from an external server.
- Use external material only when reuse is permitted; otherwise redraw the relationship and cite the source.
- Add meaningful alt text and a caption with the purpose and source.
- Use the article folder under `assets/images/posts/graphics-series/`.

## Writing

- Create the post under `_posts/Graphics/Series`.
- Use the actual run date in the filename.
- Read the current series ID, display title, unique category and page URL from the plan and `_data/graphics_series.yml`.
- Use the registered `Graphics/Series/<Series-Key>` value as the category. Never use the shared `Graphics/Series` path as a post category.
- Prefix the title with `[연재 제목 NNN]`, where `NNN` is the zero-padded three-digit `series_order`.
- Add the registered `series`, `series_title`, `series_url`, the selected `series_id`, and matching `series_order`.
- Do not repeat the front-matter title as a body `#` heading.
- End with `정리`, a question leading to the next planned article, and `참고`.

## Validation

1. Recheck technical claims against the selected primary sources.
2. Check every local image path in the Markdown.
3. Inspect every created raster image or SVG rendering for correctness and readability.
4. Run the repository's Jekyll build.
5. Inspect the generated HTML for the article, images, captions and links.
6. Leave the selected plan item unchecked even when all checks pass.
7. Report the result as a draft awaiting user review, never as a completed series item.

If validation fails, leave the plan item unchecked and report the exact blocker. Do not move to the next item.

Only a manual task with explicit user approval may mark an item complete. Completion requires the approval,
a commit containing the approved article and completion marker, a successful push, and verification that the
completion commit exists on the remote branch.

## Scope and safety

- Preserve unrelated user changes.
- Do not rewrite earlier series articles unless needed to repair a direct sequence link created by this run.
- Do not create more than one article.
- Do not mark the plan item complete.
- Do not commit, push, deploy or publish externally from a scheduled run.
