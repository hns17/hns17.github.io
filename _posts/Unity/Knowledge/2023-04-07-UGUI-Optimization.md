---
title: "UGUI Optimization"
categories: [Unity/Knowledge]
tag : ["Unity", "UGUI", "Optimization", "Canvas", "UI"]

---



# UGUI Optimization [작성중]

- UI는 게임의 필수 요소이며 특히 모바일에서 많은 부분을 차지한다.
- UGUI Canvas의 최적화에 관련된 내용을 정리해보자

<br>

# 목차

- [1. Canvas 나누기](#canvas-나누기)
- [2. UI 비활성화 하기](#ui-비활성화-하기)
- [3. Graphic Raycaster](#graphic-raycaster)
- [4. RaycastTarget](#raycasttarget)
- [5. LayoutGroup](#rayoutgroup)
- [6. Object Pool](#object-pool)
- [7. Canvas RenderMode](#canvas-rendermode)
- [8. z값 통일하기](#z값-통일하기)
- [9. 스프라이트 아틀라스](#스프라이트-아틀라스)
- [10. Animator를 트윈으로](#animator를-트윈으로)



## Canvas 나누기

- UGUI의 Canvas는 변경된 요소가 하나라도 있으면 전체 요소를 업데이트 한다. 
- 많은 요소로 구성된 Canvas에서는 굉장히 부담스러운 작업이므로 자주 변경되는 요소와 정적인 요소를 분리하여 별도의 Canvas로 관리하는게 도움이 된다.



## UI 비활성화 하기

- 화면상에 표시되지 않는 요소는 비활성화하여 렌더링 및 연산에서 제외시키고 필요할때 다시 활성화 하자



## Graphic Raycaster

- GraphicRaycaster 컴포넌트는 화면의 각 입력 지점을 순환하며 입력 지점이 UI의 RectTransform 내에 있는지 확인한다.
- 화면 터치나 클릭과 같은 입력 이벤트 확인에 사용되는 컴포넌트
- 보통 최상위인 Canvas 오브젝트에 추가되어 있는데, 이를 제거하고 상호작용 이벤트가 필요한 요소를 그룹화 하거나 개별요소에 부착하자



## RaycastTarget

- 특정 UI 요소에는 RaycastTarget 속성이 존재한다.
- 상호작용이 필요하지 않은 요소라면 해제하도록 하자



## LayoutGroup

- LayoutGroup 은 상당히 무거운 작업을 수행한다.
- 가급적 사용을 피하고, 사용할 경우 UI 활성화시 사용하고 설정이 끝나면 비활성화하도록 하자



## Object Pool

- 많은 요소를 가질 수 있는 ListView나 Scroll 형태의 UI에서는 요소들을 풀링하여 화면에 보이는 만큼만 생성하고 재활용하자



## Canvas RenderMode

- Event 또는 Render Camera 필드를 공백으로 두면 Unity가 자동으로 Camera.main을 채워 넣어 불필요한 리소스가 소모됩니다.
- 가능한 경우 Canvas의 RenderMode에 카메라가 필요 없는 Screen Space – Overlay를 사용하는 것이 좋습니다.



## Z값 통일하기

- RectTransform의 z 값이 다른 경우 배칭이 깨지므로 통일해주세요



## 스프라이트 아틀라스

- UI 이미지 또한 시트로 묶어 관리하면 드로우 콜을 크게 줄일수 있습니다.



## Animator를 트윈으로

- UI의 동적인 표현을 위해 Animator 보다는 트윈 기능을 사용합시다.
- 트윈을 사용하면 애니메이터 파일의 증가를 막을 수 있으며 반복되는 업데이트 또한 줄일 수 있습니다.

<br>

# Ref

[https://unitysquare.co.kr/growwith/resource/form?id=154](https://unitysquare.co.kr/growwith/resource/form?id=154)