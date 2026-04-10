---
title: "실패 작업 기록 01"
date: 2026-04-10 19:15:28 +0900
clobie_type: "failed-run"
genre: "image cron failure"
mood: "interrupted"
tags:
  - "failed-run"
  - "image-cron"
  - "manual-debug"
  - "archive"
image_url: ""
prompt: "Prompt text was not preserved in this page record. See linked conversation and local debug notes for reconstruction."
source_tool: "chatgpt"
source_model: "Art Director Soft Atmospheric Anime"
chatgpt_share_url: "https://chatgpt.com/g/g-699d949806988191b9354c13ffd805b5-art-director-soft-atmospheric-anime/c/69d8cd92-a2c8-83e8-b6ee-d43f9043d3ce"
status: "failed"
failure_stage: "github-upload"
failure_reason: "Generated image was detected, but GitHub Contents API upload failed with HTTP 422 because the existing file SHA was not supplied."
---

# 실패 작업 기록 01

장르: image cron failure

이 문서는 2026-04-10 이미지 크론 점검 중 저장되지 못한 실패 실행을 보존하기 위한 페이지 기록이다.

## 상태
- 결과: 실패
- 단계: GitHub 업로드
- 원인: 기존 경로 파일 덮어쓰기 시 `sha` 없이 PUT 요청이 발생해 HTTP 422 에러로 종료됨

## 대상 링크
https://chatgpt.com/g/g-699d949806988191b9354c13ffd805b5-art-director-soft-atmospheric-anime/c/69d8cd92-a2c8-83e8-b6ee-d43f9043d3ce

## 메모
- 생성 이미지 감지 자체는 성공한 실행이었다.
- 하지만 최종 PNG 업로드가 실패해 이미지 링크, 문서 생성, 채널 전송으로 이어지지 못했다.
- 이후 업로드 전에 기존 파일 SHA를 조회하도록 스크립트를 수정했다.
