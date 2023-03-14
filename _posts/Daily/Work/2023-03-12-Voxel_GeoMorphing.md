---
title: "Voxel GeoMorphing"
categories: [Daily/Work]
tag : ["Unity", "Project", "Voxel", "Vertex Morphing", "Morphing", "Geometry"]
---

# Voxel GeoMorphing

## 1. 개요

- 이전에 Voxel 지형에 사용한 변환을 오브젝트에 사용 가능하지 않을까 해서 만들어봄
- 방식은 동일하며, 몇 가지 계산 옵션을 추가하거나 변경함
- 아래는 결과

![VoxelGeoMorphing](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/VoxelGeoMorphing.gif)

```
1. Asset Store에 있는 무료 복셀 오브젝트를 아무거나 받음
2. Object VertexMorphing 처리된 마테리얼로 교체
3. LOD 값 변경
```



## 1. 장점, 단점

### [장점]

- 쓰기 편함
- 그렇게 무겁지 않음
  - 버텍스 셰이더에서 처리됨
  - Shift 연산 두 번, frac, 사칙 연산을 좀 많이함(6번 정도)
- 연출용으로 쓸만할 지도?



### [단점]

- 원하는 형태로 변경이 불가능
  - 일부가 납작한 평면으로 변환됨
- 겹치는 면이 발생해 z-fighting 문제가 생김
- 정점 정보가 양수가 아니면 오동작함
  - 바운딩 박스 위치 문제가 있음.
  - 메쉬 셰이더를 쓰거나 위치 마춰주면 크게 문제되지는 않을 듯
- 연출을 제외하면 쓸모가 없음
- 전체 모델의 최소 단위 복셀의 사이즈가 다를 수 있으므로 원하는 수준의 스케일을 맞추기 번거로움
  - 마테리얼을 세분화 하거나 모델 파일의 복셀 사이즈를 통합하거나 그냥 쓰거나...