---
title: "CubicPuzzle - OneTouch Puzzle 추가 및 Unity Version 변경"
categories: [Daily/Work]
tag : ["Unity", "Project", "Puzzle", "CubicPuzzle"]
---





#### [2022.08.06]

- OneTouch 방식의 Puzzle 게임 추가

  ![OneTouch](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/OneTouch.gif)

#### [2022.08.15]

- Unity Version 2020에서 2021로 변경
- 기존의 NativeArray를 사용한 코드 삭제
  - stackalloc : 2021 버전에서 지원되는 Span 타입을 이용해 stack 영역을 사용하도록 수정
  - objectpool : 2021 버전에서 추가된 ObjectPool을 이용하도록 수정
  - collection pool : 2021 버전에서 추가된 Collection Pool을 이용하도록 수정

