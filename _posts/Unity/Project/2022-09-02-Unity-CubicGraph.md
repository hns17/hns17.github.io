---
title: "CubicGraph"
categories: [Unity/Project]
tag : ["Unity", "Project", "UIElement", "CubicGraph"]
---

# CubicGraph

### 1. 개요

- Project에 사용될 Data를 Node 기반으로 구성하는 Editor 만들기
- Node 추가 및 변경 등의 확장을 고려해서 작업
- Detail
  - Unity 2021.3 사용
  - UIElement Base로 개발 진행
    - ui builder, uss, uxml 



### 2. 기능

####  (1) Project 추가하기

- CubicSystem-Generator-ProjectGeneratorWindow를 통해 신규 Project를 추가할 수 있다

  ![image-20220904194039861](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220904194039861.png)

  

#### (2) Node 추가하기

- CubicSystem-Generator-NodeGeneratorWindow를 통해 Project에 사용할 기본 노드를 생성할 수 있다

  ![image-20220904195018896](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220904195018896.png)

#### (3) Project Window 열기

- 추가된 프로젝트는 CubicSystem-Project 메뉴에서 확인 가능

  - Create : 신규 데이터 생성
  - Open Asset : 기존 작업 데이터 불러오기

  ![image-20220904194816414](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220904194816414.png)

- 신규 Data Asset은 Quick Menu의 CubicSystem을 통해서 도 생성 가능



#### (4) Node 구성하기

- 앞서 프로젝트에 추가한 노드를 통해 데이터 구성

  ![image-20220904195545569](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220904195545569.png)



# PuzzleGame Editor

- PuzzleBoard Stage 및 패턴 제작용 에디터로 확장

### [Stage Editor]

<img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/CubicPuzzleEdit.gif" allign = "left" />

### [Extra Pattern Editor]

<img src="https://raw.githubusercontent.com/hns17/ImageContainer/main/img/ExtraPattern_editor.gif" alt="ExtraPattern_editor" style="zoom: 80%;" />



# Block based Voxel Editor

- 블럭 기반 복셀 커스텀 에디터로 확장

![Noise](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Noise.gif)

![BlendTexture](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/BlendTexture.gif)
