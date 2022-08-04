---
title: "SampleProject_CubicPuzzle"
categories: [Unity/Project]
tag : ["Unity", "Project", "Puzzle"]
---



# SampleProject_CubicPuzzle

### 1. 개요

<figure class="half">
    <image src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/ThreeMatch.gif"/>
    <image src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/OneTouch.gif"/>
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/CubicPuzzleEdit.gif" allign = "left" />
</figure>
- 소개 : 매치 퍼즐 기능 및 툴 개발

- 목적 : 샘플 코드 및 포트폴리오 제출

- 개발 기능 

    - ThreeMatch
      - 라인 매치(세로, 대각선, 역대각선), Square 매치,
    - OneTouchMatch
      - 이웃 블럭 매치

    - Drop & Fill Event

    - Stage Data Editor

    - 기타 효과 및 구성

- Detail

  - Unity 2020.3 사용
  - Reactive Programming을 위해 UniRx 사용

  - Dependency Injection을 위해 ZenJect 사용
  - MVP 패턴 중심으로 개발 진행

  - 확장성을 고려한 설계에 중점을 두고 개발 진행
    - 매치 퍼즐 형태의 게임 추가 및 보드 추가
  - 추가 사용 패키지 : InputSystem




### 2. UML

- Stage 구성도
  - 의존, 연관, 상호연관 확인

![CubicPuzzle_Stage](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/CubicPuzzle_Stage.png)

### 3. Simulation

![gif_animation_002](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/gif_animation_002-1657289632295.gif)

- 화면 전체를 채우는 보드를 구성 후 매치 및 파괴가 반복되는 환경 구성

- Match Test 및 Performance Test

- Test Device : LG G8

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
  - Native Memory를 사용 중.
    
    - 원래 목적은 StackAlloc을 통해 Stack Base 자료구조 사용에 있었으나, Nuget Dll 이나 Unsafe Base의 Pointer를 사용하기 꺼려져 힙을 직접 관리하는 NativeArray를 사용.
    
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





### 4. 이후 변경사항

##### [2022.07.26]

- UniTask 종료 문제 수정

  - 진행중인 Task 작업이 씬 전환등으로 중단될 필요가 있어 Cancellation Check 후 중단 하도록 변경
    - 전체 Task에 Check API를 사용하면 느리므로 특정 단위에 Check Point 구성
    - 반복적(Loop, Recursive)인 Task 위주로 Check Point 구성
  - Cancellation Token 을 관리하는 Manager Script 추가

- Collider Performance 개선

  [수정 전]

  ![image-20220708225911538](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220708225911538.png)

  [수정후]

  ![image-20220727114320867](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220727114320867.png)

  - Physics(주황색) 부분 개선
  - 좌표 계산이 아닌 Raycast를 통해 Hit Block을 추적 중이므로 Block에 Collider를 사용중
    - 좌표계산의 경우 보드 Type(Hex, Grid...)에 따라 계산 방식도 달라져야해서 편의상 RayCact 사용
    - Cell의 형태에 따라 변경되는 Touch 영역을 코드상으로 고려할 필요없음
  - Block 파괴 연출로 인해 Unity 내부적으로 Collider 재구성하는 부분에서 성능 저하 생김
    - Collider 활성화 및 비활성화
    - Block Size 변경
  - Physic2D SimulationMode를 Fixed Update -> Script로 변경
    - Script를 통해 Simulation





# Ref

- Youtube : [https://youtu.be/yKh607hPXl0](https://youtu.be/yKh607hPXl0)
