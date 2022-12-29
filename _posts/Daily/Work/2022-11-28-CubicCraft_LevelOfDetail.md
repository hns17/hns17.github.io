---
title: "CubicCraft - Level of Detail"
categories: [Daily/Work]
tag : ["Unity", "Project", "CubicCraft", "LOD", "PopBuffer"]

---



# CubicCraft - Level Of Detail

![levelofdetail](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/levelofdetail.gif)

- PopBuffer를 이용한 Block Based Voxel Level Of Detail
- 사실 프로젝트에 도움되는 기능은 아니며 흥미있어서 만들어 본 기능



## 1. PopBuffer Based Level of Detail

- 꽤 오래전에 작성된 기술 문서에서 시작
  - [https://x3dom.org/pop/](https://x3dom.org/pop/)
  - [https://0fps.net/2018/03/03/a-level-of-detail-method-for-blocky-voxels/](https://0fps.net/2018/03/03/a-level-of-detail-method-for-blocky-voxels/)
-  Web이나 모바일 환경에서 데이터가 큰 모델 파일을 로드 할 경우 부담을 줄이기 위해 단계별로 분할하여 로드하고 표현
- 만들어진 Vertex 정보를 Face단위로 Level 계산하여 분할 후 정렬
- 이렇게 정렬된 Vertex 정보를 적절한 Level로 Set 하고 최종적으로 Level에 맞게 셰이더에서 지오메트리 모핑함



## 2. 사용 후 장/단점

- 일반적인 지형 LOD의 경우 보통 Quad나 Octree를 사용하는데 이러한 LOD에는 몇가지 불편한 점들이 있다.
- 이와 비교했을때 차이점을 알아보자



### (1) 장점

#### 가. 추가적인 Vertex Buffer를 구성할 필요가 없다

- PopBuffer는 Level 단위 정렬된 Vertex 정보로 구성되기 때문에 VertexBuffer와 Level 별 Count만 있으면 된다.



#### 나. Chunk 단위 작업에 편하다.

- 보통 Tree를 이용한 LOD는 Chunk 단위보다는 지형 전체에 영향을 미친다.
  - Chunk 단위로 분할하는 것도 가능하지만 노드 분할이나 LOD 적용, 크랙 문제 처리 등이 상당히 불편해짐
- 이와 달리 PopBuffer를 이용하면 Chunk별로 별도의 VertexBuffer를 가지기만 하면 되므로 다른 점을 크게 신경쓸 필요가 없다.
- 이는 완전 독립된 Chunk 사용에 도움이 된다.



#### 다. Poping Issue

- VertexShader에서 Morphing하기 때문에 Level간 Popping 현상이 해소된다.
- 아래는 Level 간 거리를 아주 짧게 적용한 Level of Detail
  - 멀리 있는 물체와 플레이어 중심의 차이를 비교했을때 레벨 전환이 자연스럽다



#### 라. Greedy Meshing Algorithm과 잘 맞다

- Tree 기반의 Level Of Detail은 Mesh Merge 알고리즘과 잘 어울리지 않다.
- Mesh Merge가 많은 Vertex 감소 효과를 가져다 주지만 Merge 알고리즘은 꽤 무거운 연산이다.
- 이 둘을 같이 사용하여 (Tree & Merge Meshing) 두 가지를 같이하는 경우 가지게 되는 부담이 가볍지 않다

- PopBuffer LOD의 경우 만들어진 Vertex를 추가로 1회 정렬하기만 하면 되므로 부담이 크지 않다.



#### (2) 단점

#### 가 . Geometry Morphing

- Vertex Shader에 연산이 추가되므로 그래픽 레이어 연산량이 증가한다.



#### 나. 크게 쓸모가 없다

- Vertex 최적화와 잦은 Buffer Set을 피하기 위해 Greedy Meshing을 사용하고 있으며, 거리에 따라 Load / UnLoad를 수행할 생각이기 때문에 LOD 자체가 필요가 없다.

  

#### 다. Vertex Lighting & Ambient Issue

![lod_issue](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/lod_issue.gif)

- Vertex에 Lighting과 Ambient 정보를 Bake해서 사용할 수 없다.

- VertexShader에서 GeoMorphing되기 때문에 정보가 맞지 않다

  - 재 계산하는 방법이 있겠지만 그런 경우 이 기능의 이점이 없다고 생각함

  - 먼 거리의 경우 굳이 Ambient 표현이나 Point Lighting 처리가 필요하지 않을테니 크게 문제되지 않을지도...
  - 다만 DirectionalLighting을 Vertex에 Bake해서 사용한다면 해당 기능은 사용하지 않는게 맞을거 같다.





# Result

![res](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/res.gif)

```
거리 기반으로 적용한 Level Of Detail
```



- 단순 연출용이나 자연스러운 먼 거리 청크 표현으로는 쓸만 할지도?
- 어쩌면 미니맵 용으로 쓸 수 있을지도 모르겠다





# Ref

- [https://x3dom.org/pop/](https://x3dom.org/pop/)
- [https://0fps.net/2018/03/03/a-level-of-detail-method-for-blocky-voxels/](https://0fps.net/2018/03/03/a-level-of-detail-method-for-blocky-voxels/)