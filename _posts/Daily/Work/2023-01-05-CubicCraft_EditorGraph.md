---
title: "CubicCraft - EditorGraph"
categories: [Daily/Work]
tags: ["Unity", "Project", "CubicCraft", "VisualElement", "CubicGraph"]

---

> 핵심 요약
> - 이 글은 `CubicCraft - EditorGraph` 작업에서 진행한 내용을 기록한다.
> - 구현한 기능, 확인한 결과, 남은 과제를 중심으로 정리한다.
> - 프로젝트 로그를 빠르게 훑을 수 있게 핵심을 먼저 배치한다.

- VisualElement 기반으로 Map Tool용 Editor 작업 중

### 1차 작업내역

- 기본 CubicGraph에 기능 추가
  - Resizable Element 추가
  - CubicSlider 추가
  - NodeEvent용 Interface 추가
- Project용 Graph 생성 후 기능 구현
  - CubicVoxelGenerator Graph 생성
  - WorldNode, LayersNode, LayerNode, GenerateNode 추가

#### GenerateNode & PreviewContainer

![Noise](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Noise.gif)

```
Map Generate를 위한 Noise Node와 Preview 기능
Noise Option이 많아서 NodeView가 상당히 복잡함
```

#### Blending Option

![Blend](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Blend.gif)

```
Noise와 Noise Blending 기능
BlendType에 따라 Child Noise를 Main에 Blending
```

#### Layers Node

![Layers](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Layers.gif)

```
Layers 분할
높이 단위로 영역 분할
```

### 추가할 것들

- 필드 정보들 Serialize 하기
- Layer에 Biom 정보 추가 후 색상으로 표현
- Data 파일로 내보내기
- Area Node
- VoxelMap 프로젝트와 통합하기
- 계속 안하게 되네...
