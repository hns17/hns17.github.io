---
title: "UGUI Optimization"
categories: [Unity/Knowledge]
tag : ["Unity", "UGUI", "Optimization", "Canvas", "UI"]

---



# UGUI Optimization

- UI는 게임의 필수 요소이며 특히 모바일에서 많은 부분을 차지한다.
- UGUI Canvas의 최적화에 관련된 내용을 정리해보자

<br>

# 목차

- [1. Canvas 나누기](#canvas-나누기)
- [2. UI 활성화/비활성화 주의하기](#ui-활성화와-비활성화-주의하기)
- [3. Graphic Raycaster](#graphic-raycaster)
- [4. RaycastTarget](#raycasttarget)
- [5. LayoutGroup](#layoutgroup)
- [6. Object Pool](#object-pool)
- [7. Canvas RenderMode](#canvas-rendermode)
- [8. UGUI 렌더링과 최적화](#ugui-렌더링과-최적화)
- [9. 스프라이트 아틀라스](#스프라이트-아틀라스)
- [10. Animator를 트윈으로](#animator를-트윈으로)
- [11. PixelPerfect 비활성화](#pixelperfect-비활성화)
- [12. Mask 사용 최소화](#mask-사용-최소화)



## Canvas 나누기

- UGUI의 Canvas는 변경된 요소가 하나라도 있으면 전체 요소를 업데이트 한다. 

  - 이동, 크기, 회전, 애니메이션, 이미지 변경, 활성화 등 

- 많은 요소로 구성된 Canvas에서는 굉장히 부담스러운 작업이므로 자주 변경되는 요소와 정적인 요소를 분리하여 별도의 Canvas로 관리하는게 도움이 된다.

  - Canvas 단위로 ReBuild 처리하기 때문에 자식 캔버스의 요소가 변경되어도 부모 캔버스 요소는 Rebuild 되지 않는다.

  - 다만 요소의 활성화/비활성화 시에는 전체가 Rebuild되는 것 같으므로 주의가 필요하다.

    - [UnityPerformanceTuningBible_KR - UI_Sector](https://github.com/CyberAgentGameEntertainment/UnityPerformanceTuningBible/issues/35)

    ![image-20230416123947860](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230416123947860.png)

- 단, Canvas 단위로 렌더링하기 때문에 배칭이 조금 늘어난다.



## UI 활성화와 비활성화 주의하기

- 화면상에 표시되지 않는 요소를 비활성화하여 렌더링 및 연산에서 제외시키고 필요할때 다시 활성화 하는 것이 최적화에 도움이 될지도 모른다. 

- 하지만 UGUI에서는 전체 캔버스가 Rebuild 되므로 순간적으로 훨씬 많은 연산이 요구될 수 있다.

- 아래는 사용하지 않는 요소에 대해 각 상황별로 처리시간을 측정한 표이다.

  - [UnityPerformanceTuningBible_KR - UI_Sector](https://github.com/CyberAgentGameEntertainment/UnityPerformanceTuningBible/issues/35)

  ![image-20230416124655011](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230416124655011.png)

```
SetActive : 필요없는 요소를 컨트롤 단위로 처리 한 경우
Canvas : Canvas로 그룹화 한 후 Canvas 단위로 처리한 경우
CanvasGroup : 활성화/비활성화 하지 않고, 알파값만 변경한 경우

Canvas Group 컴포넌트를 통해 알파값으로 투명화 시킨 경우가 훨씬 빠르다.
다만 이 경우 컨트롤의 붙어 있는 컴포넌트 연산은 그대 수행되므로 이점을 고려해서 작업할 필요가 있다.
```



## Graphic Raycaster

![image-20230416144902478](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230416144902478.png)

- 화면 터치나 클릭과 같은 입력 이벤트 발생에 사용되는 컴포넌트

- GraphicRaycaster 컴포넌트는 입력이 발생하면 화면의 각 입력 지점을 순환하며 입력 지점이 UI의 RectTransform 내에 있는지 확인한다.
  - 범위내 있는 모든 컨트롤에 이벤트를 전달한다.



#### [그룹화 또는 개별 사용하기]

- 보통 최상위인 Canvas 오브젝트에 추가되어 있는데, 이를 제거하고 상호작용 이벤트가 필요한 요소만 그룹화 하거나 개별로 부착하여 사용하자



#### [Ignore Reversed Graphics 비활성화]

- Ignore Reversed Graphics는 뒷면에 충돌 처리를 할지 여부를 판단한다. 
- 일반적인 경우 사용되지 않으니 비활성화하는 것이 좋다



## RaycastTarget

![image-20230416125653063](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230416125653063.png)

- Image와 RawImage의 베이스 클래스인 Graphic에는 Raycast Target 이라는 프로퍼티 가 있다.
- RaycastTarget은 컨트롤과 상호작용을 하기 위한 요소로 Graphic Raycaster 이벤트에 수신 여부를 결정한다.
  - 이 속성이 활성화된 컨트롤은  Graphic Raycaster 이벤트를 받는다.
- 이 속성값은 기본적으로 활성화 되어 있으므로, 상호작용이 필요하지 않은 요소라면 해제하는 것이 성능향상에 도움이 된다.
  - 상당수의 컨트롤은 상호작용이 필요하지 않다.



## LayoutGroup

- UGUI에는 요소의 변화를 감지하고 정렬해주는 LayoutGroup 컴포넌트가 있다.

- LayoutGroup과 관련된 컴포넌트는 상당히 무거운 작업을 수행한다.
- 가급적 사용을 피하고, 사용이 필요할 경우 UI 활성화시 사용하고 설정이 끝나면 비활성화하도록 하자
  - 중첩되어 사용되는 경우 특히 무거워 지므로 중첩하여 사용하지 않아야한다.



## Object Pool

- 많은 요소를 가질 수 있는 ListView나 Scroll 형태의 UI에서는 요소들을 풀링하여 화면에 보이는 만큼만 생성하고 재활용하자



## Canvas RenderMode

- Event 또는 Render Camera 필드를 공백으로 두면 Unity가 자동으로 Camera.main을 채워 넣어 불필요한 리소스가 소모된다.
- 가능한 경우 Canvas의 RenderMode에 카메라가 필요 없는 Screen Space – Overlay를 사용하는 것이 좋다.



## UGUI 렌더링과 최적화

- UGUI는 오브젝트를 렌더링 할때 한번에 그릴 수 있는 요소는 모아서 한번에 그린다.

- 아래를 보자

  #### [Case_0]

![image-20230416175849830](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230416175849830.png)

![Overdraw_0](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Overdraw_0.gif)

```
위 화면을 보면 동일한 버튼이 4개 있다.
Batch 1~3의 내용을 보면 동일한 오브젝트를 모아 한번에 그리는 것을 확인할 수 있다.
```



### [오버드로우]

- UI 요소는 오버드로우될 경우 상황에 따라 배치 카운트가 증가한다.

- 아래는 렌더링 순서에 따라 오버드로우로 인해 달라진 배치 카운트의 예이다.

  #### [Case_1]

![image-20230416180238435](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230416180238435.png)

![Overdraw_1](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Overdraw_1.gif)

```
앞서 보여준 Case_0과 Case_1의 차이는 버튼 1~3과 겹치는 투명 이미지를 그리는 순서이다.

Case_0은 버튼이 그려지고 투명 이미지를 그린다.
Batch 1~3의 내용을 보면 동일한 오브젝트를 한번에 그리는 것이 보인다.

Case_1은 투명 이미지를 그리고 버튼을 그린다.
겹치는 버튼과 겹치지 않는 버튼이 분리되어 따로 그려지는 것을 볼 수 있다.
```



### [Z값 문제]

- RectTransform의 z 값이 0이 아닌 경우 배칭이 틀어져 카운트가 증가 또는 감소하게 된다.

  - UGUI는 z값이 0인 요소들을 대상으로 한번에 그릴 수 있는 요소는 통합하여 한번에 그리는 것으로 보인다.

- z값을 0으로 통일하는 것이 항상 최선은 아니지만 특수한 경우를 제외한 대부분의 경우 z 값을 0으로 통일하는 것이 좋다.

- 아래는 z값으로 인해 배치 카운트가 감소하는 경우와 증가하는 경우의 간단한 예를 테스트해 본 결과이다.

  - 배치가 증가하는 경우

    ![Overdraw_2](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Overdraw_2.gif)

    ```
    위는 Case_0에서 버튼 요소의 z 위치 값을 1로 변경한 결과이다. 
    z 값이 변경되면서 버튼의 모든 요소가 개별로 그려지고 있다.
    z 값이 동일하더라도 0이 아니면 개별 요소로 그린다.
    ```

  - 감소하는 경우

    ![Overdraw_3](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Overdraw_3.gif)

    ```
    위는 Case_1에서 투명 이미지의 z값을 변경한 결과이다.
    Case_1에서 오버드로우로 인해 늘어난 배치 카운트가 줄었다.
    투명 이미지가 버튼 요소 렌더링하는 패스에서 완전히 분리되어 처리된 것으로 보인다.
    ```



## 스프라이트 아틀라스

- UI 이미지 또한 시트로 묶어 관리하면 배치 카운트를 크게 줄일수 있다.



## Animator를 트윈으로

- UI의 동적인 표현을 위해 Animator 보다는 트윈 기능을 사용합시다.
- 트윈을 사용하면 애니메이터 파일의 증가를 막을 수 있으며 반복되는 업데이트 또한 줄일 수 있다.



## PixelPerfect 비활성화

- UI의 PixelPerfect는 굉장히 무거운 작업이므로 가능하면 사용하지 않는게 좋다.
- 사용이 필요하다면 과도하게 연산되지 않도록 동적일때 꺼주고 다시 활성화 하거나 필요한 UI만 별도의 Canvas로 분리하는게 좋습니다.
  -  Canvas 분리시 상위 Canvas의 PixelPerfect 상속 옵션 비활성화 필요



## Mask 사용 최소화

- UGUI에는 마스킹 기능을 위해 Mask와 RectMask2d 컴포넌트를 제공한다.

- 가급적이면 마스크 사용을 최소화하고 사용이 필요할 경우 가능하다면 Mask보다는 RectMask2d를 사용하자.

- 아래는 Mask와 RectMask의 차이점

  ```
  [Mask]
  스텐실을 이용해 마스크를 구현하기 때문에 컴포넌트가 늘어날 때마다 드로잉 비용이 증가한다.
  별도의 마스크 이미지가 필요하며 원하는 형태로 마스킹 작업이 가능하다.
  
  [RectMask2d]
  셰이더의 파라미터로 마스크를 구현하기 때문에 별도의 마스크 이미지가 필요없으며 드로잉 비용의 증가를 억제할 수 있다.
  RectMask2d는 직사각형으로만 속을 비울 수 있다.
  ```

  

<br>

# Ref

- [https://unitysquare.co.kr/growwith/resource/form?id=154](https://unitysquare.co.kr/growwith/resource/form?id=154)
- [https://github.com/CyberAgentGameEntertainment/UnityPerformanceTuningBible/issues/35](https://github.com/CyberAgentGameEntertainment/UnityPerformanceTuningBible/issues/35)