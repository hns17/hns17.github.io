title: "UI Toolkit"
categories: [Unity/SupportFeatures]
tags: ["Unity", "UI Element", "UI Toolkit", "VisualElement",]



# UI Toolkit

## 소개

- 2019 년도인가 Unity에서 공개한 새로운 UI 개발 기능
- 초기에는 UI Element로 소개되었는데 최근 버전의 문서에는 해당 명칭 보다는 UI Toolkit이란 용어로 관련된 내용이 작성되고 있다.
  - 사실 내부 요소인 VisualElement와 이름이 비슷해서 구분하기 힘든면도 있었다
  - 또한 UI Element와  UIToolkit을 분리하는 경계가 애매하기도 했다
- 초기 공식문서 내용을 보면 핵심은 IMGUI를 대체 하기위한 새로운 UI 개발 툴이었다.
-  현재에 와서는 분리되어 있는 기존의 UI개발 기능 UGUI(Runtime), IMGUI(Editor)를 통합하여 UIToolkit이라는 하나의 툴로 대체 하는게 목적으로 보인다.

- 아래는 초기 [Unity 2018 문서 내용](https://docs.unity3d.com/kr/2018.4/Manual/UIElements.html)

![image-20230106151413118](C:\Users\hns17\AppData\Roaming\Typora\typora-user-images\image-20230106151413118.png)



## 구성

- UI Element는 새롭게 추가된 UI 개발 기능을 말한다
  - UI 개발 편의를 위해 UIToolkit 기능을 제공한다
  - 기존의 C# 코드를 목적에 맞게 UXML, USS, C# 파일 세 가지로 분리함
  - VisualElement를 기반으로 구성된다

### 1. Visual Tree

- UI Element의 구성은 VisualElement를 Tree 형태로 구성함

  ![image-20230106161927106](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106161927106.png)



#### (1) Visual Element

- VisualElement는 UI 컨트롤의 가장 기본이되는 클래스
- 제공되는 컨트롤 대부분이 VisualElement의 파생 클래스라 생각하면 된다
- 프로그래머 입장에서 보면 핵심은 VisualElement이며, 나머지 툴킷 기능이나 파일들은 VisualElement를 표현하기 위한 도구로 볼 수 있다
- VisualElement는 Sytle, Layout, EventHandler와 같은 Property를 가진다![image-20230106162051212](C:\Users\hns17\AppData\Roaming\Typora\typora-user-images\image-20230106162051212.png)



#### (2) Drawing Order

![image-20230106162204469](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106162204469.png)



### 2. 파일 구성

- 목적에 맞게 파일을 분리해서 개발 할 수 있게 되었다

  

#### (1) UXML

- UI 화면 설계와 관련된 UI 컨트롤의 생성과 관련된 정보를 담고 있다
- XML 형태이지만 이걸 손으로 직접 작성하는 사람이 있을까 싶고, 보통은 UI Builder라는 UI Toolkit 기능을 이용해 UI 컨트롤 배치 작업을 한다
  - 이제 코드가 아닌 빌더를 통해 시작적 작업이 가능해 졌다
- UI Builder로 작업한 내용을 저장한 파일이라고 볼 수 있다



#### (2) USS

- VisualElement용 Style Sheet로 css 파일과 거의 동일하다.
- UIBuilder에 제공되지 않거나 Uxml에 담기 어려운 컨트롤의 속성 값 등을 지정 할 수 있다



#### (3) C#

- UI Control의 기능을 구현



### 3. UI Toolkit

- UI 개발용 편의 기능을 제공

  

#### (1) UI Builder

- 시각적 편집 기능을 제공하는 UI 편집 툴이다.
- 작업 내용은 uxml 파일과 uss 파일로 저장된다.

![image-20230106164319132](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106164319132.png)



#### (2) UI Debugger

- 대상이되는 UI의 구성을 Tree 형태로 확인 할 수 있다.
- 컨트롤의 현재 속성 값을 확인 할 수 있고 속성 값을 변경하여 변경된 상태를 확인할 수 있다.
  - 변경 값이 적용되는 건 아님

![UIDebugger](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/UIDebugger.gif)



#### (3) Event Debugger

- VisualElement에서 일어나는 Event를 Log 형태로 볼 수 있다
- 선택하면 시각적으로 해당 컨트롤을 시각적으로 알려주고 필터링 기능도 제공해서 특정 이벤트만 확인하는 것도 가능

![image-20230106163453250](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106163453250.png)



#### (4) Sample

- 컨트롤 사용과 관련된 샘플과 코드를 볼 수 있다.

- 이 글 쓰면서 첨 알았다.
- 공식 문서보다 이쪽이 더 좋아보인다...

![image-20230106163013089](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106163013089.png)





## 이전의 기능들과 비교

- 사용 목적에 따라 이전의 기능과 비교를 해보자

- 아래는 [2021.3 문서에 제공되는 UI 개발 지침서](https://docs.unity3d.com/kr/2021.3/Manual/UI-system-compare.html) 내용이다



##### [사용 범위]

![image-20230106175650400](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106175650400.png)

```
UGUI, IMGUI와 달리 UIToolkit은 Editor와 Runtime 구분없이 사용가능하다.
IMGUI가 런타임에서 사용 가능했었나??
```



##### [기술 역량]

![image-20230106175712996](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106175712996.png)

```
각 포지션에 따른 기술 안내인데 프로그래머는 사실 신경 쓸 필요없을 테고 UI 작업을 하는 아티스트 관점에서 생각해 볼 필요가 있다
UI Toolkit을 사용할 경우 UI 아티스트 또한 툴킷의 빌더 기능을 사용해야하니 제대로된 학습이 필요하다.
에디터 작업을 놓고 보면 프로그래머의 작업이 다른 파트로 분산되는게 장점이 될 수 있다
```



### 1. Runtime(UGUI) 비교

#### (1) 장점

- ... 모르겠다. UGUI를 대체할 장점을 찾기 어렵다.
- 성능과 에디터 UI와 통합된 관리 정도가 떠오르는데 어디까지나 프로그래머 관점에서의 장점이지 이걸 가지고 UI 아티스트를 설득해서 사용을 권할 수 없다

#### (2) 단점

- 불편하다. 그냥 불편하다

  - UI Builder를 통한 시각적 배치 및 설계가 가능하지만 그건 어디까지나 IMGUI와 비교했을때 장점일 뿐 인스펙터와 에디터 뷰를 통해 작업하던 UGUI 관점에서는 전혀 장점이 되지 못함. 오히려 UIBuilder 보다 UGUI가 훨씬 편하다.

- UI를 구성하는 스타일과 관련된 스타일 시트 작성 역량이 요구된다

  - UI Builder에서 제공되는 기본 속성만으로는 한계가 있기 때문에 USS 작성이 요구됨
    - 그런데 이 USS 작성이 쉽지가 않다.
    - *~~공식 문서의 빈약함으로 속성들의 field name을 알기도 어렵고 Selector에 대한 설명도 부족하다~~*
      - 최근 문서를 확인해보니 이전과 달리 상당히 개선되어 있다. 샘플 코드도 추가되었으면 좋겠다.
    - 관련 문서도 많지않아서 아티스트에게 강요할 내용이 아니다

- 제공되는 컨트롤 제한

  - 런타임용 컨트롤과 에디터에서만 사용 가능한 컨트롤이 구분되어 있는데 확장용 컨트롤 대부분이 에디터용이다
  - 유니티 에디터용이 아닌 빌드용 에디터 개발에 써볼까 했지만 쓸 만한 기능이 전부 확장용 컨트롤이라...

- 커스텀 마테리얼과 마스킹 사용불가

  - 아래는 2021.3 기준 렌더링 지원에 대한 비교
  - UI Toolkit은 커스텀 마테리얼을 사용하지 못하며, 마스킹 기능도 부분적으로만 사용 가능하다
    - 이후 기능이 추가되면 몰라도 다양한 표현을 요구하는 게임에서는 고려 대상이 될 수 없다

  ![image-20230106181831320](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106181831320.png)

- 기타

  - 커스텀 기능이다 그 외에도 DoTween과 같은 Asset 활용 등을 고려하면 현 시점에서는 장점 보다는 단점만 산더미

  ![image-20230106182239356](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230106182239356.png)



### 2. Editor(IMGUI) 비교

### (1) 장점

- UI Builder의 제공
  - UI Builder를 통해 시각적으로 컨트롤 배치와 화면 구성이 가능해졌다.
  - 기존 에디터 툴 작업을 고려하면 굉장히 많은 시간 단축을 가져다 준다

- 파일의 분할

  - 기존과 달리 UXML, USS, C#으로 역할이 분할되었다
  - 덕분에 C# 영역에서는 기능 구현만 신경쓸 수 있게 되었다
  - 또한 컨트롤 스타일과 배치 등이 uxml, uss파일로 분리되어 c# 코드 수정에 대한 컴파일을 신경쓸 필요가 없어졌다
    - 기존의 Immediate Mode 작업과 비교하면 많은 시간 단축을 가져옴

- IMGUI Container 제공

  - 기존의 IMGUI를 보여주는 VisualElement를 제공
  - IMGUI와 혼합해서 에디터 제작이 가능하다 

- UI Debugger 제공

  - 제작된 UI의 Visual Tree를 볼 수있으며, 셋팅된 속성 및 스타일 시트 등의 현재 상태를 확인할 수 있다.
  - 디버거 상 속성 값을 수정하면 수정된 값이 반영된 UI를 바로 확인 할 수 있다.
  - 커스텀한 UI 뿐만 아니라 기존의 Unity에서 작업된 UI들의 VisualTree도 확인할 수 있다.
    - 이는 에디터 툴 개발에 상당히 참고가 됨

- 기타 편의성 툴

  - Event Debugger를 통해 UI 에서 일어나는 Event를 확인할 수 있다

  - Sample Window를 통해 UI 종류와 샘플 코드 또한 확인이 가능하다

    

### (2) 단점

- 단점이 있나??
- 굳이 찾아본다면 만들어진지 오래된 IMGUI와 비교하면 관련 문서가 적다
- 또한 AssetStore의 Asset들 대부분이 IMGUI로 구성되어 있다
  - VIsualElement를 사용한다고 IMGUI를 사용하지 못하는건 아니라서 크게 문제가 되지 않음
  - 또한 IMGUI Container를 사용해 확장도 가능.



# 결론

- 단순하고 간단한 UI 표현용 프로젝트가 아니라면 출시용으로 사용하기는 어렵다.
- 에디터 개발용으로는 IMGUI를 훌륭히 대체 했다고 보며, 사용하지 않을 이유가 없다



# Ref

- [https://docs.unity3d.com/kr/2021.3/Manual/UI-system-compare.html](https://docs.unity3d.com/kr/2021.3/Manual/UI-system-compare.html)