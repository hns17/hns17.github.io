---
title: "CubicPuzzle - ExtraPattern 추가"
categories: [Daily/Work]
tags: ["Unity", "Project", "Puzzle", "CubicPuzzle", "CubicGraph"]
---

> 핵심 요약
> - 이 글은 `CubicPuzzle - ExtraPattern 추가` 작업에서 진행한 내용을 기록한다.
> - 구현한 기능, 확인한 결과, 남은 과제를 중심으로 정리한다.
> - 프로젝트 로그를 빠르게 훑을 수 있게 핵심을 먼저 배치한다.

### 2022.08.28

- Extra Pattern Match 기능 추가

- InGame

  - Extra Pattern Check, Merge, Convert Block(현재는 기본 블럭으로 변경되게 해둠, 언젠가 특수 블럭 구현하면 변경)

    ![ExtraPattern_match](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/ExtraPattern_match.gif)

- Extra Pattern Editor 구현

  - 예정에 없던 기능 추가로 전체적인 에디터 구성 변경

  - Pattern 추가, 삭제, Root Position 설정, 파생 패턴 및 InGame용 SctableObject 출력

  <img src="https://raw.githubusercontent.com/hns17/ImageContainer/main/img/ExtraPattern_editor.gif" alt="ExtraPattern_editor" style="zoom: 67%;" />
