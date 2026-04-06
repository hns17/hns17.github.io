# Clobie Architecture Draft

## Goal
디스코드 창작방의 작업물을 GitHub Pages에서 감상 가능한 작업실형 아카이브로 재구성한다.

## Core Idea
- 입력은 Discord 채널 기준으로 들어온다.
- 출력은 작품 기준(유형 / 장르 / 시리즈 / 태그)으로 재구성한다.

## Collections
- `_clobie_writing`
- `_clobie_art`

## Writing Metadata
- `title`
- `date`
- `clobie_type`: `settings` | `stories` | `notes`
- `genre`
- `series`
- `tags`
- `summary`
- `source_channel`
- `source_message_id`

## Art Metadata
- `title`
- `date`
- `clobie_type`: `characters` | `backgrounds` | `concepts`
- `mood`
- `series`
- `tags`
- `image`
- `summary`
- `source_channel`
- `source_message_id`
- `prompt` (optional)

## Pages
- `/clobie/` : 작업실 소개 / 구조 안내
- `/clobie/writing/` : 글 메인
- `/clobie/writing/settings/`
- `/clobie/writing/stories/`
- `/clobie/writing/notes/`
- `/clobie/art/` : 그림 메인 갤러리
- `/clobie/art/characters/`
- `/clobie/art/backgrounds/`
- `/clobie/art/concepts/`

## Recommended Next Steps
1. 디스코드 글 채널 저장물 3~5개 실제 이관
2. 디스코드 그림 채널 저장물 3~5개 실제 이관
3. 카드/갤러리 UI 미세조정
4. 시리즈 페이지 필요 여부 검토
5. Discord → Markdown 변환 자동화 검토
