---
title: "CubicPuzzle - Start PuzzleProject"
categories: [Daily/Work]
tag : ["Unity", "Project", "Puzzle", "CubicPuzzle"]
---



# 1. 목적

- 아래의 목적을 위해 간단한 Puzzel Project 진행
  - Dependency Injection을 위해 Zenject 사용하기
  - 비동기 프로그래밍을 위해 Unitask 사용하기
  - MVP 아키텍처 패턴으로 구조 설계하기
  - ReactiveProgramming을 위해 UniRx 사용하기
  - VisualElement를 바탕으로 Editor 기능 제작하기



# 2. Work

### 1. 구현

- ThreeMatch 형태의 HexPuzzle
- 기본적인 매칭, 파괴, 이동, 생성 등

![ThreeMatch](https://raw.githubusercontent.com/hns17/ImageContainer/9b72e213e2ddcf490fdf96211c76a9d858c57915/img/ThreeMatch.gif)

### 2. Simulation

![gif_animation_002](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/gif_animation_002-1657289632295.gif)

- Profile

  ![image-20220708225911538](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220708225911538.png)

  - Drop&Fill Table 구성시 18~20 Frame 까지 떨어졌으나 아래 내용 적용 후  30 Frame 이상 유지 중...
    - 반복 연산으로 인한 Overhead 최적화
      - Dictionary ContainKey -> TryGetValue
      - foreach -> for
      - data caching(loop count, get_property...)
      - 기타
    - SetActive 사용 최소화
      - Object를 비활성화 하기 보다는 화면 밖으로 이동시킴

- Memory

  - ~~Native Memory를 사용 중.~~

    - ~~원래 목적은 StackAlloc을 통해 Stack Base 자료구조 사용에 있었으나, Nuget Dll 이나 Unsafe Base의 Pointer를 사용하기 꺼려져 힙을 직접 관리하는 NativeArray를 사용.~~

    - IL2CPP Build 시 NativeArray가 StackAlloc 다음으로 접근이  빠르다. [#Ref](https://qiita.com/pCYSl5EDgo/items/2901604b72cbb2764940)

      ![image-20220708234852478](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220708234852478.png)

    - GC 호출 문제를 회피할 수 있으나 External Fragmantation 문제가 발생 할 수 있으므로 주의 필요.

  - Memory Profile

    - Stage 생성 후

      ![image-20220708235359255](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220708235359255.png)

    - 30분 경과

      - Native Memory 사용량이 3MB 정도 증가하였다.

      ![image-20220708235434335](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220708235434335.png)

  - NativeArray는 기능적으로 불편하고 대용량 메모리 사용 같은 특정 상황이 아닌 경우 크게 의미가 없어 보이므로 다음 프로젝트 진행시에는 잡 시스템 사용을 제외하면 사용하지 않을 생각.



### 2. Editor

- Stage 제작용 Editor 

<img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/CubicPuzzleEdit.gif" allign = "left" />