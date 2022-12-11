---
title: "CubicCraft - GreedyMeshing"
categories: [Daily/Work]
tag : ["Unity", "Project", "Voxel", "Block", "CubicCraft", "GreedyMeshing"]
---



# CubicCraft - Greedy Meshing

- 주변 블럭 상태를 확인후 동일한 블럭이면 하나로 합쳐서 많은 Vertex, Mesh 정보를 줄임
- JobSystem과 Noise Asset 사용



### 1. Greedy Meshing

- Voxel 단위 처리와 Mesh 단위 처리로 나눠 생각해볼수 있음

- Mesh 단위 

  - 각 방향에 대해 면 단위로 처리를 하므로 합치는 과정이 복셀 단위보다 6배 가량 더 요구됨
  - 외부에 보이는 면을 대상으로 방향마다 계산하므로 내부의 Culling을 신경쓸 필요없다

- Voxel 단위

  - 하나의 블럭단위 검사로 합치는 것을 처리하므로 Mesh 단위보다 빠르다
  - 내부에 대한 정점 컬링이 제대로 이루어 지지 않아 효율이 떨어짐

- Vertex를 최소화하기 위한 방법이므로 Mesh단위 합치기를 수행하기로 함

- Voxel / Mesh 단위 합치기 차이점

  - 아래 단순한 예를 보면 같은 상태를 구성하는데 Voxel의 경우 4개의 큐브 -> 24개의 쿼드 메쉬가 필요
  - Mesh의 경우 12개의 쿼드 메쉬로 표현됨
  - Mesh 단위는 눈에 보이는 표면 만을 대상으로 하기에 내부를 신경 쓸 필요없지만 각 방향(6 방향)에 대해 연산이 필요
  

<img src="https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221205115415969.png" alt="image-20221205115415969" style="zoom:50%;" />



- GreedyMeshing의 적용된 결과


<img src="https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Greedy.PNG" alt="Greedy" style="zoom:67%;" />

### 2. Texturing

- 하나의 마테리얼 사용을 위해 아래와 같은 두 가지 방법을 쉽게 생각해 볼 수 있다.

##### (1)  Atlas Texture

- 아틀라스 텍스처를 만들어 대응되는 UV 좌표를 계산하는 방법
- 오래전부터 사용되던 방법으로 사용에 따른 플랫폼 간 문제가 크게 없음
- Mipmap과 엮어서 사용할 경우 Level 간의 Issue를 포함해 경계선과 Texture Bleeding  문제가 커짐

  - 별도의 Level 처리나 샘플링 등으로 어느정도 문제가 해결되지만 Mipmap의 장점을 최대화하기는 어려워보인다
  - 아래는 기본 Sampling을 통한 비교, [NoMip & Mip, Sampler - Point]
  
    - Mipmap을 쓴 경우 멀리있는 색과 타일 사이의 색이 뭉게지는 것을 볼수 있다
  

<div class='cocoen'>
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/No_mip_point.png" alt="Lazy" style="max-width: none;">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/mip_point.png" alt="Lazy" style="max-width: 100%;">
   </div>

[[Atlas Texture와 Mipmap에 관한 내용]](https://hns17.github.io/it/knowledge/02-Mipmap_Atlas/)

##### (2) Texture Array

- 분리된 텍스처를 Array 형태로 만들어 Set하는 방식

- Atlas의 번거로운 uv 계산과 Mipmap에서 발생하는 Bleeding Issue를 신경쓸 필요가 없다

- 결과적으로 해당 Texture의 index만 Setting하면 되기때문에 코드도 짧아짐

- 단점을 생각해보면
  - 우선 지원하지 않는 장비에 대해 알아봐야 하는데
    - OpenGL 기준 SM3.0에서 부분적으로 사용이 가능했고 4.0에서 부터는 제대로 기능을 지원하기 때문에 현 시대의 PC에서는 신경 쓸 필요없음
    
    - 저사양의 모바일 이나 기타 그래픽스 API가 지원하지 않는 플랫폼에서 사용할 수 없다
    
  

![image-20221209214559396](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221209214559396.png)

[https://docs.unity3d.com/kr/2019.4/Manual/class-Texture2DArray.html](https://docs.unity3d.com/kr/2019.4/Manual/class-Texture2DArray.html)

- 시트를 Texture2d로 변환하는 기능을 제공하며 시트화 하기 싫은 경우 별도의 스크립팅을 통해 텍스처를 묶어 Asset으로 만들수 있다.
  - Array화 할 Texture는 모두 통일된 유형의 Texture야 함
- 아래는 Texture2DArray를 사용해 Sampling한 결과

  - [NoMip & Mip, Sampler - Point]

    - Atlas와 달리 깔끔하게 Mipmap 효과가 적용되어 Mipmap을 사용하지 않은 것과 크게 차이나지 않는 것을 확인할 수 있다


<div class='cocoen'>
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/No_mip_point.png" alt="Lazy" style="max-width: none;">
	<img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/array2d_point.png" alt="Lazy" style="max-width: 100%;">
</div>


<p> </p>

##### (3) Greedy에서 UV 처리

- Atlas의 경우 Sheet의 Tile 시작점 + Merge 범위를 통해서 처리
- Texture2DArray는 Index 정보가 있으므로 Merge 범위가 UV Coordinate가 된다

### 3. Result

- [GreedyMeshing과 Mipmap, Sampling  - Linear]

<img src="https://raw.githubusercontent.com/hns17/ImageContainer/main/img/array2d_linear.png" alt="array2d_linear" style="zoom: 40%;" />





------

# Ref

[https://0fps.net/2012/06/30/meshing-in-a-minecraft-game/](https://0fps.net/2012/06/30/meshing-in-a-minecraft-game/)

[https://0fps.net/2013/07/09/texture-atlases-wrapping-and-mip-mapping/](https://0fps.net/2013/07/09/texture-atlases-wrapping-and-mip-mapping/)

------

