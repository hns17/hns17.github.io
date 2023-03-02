---
title: "CubicCraft - EditorGraph"
categories: [Daily/Work]
tag : ["Unity", "Project", "CubicCraft", "VisualElement", "CubicGraph", "VisualScripting"]
---



# CubicCraft - EditorGraph

- VisualElement 기반으로 Map Tool용 Editor 작업 중




## (1) EnvironmentValue  추가

- BlackBoard에 프로젝트 전체에 사용될 환경변수와 관련된 컨트롤 추가

![image-20230302224343545](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230302224343545.png)



## (2) Procedural Node

- VoxelGenerateNode를 폐기하고 ProceduralNode로 분할함
  - 해당 프로젝트가 아닌 다른 프로젝트에서도 사용가능 하도록 공용 노드화 시킴

![ProceduralNode](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/ProceduralNode.gif)





## (3) LayerNode

- LayerNode에 Biome 정보와 PreviewEdit, PositionOffset 기능을 추가



#### 1) Biome

- 생성될 지형의 블럭 구성을 데이터화 하기위한 기능

- 아직 관련된 기능 수정이나 추가가 많이 필요해 보이는데, 어떤 방식으로 에디터를 만들지 떠오르지 않음...

  

#### 2) Preview Edit

- PreviewEdit는 에디터에서 지형을 만들어 확인하는 기능인데 유니티 씬뷰가 아닌 에디터에 추가로 뷰를 만든 이유는 나중에 라이트 설치나 오브젝트 설치 등을 에디터 내에서 하도록 지원하는게 좋다 생각했기 때문임



![PreviewEdit](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/PreviewEdit.gif)

```
위는 NoiseNode를 바탕으로 생성한 밀도 값을 Biome정보에 맞춰 미리보여주는 PreviewEdit 기능.
간단하게 뷰와 카메라 정보 및 줌 기능 정도만 만듬
```



### 3) PositionOffset

- 지형을 생성할때 지형 위치에 따라 추가적으로 밀도 정보를 변경하는 기능
- AnimationCurve를 통해 밀도 정보를 수정함

![PositionOffset](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/PositionOffset.gif)

```
위에서 만든 지형에 PositionOffsetNode를 추가한 경우
Y축을 기준으로 높이가 높아질수록 밀도 값이 감소되도록 변경함
```



## (3) BlendNode

- Procedural Node를 Merge하는 노드

![BlendTexture](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/BlendTexture.gif)

```
위에서 작업한 결과물에 CellularNoise를 혼합한 결과
```



# Next

- 기본적인 틀은 만들어 진거 같은데, 아직 Biome 구성이나 조건 등이 뭔가 별로임
- 기능 제작이 문제가 아니라 어떤 형태로 만들지 정하기가 어려워서 좋은 생각이 떠오를 때 까지 묵혀두기로...
