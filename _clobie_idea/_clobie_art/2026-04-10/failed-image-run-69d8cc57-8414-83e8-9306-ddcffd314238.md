---
title: "실패 작업 기록 03"
date: 2026-04-10 19:13:24 +0900
clobie_type: "failed-run"
genre: "image cron failure"
mood: "stalled"
tags:
  - "failed-run"
  - "image-cron"
  - "manual-debug"
  - "archive"
image_url: ""
prompt: "2D anime illustration(비실사), cinematic key visual, full-body, eye-level. 아동 남성 흡혈귀 캐릭터 1명. Genre/theme: 어반 느와르, 트램이 지나는 구시장 골목..."
source_tool: "chatgpt"
source_model: "Art Director Cinematic Cel Style"
chatgpt_share_url: "https://chatgpt.com/g/g-699cd04b3fe88191813f60ecabf64a38-art-director-cinematic-cel-style/c/69d8cc57-8414-83e8-9306-ddcffd314238"
status: "failed"
failure_stage: "result-detection"
failure_reason: "The prompt was submitted and present in the page body, but articleCount stayed at 0, so the automation could not discover the generated image block and timed out."
---

# 실패 작업 기록 03

장르: image cron failure

이 문서는 2026-04-10 이미지 크론 점검 중 저장되지 못한 실패 실행을 보존하기 위한 페이지 기록이다.

## 상태
- 결과: 실패
- 단계: 결과 감지
- 원인: 프롬프트는 살아 있었지만 `articleCount=0` 상태가 지속되어 자동화가 결과 블록을 찾지 못함

## 대상 링크
https://chatgpt.com/g/g-699cd04b3fe88191813f60ecabf64a38-art-director-cinematic-cel-style/c/69d8cc57-8414-83e8-9306-ddcffd314238

## 메모
- 이 링크는 DOM 탐지 실패의 대표 사례다.
- 수동 진단 로그에서 `bodyHasNeedle=true`, `articleCount=0` 반복이 확인되었다.
- 이후 article 외에 main/body 기반 탐지를 추가했다.
