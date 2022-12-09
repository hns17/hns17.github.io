---
title: "CubicCraft - VertexAmbient"
categories: [Daily/Work]
tag : ["Unity", "Project", "Voxel", "Block", "CubicCraft", "Ambient"]

---



# CubicCraft - Vertex Ambient

<div class = "cocoen">
    <img src="https://raw.githubusercontent.com/hns17/ImageContainer/main/img/no_ambi.png" alt="array2d_linear" style="max-width: none;" />
    <img src="https://raw.githubusercontent.com/hns17/ImageContainer/main/img/array2d_linear.png" alt="array2d_linear" />
</div>



- 화면 품질 향상을 위해 사용되는 대표적인 것중 하나가 Ambient Occlusion.

- 주로 화면 복잡도나 전처리 단계 등을 크게 고려하지 않고 편하게 사용가능한  SSAO나 라이트맵 베이킹을 많이 사용

- 하지만 아래와 같은 이유로  Mesh 생성시 Ambient 정보를 Vertex 정보에 Bake하여 사용하기로 함

  - 프로젝트는 넓은 공간의 오브젝트를 Dynamic하게 생성하며 포워드 렌더로 진행

  - SSAO의 경우 디퍼드 렌더가 아니면 사용하기 어렵고 화면 공간 밖의 오브젝트에는 반영되지 않는 등 단점도 존재함

  - 라이트맵은 넓은 공간의 데이터를 Dynamic하게 생성하는 과정에서 사용하기 어려움



### 1. Calculate Ambient Data

<img src="https://0fps.files.wordpress.com/2013/07/aovoxel2.png" style="zoom:50%;" />

- Block Based Voxel의 경우 Vertex에 대한 총 4가지 상황만 고려하면 된다.
  - 0 : 완전 차단된 경우
  - 1 : Side와 Corner가 차단된 경우
  - 2 : Side or Corner 중 하나가 차단된 경우
  - 3 : 차단되지 않은 경우

### 2. Anisotropy Problem

-  



### 3. 장/단점

- 장점
  - 간단한 과정으로 괜찮은 수준의 화면 품질 향상을 가져옴
  - 데이터 생성과정이 CPU 연산이므로 Forward Base Render에 잘 맞음
  - Mesh 생성시 Data를 만들기 때문에 동적이고 넓은 환경에 대해 크게 신경 쓸 필요 없음
  
- 단점
  - Mesh 생성시 주변 블럭 정보를 고려하여 데이터를 만드는 과정이 요구됨
  
  - Ambient 정보에 대한 추가적인 Buffer 사용
  
  - Greedy Meshing 효율이 떨어짐
    - Vertex 단위로 Ambient 정보가 저장되므로 서로 다른 Ambient 정보를 가진 Vertex는 Merge 대상이 될 수 없음
    
    - [VertexAmbient가 적용된 Mesh와 비교]
    
      - AO가 적용된 Mesh의 경우 차폐 구역이 Merge되지 않고 분할 되어있다
    
        <div class = "cocoen">
            <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Greedy.PNG" style="max-width: none;">
            <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/GreedyAmbi.PNG">
        </div>
        
        
        
        
        
         


# Ref

- [https://0fps.net/2013/07/03/ambient-occlusion-for-minecraft-like-worlds/](https://0fps.net/2013/07/03/ambient-occlusion-for-minecraft-like-worlds/)

