---
title: "CubicPuzzle - 기능 개선"
categories: [Daily/Work]
tag : ["Unity", "Project", "Puzzle", "CubicPuzzle"]
---



#### [2022.07.26]

- UniTask 종료 문제 수정

  - 진행중인 Task 작업이 씬 전환등으로 중단될 필요가 있어 Cancellation Check 후 중단 하도록 변경
    - 전체 Task에 Check API를 사용하면 느리므로 특정 단위에 Check Point 구성
    - 반복적(Loop, Recursive)인 Task 위주로 Check Point 구성
  - Cancellation Token 을 관리하는 Manager Script 추가

- Collider Performance 개선

  - TestDevice : Samsung Galaxy A52

  [수정 전]

  ![image-20220708225911538](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220708225911538.png)

  [수정후]

  ![image-20220816115813494](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220816115813494.png)

  - Physics(주황색) 부분 개선

  - 좌표 계산이 아닌 Raycast를 통해 Hit Block을 추적 중이므로 Block에 Collider를 사용중

    - 좌표계산의 경우 보드 Type(Hex, Grid...)에 따라 계산 방식도 달라져야해서 편의상 RayCact 사용
    - Cell의 형태에 따라 변경되는 Touch 영역을 코드상으로 고려할 필요없음

  - Block 파괴 연출로 인해 Unity 내부적으로 Collider 재구성하는 부분에서 성능 저하 생김

    - Collider 활성화 및 비활성화
    - Block Size 변경

  - Physic2D SimulationMode를 Fixed Update -> Script로 변경

    - Script를 통해 Simulation

      
