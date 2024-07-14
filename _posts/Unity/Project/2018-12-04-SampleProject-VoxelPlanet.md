---
title: "SampleProject_VoxelPlanet"
categories: [Project/Portfolio]
tag : ["Unity", "Project", "Voxel"]

---



# **VoxelPlanet**

  - 개발기간 : 2018년도 (3개월)

  - 개발환경 : Unity 2018

  - [BaseLink](https://hns17.tistory.com/entry/VoxelPlanet-Unity)

**\[소개영상\]**

<iframe src="https://www.youtube.com/embed/h5EgYjCVOAQ?rel=0" frameborder="0" allowfullscreen=""></iframe>



## 개발한 기능들

### 1\. Map Editor

-  Generator 영상 및 포스팅 : _[클릭](https://hns17.tistory.com/entry/Voxel-Planet-Generator?category=403828)_

<iframe src="https://www.youtube.com/embed/ZRG4CgVTNvI?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **2\. WorldMap / MiniMap**

   - 포트폴리오에 사용된 미니맵 월드맵 입니다.

   - 추가한 지역을 맵에 표시합니다.

<iframe src="https://www.youtube.com/embed/o2CAmzYl0tk?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **3\. day / night**

   - 태양의 위치 변화를 기반으로 한 하늘의 낮과 밤

<iframe src="https://www.youtube.com/embed/SNxFjQv0mnw?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **4\. Character Skill**

   - 플레이어 스킬과 기본 동작들

<iframe src="https://www.youtube.com/embed/rwZGoq42qrM?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **5\. 오브젝트 UI & Talk Event**

  - Object에 표시되는 UI 및 대화 이벤트

<iframe src="https://www.youtube.com/embed/zHtkNLecjNc?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **6\. Object Health & Hit**

-  Object에 체력을 부여하고 피격 UI를 표시합니다.

<iframe src="https://www.youtube.com/embed/rUQL02r4gtw?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **7\. Item Editor & Inventory**

- ItemEditor : Editor를 통해 Item 정보를 추가, 수정, 삭제하고 Prefab으로 만들어줍니다.
- Inventory : Editor에서 만들어진 아이템을 플레이어가 획득하면 보관하고 보여줍니다.

<iframe src="https://www.youtube.com/embed/B0EaCiSHz_A?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **8\. BGM & Text Effect**

- 배경음악 재생 이벤트와 텍스트 애니메이션입니다.

<iframe src="https://www.youtube.com/embed/RCBFNOV4pX8?rel=0" frameborder="0" allowfullscreen=""></iframe>

------



### **9. Particle & Animation**

 가. 오브젝트 애니메이션

\- 단순한 UI나 오브젝트 애니메이션은 ITween과 애니메이션 클립을 이용하였습니다.

\- 효과음과 같은 애니메이션 이벤트가 필요한 경우는 주로 클립을 만들어 이벤트를 이용합니다.

![img](https://t1.daumcdn.net/cfile/tistory/99D9D3425C483AED0D)

 

 나. 파티클 이펙트

- 대부분 캐릭터나 이벤트 장면의 큐브 복셀을 표현하기 위해 만들었습니다.

  

![img](https://t1.daumcdn.net/cfile/tistory/992BF1445C48543D24)

------



### **10. Shader**

 가. Terrain

- Unity의 Standard Shader에 기능을 추가한 Shader를 사용합니다.
- 해수면의 높이에 따른 빛의 감쇄를 표현합니다.
- 처음에는 Ocean Shader에서 깊이 텍스쳐 기반으로 표현하였는데 카메라 높이에 따라 표현의 밝기가 달라지는게 예쁘지 않아서 terrain vertex 위치로 조정하였습니다.

![img](https://t1.daumcdn.net/cfile/tistory/996A1B485C49070230)

 

 나. Clouds

- 물체의 내부산란을 표현하는 셰이더를 사용합니다.
- ref : *[Fast SubSurface Shader](https://www.alanzucconi.com/2017/08/30/fast-subsurface-scattering-1/)*

| [Standard]                                                   | [Emission]                                                   | [SubSurface]                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![img](https://t1.daumcdn.net/cfile/tistory/994E433A5C491AC10E) | ![img](https://t1.daumcdn.net/cfile/tistory/9981C64A5C491B0611) | ![img](https://t1.daumcdn.net/cfile/tistory/9994383C5C491B230B) |
| 아래쪽이 음영처리 된다.                                      | 음영 문제는 해결되지만 구름의 굵기등에 의한 부분적 감쇄 처리가 어렵다. | 구름의 굵기에 따라 부분적으로 빛의 감쇄가 적용되지만, 예쁜지 잘 모르겠다. |



 다. Ocean

- 빛의 굴절을 표현하기 위해 Distortion 기반의 셰이더로 작성하였습니다.
- uv scroll과 프레넬을 사용합니다.

![img](https://t1.daumcdn.net/cfile/tistory/99A4BE4E5C4906EA30)

 

 

 라. Dissolve Shader

- 숨겨진 물체의 표현에 사용합니다.

![img](https://t1.daumcdn.net/cfile/tistory/9916A44E5C483A2A36)

 

 마. 왜곡

- 빛의 굴절을 표현하기 위해 Distortion 셰이더를 사용합니다.

![img](https://t1.daumcdn.net/cfile/tistory/99FD184C5C483A112F)

 



 바. Player

- Unity StandardAsset에서 제공되는 ToonShader를 사용합니다.
- Face 음영을 넣고 싶었는데 텍스쳐 작업을 아무리 해도 안 예뻐서 그냥 렌더합니다....

![img](https://t1.daumcdn.net/cfile/tistory/99FA56505C49245119)

 

그외 셰이더는 유니티에서 제공되는 셰이더나 HDR Emission 셰이더 정도가 사용되었습니다.

 