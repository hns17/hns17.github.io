---
title: "Unity Script Optimization"
categories: [Unity/Knowledge]
tag : ["Unity", "Script", "Optimization", "Performance", "Memory"]
---



# Unity Script Optimization

- 프로그래밍을 할 때 신경써야 할 것은 크게 처리 속도와 메모리 사용 두 가지로 나누어 볼 수 있다.

- 이를 바탕으로 Unity 환경에서 Script를 작성할 때 알아두면 좋은 것들을 정리해보자



# 목차

- [Performance](#performance)
  - [사용하지 않는 이벤트 함수 제거](#사용하지-않는-이벤트-함수-제거)
  - [시작 이벤트 함수에서 무거운 작업 피하기](#시작-이벤트-함수에서-무거운-작업-피하기)
  - [무거운 함수의 반복적인 사용 최소화하기](#무거운-함수의-반복적인-사용-최소화하기)
  - [Debug.Log 구문 제거](#debuglog-구문-제거)
  - [프레임 단위로 실행되는 코드 최소화](#프레임-단위로-실행되는-코드-최소화)
  - [Native 호출 최소화](#native-호출-최소화)
  - [런타임 시 컴포넌트 추가 X](#런타임-시-컴포넌트-추가-x)
  - [Transform 연산 최소화](#transform-연산-최소화)
  - [수학 연산 최적화](#수학-연산-최적화)
  - [Target Frame 지정](#target-frame-지정)
  - [For, Foreach, List, Array](#for-foreach-list-array)
- [Memory](#memory)
  - [공간복잡도 문제](#공간복잡도-문제)
  - [가비지 컬렉터 문제](#가비지-컬렉터-문제)
    - [불 필요한 힙 사용 줄이기](#1-불-필요한-힙-사용-줄이기)
    - [메모리 풀](#2-메모리-풀)
    - [가비지 컬렉터 강제 호출](#3-가비지-컬렉터-강제-호출)
- [기타](#기타)
  - [Target Frame 지정](#target-frame-지정)
  - [LINQ 사용시 주의가 필요하다](#linq-사용시-주의가-필요하다)
  - [명시적 파기가 필요한 유니티 클래스](#명시적-파기가-필요한-유니티-클래스)

<br>

# Performance

- 처리속도로 인해 신경써야 하는 것들



## 사용하지 않는 이벤트 함수 제거

- 모노비헤이비어 클래스에는 다양한 이벤트 함수가 있다.
- 함수 내 기능이 없더라도 PlayerLoop의 실행 대상이 되므로 사용하지 않는 함수는 제거해야 한다.



## 시작 이벤트 함수에서 무거운 작업 피하기

- Start, Awake, OnEnable와 같은 이벤트 함수에서 시간이 많이 소비되는 너무 무거운 작업은 피하는 것이 좋다.

- 첫 번째 프레임이 렌더링되기 전 비용이 많이 드는 로직을 수행할 경우 필요 이상으로 로딩 시간이 길어질 수 있기 때문이다.
- 무거운 작업이 필요할 경우 Non-Blocking 형태의 함수로 분할하는 것도 좋은 방법이다.
  - UniTask, Coroutine 등



## 무거운 함수의 반복적인 사용 최소화하기

- Unity의 GetComponent나 FInd 같은 무거운 함수를 반복적으로 사용하는 것은 성능상 좋지 않다.
- 대상이 고정된 값이나 레퍼런스라면 Awake나 Start 함수에서 멤버변수로 캐싱하고 함수의 반복적인 사용을 최소화한다.



## Debug.Log 구문 제거

- Log 구문, 특히 Update, LateUpdate 또는 FixedUpdate에 있는 Log 구문은 성능에 악영향을 준다.
- 빌드를 만들기 전에 Log 구문을 비활성화해야 한다.
- 아래는 define symbol을 이용해 로그를 비활성화 하는 방법을 보여준다.

![image-20230422145238304](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230422145238304.png)



## 프레임 단위로 실행되는 코드 최소화

- Update, LateUpdate, FixedUpdate와 같이 프레임 단위로 매번 실행되는 이벤트 함수의 기능을 최소화 하자
- 반복적으로 확인이 필요한 경우가 아니라면 코드를 제거하고 상황에 맞는 경우에만 실행되도록 수정한다.
  - Reactive, Observer 등의 방법을 활용하는 것도 좋은 대안이다.
- 매 프레임 연산될 필요가 없는 반복작업이 필요할 경우 Coroutine이나  UniTask등을 사용하여 고정된 인터벌을 두고 실행하여 연산횟수를 줄이는 것도 좋은 방법이다.



## 런타임 시 컴포넌트 추가 X

- AddComponent 함수는 런타임에 컴포넌트가 추가될 때마다 중복 또는 기타 필요한 컴포넌트를 확인하는 무거운 함수다.
- 컴포넌트를 미리 추가해 둔 프리팹을 인스턴스화하는 것이 일반적으로 더 효과적이다.



## Native 호출 최소화

- 유니티 내부에서 제공하는 API를 호출하거나 오브젝트에 접근 할 경우 주의가 필요하다.
- Unity 엔진의 코어는 C++ 로 작성되어 있고, C# 영역에서 Native 영역에 접근 할 경우 네이티브 호출이 발생하며 많은 비용이 발생한다.
- 또한 C#과 네이티브는 메모리를 공유하지 않기 때문에 정보를 가져올 때 C# 측에서 메모리를 추가 사용한다.
- 예를들어 GameObject.transform과 같이 Unity에서 제공하는 기능들은 접근시 c++ 영역에 접근하기 때문에 네이티브 호출이 발생하게 되며 추가적으로 메모리도 요구하기 때문에 값을 캐싱하여 반복적인 접근을 최소화 하는 것이 좋다.



## Transform 연산 최소화

- Transform 정보는 변경되면 관련된 모든 계층의 정보도 같이 변경되는 무거운 연산이 수행된다.
- 변경이 필요한 경우 변경될 데이터를 모두 계산한 후 한번에 업데이트한다.
  - 위치와 회전 변환은 SetPositionAndRotation() 함수를 이용하면 한번에 처리 가능하다.



## 수학 연산 최적화

- ### Mathf.Abs 연산은 생각보다 느리다.

  - Define함수나 삼항연산자를 이용하는 것도 좋은 방법

    

- ### Vector 연산은 Scalar 부터 연산하는게 좋다.

  ```c#
  Vector3 vec = Vector3.one;
  float scalar = 0.5f;
  float scalar2 = 0.4f;
  
  //case1
  vec = vec * scalar * scalar2;
  //vec.x * scalar, vec.y * sclar, vec.z * sclar;
  //vec.x * scalar2, vec.y * sclar2, vec.z * sclar2;
  
  //case2
  vec = vec * (scalar * scalar2);
  //_sclar = sclar * sclar2;
  //vec.x * _sclar, vec.y * _sclar, vec.z * _sclar
  
  //case2 쪽이 더 빠르다
  ```



- ### 나누기보다는 곱 연산

  - 굳이 나누기 연산을 할 필요없는 경우 곱 연산을 하는게 더 빠르다

  ```c#
  float num = 10f;
  
  num /= 2; 보다는 num *= 0.5f;를 쓰는게 좋다
  ```

  

## For, Foreach, List, Array

- 아래는 가장 흔히 사용하는 배열 형태의 자료구조를 상황에 따라 비교해서 나온 결과이다.

![image-20230423235227912](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423235227912.png)

![image-20230423233331398](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423233331398.png)



```
위 내용을 보면 배열을 사용한 반복문 처리가 더 빠르다는 것을 알 수 있다.
이는 배열의 경우 인덱스를 직접 참조하지만, 리스트는 내부적으로 인덱서를 사용하여 접근하기 때문으로 보인다.
인덱서는 프로퍼티와 유사한 형태로 호출시 인덱스 값을 직접 사용하는 배열과 달리 오버헤드가 존재한다.
따라서 성능상 민감한 부분은 List보다는 배열을 사용하는 것이 좋다.

리스트를 사용할 경우 foreach 보다는 for를 사용하는 것이 유리하다.
List의 foreach는 for와 달리 내부적으로 MoveNext() 와 Current 속성을 이용하기 때문에 여기서 오버헤드가 발생한다.
또한, for를 사용할 경우 List.Count 값을 캐싱해서 사용하여 추가적으로 성능상 이점을 얻을 수 있다.
```



<br>

# Memory

- 메모리 사용에 따라 발생하는 문제



## 공간복잡도 문제

- 공간복잡도 문제는 필요에 따라 메모리 프로파일러를 확인해가며 매번 신경써 줘야 하는 일이다.
- 스크립팅 보다는 리소스 세팅이나 번들을 얼마나 잘 분할하여 적절하게 로드 / 언로드하는가 와 같은 상황에 따라 크게 달라지므로 여기서는 관련된 내용을 제외한다.



## 가비지 컬렉터 문제

- Unity는 Boehm-Demers-Weiser 가비지 컬렉터를 사용하며, 호출되면 프로그램 코드는 실행이 중단되고 작업이 완료될 때 까지 대기한다.
- 때문에 GC가 호출될 경우 게임이 일시적으로 멈추는 프리징이 발생할 수 있고 예측 불가능한 GC의 호출은 게임의 품질을 떨어뜰이게 된다.
- 이 문제를 해결하기 위해 불필요한 힙 사용을 줄이고 예측 불가능한 GC 호출을 최소화 할 필요가 있다.
- 이를 위한 방법들을 알아보자.



### 1. 불 필요한 힙 사용 줄이기

- 불필요한 힙 사용을 최소화 하여 GC 호출 가능성을 줄인다.

  

#### 1.1 문자열 조합시 주의하기

- string은 클래스로 생성시 힙을 사용한다.
- 연산자를 통해 조합을 하게되면 string을 추가 생성하므로 StringBuilder의 Append함수를 사용하도록 한다.



#### 1.2 힙을 생성하는 함수 호출에 주의하기

- 유니티나 기타 라이브러리의 API 중 호출 시 힙을 생성하는 경우가 많으므로 주의가 필요하다.
  - GetComponent, StartCoroutine, DoTween 등 반환 값이 class 형태로 이루어진 함수들



#### 1.3 박싱과 언박싱

- 박싱을 하게되면 높은 확률로 언박싱 될 가능성이 크며, 속도도 느림
- 추가적으로 메모리를 사용하게 됨



#### 1.4 코루틴

- 시작함수가 힙을 생성하기 때문에 StartCoroutine을 반복적으로 사용할 시 주의

  - Unitask, Unirx을 사용한다면 관련 API를 사용하는 것도 좋은 방법

- yield return 의 종류에 따라 힙을 생성하므로 캐싱해서 사용



#### 1.5 오브젝트 풀

- 많은 오브젝트를 반복적으로 생성하고 삭제해야 할 경우 풀링을 통해 재활용

- 힙 사용을 줄일 뿐만아니라 생성 및 삭제에 대한 오버헤드도 줄일수 있다.



#### 1.6 컬렉션 재활용

- c#에서 제공되는 대부분의 자료 구조는 클래스로 힙 사용
- 멤버로 만들고 필요할때 마다 Clear 함수를 이용해 재사용하면 추가적인 힙 사용을 줄일수 있다.
- 유니티 2021 이후 버전인 경우 Span을 지원하기 때문에 stackalloc으로 스택 영역을 사용하거나 Collection Pool을 이용하는 것도 좋은 방법



#### 1.7 구조체 사용하기

- 구조체는 힙이 아닌 스택을 사용하는 데이터 타입이기 때문에 반복적으로 사용되는 객체가 필요하다면 구조체를 사용하는 것도 좋은 방법이다.
- 단, 레퍼런스 타입의 멤버 변수나 박싱 등을 신경써서 사용해야 의미가 있다.
- 특히나 제너릭과 인터페이스를 사용할 경우 암묵적으로 캐스팅이 일어나지 않도록 where 구문 (generic type constraint)을 사용하여 T 이 받아들일 수 있는 타입을 제한해 주면 이러한 예기치 못한 박스화를 방지할 수 있습니다.
- 아래는 이와 같은 예이다.

![image-20230423142302817](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423142302817.png)



#### 1.8 Native 영역 접근하는 프로퍼티나 API 주의하기

- Unity 에서는 스크립트를 C#으로 구현하지만, Unity 자체는 C++ 로 구현되어 있다. 
- C# 메모리 공간과 C++ 메모리 공간은 서로 공유되지 않기 때문에 C++ 측에서 C# 측으로 정보를 전달하기 위해 추가적으로 필요한 메모리 확보가 이루어지며 이때 GC.Alloc 이 발생하게 된다.

- 가장 대표적인 문제로 문자열 정보에 접근하는 것으로 이때 전달하기 위해 문자열을 추가적으로 생성하게 된다.

- 이러한 문제는 호출할 때마다 발생하게 되므로 여러번 접근하는 경우 캐싱하여 사용해야 한다.
- 아래는 UnityEngine.Object 를 상속받은 클래스의 tag 프로퍼티와 name 프로퍼티에 대한 내용이다.
  - 둘다 Native 호출을 사용하는 것을 알 수 있다.

![image-20230422163107453](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230422163107453.png)



#### 1.9 ScriptableObject

- 외부 파일을 통해 사용될 정보를 로드하는 경우 이를 변환하는과정에서 다량의 힙이 사용될 수 있다.
- 이를 방지하기 위해 외부 파일을 런타임에서 바로 로드하기 보다는 ScriptableObject 파일로 변환한 후 런타임에서 로드하는 것이 좋다.
  - 필요하다면 스크립터블 오브젝트 데이터를 만드는 커스텀 에디터 기능을 만들어 사용하는 것도 좋은 방법이다.



#### 1.10 람다 사용시 주의하기

- 람다식도 유용한 기능이지만 사용법에 따라 GC.Alloc 이 발생하기 때문에 주의가 필요하다.

##### [람다식에서 외부변수를 사용하는 경우]

![image-20230423220519479](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423220519479.png)

```
위 코드를 보게되면 람다식 내부에서 멤버변수나 클로저(상위의 지역변수를 사용하는 람다식)를 사용할 경우 힙을 사용한다.
람다식 외부 변수를 사용하게되면 변수에 접근하기 위해 C#은 내부적으로 변수를 멤버로 가지는 임시 클래스를 자동으로 생성하기 때문에
매 프레임 실행되거나 성능이 중요한 코드라면 사용을 피해야 합니다.

스태틱 변수의 경우 추가적인 임시 클래스를 생성하지 않는다.
```



##### [람다식 내에서 함수를 호출하는 경우]

![image-20230423221247217](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423221247217.png)

```
람다식 내에서 외부 함수를 호출하는 경우에도 동일한 문제가 보인다.
다만 스태틱 함수를 지정하지 않고 내부에서 직접 호출하는 경우는 추가적인 힙을 사용하지 않는 것으로 보인다.
```



### 2. 메모리 풀

- 많은 량의 힙 공간을 미리 할당하여 사용가능한 힙공간을 크게 늘려 GC 호출 가능성을 줄인다.
- 아래는 유니티 문서에서 안내하고 있는 내용이다.
- [https://docs.unity3d.com/kr/2018.4/Manual/UnderstandingAutomaticMemoryManagement.html](https://docs.unity3d.com/kr/2018.4/Manual/UnderstandingAutomaticMemoryManagement.html)

![image-20230422164340785](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230422164340785.png)



### 3. 가비지 컬렉터 강제 호출

- GC 에 크게 영향을 받지 않는 구간에서 강제로 호출하여, 예측 불가능한 호출을 줄이고 직접 관리한다.

- 아래는 유니티 문서에서 안내하고 있는 내용이다.

  - 30프레임 단위로 한번씩 GC를 강제로 호출하고 있다.

  - [https://docs.unity3d.com/kr/2018.4/Manual/UnderstandingAutomaticMemoryManagement.html](https://docs.unity3d.com/kr/2018.4/Manual/UnderstandingAutomaticMemoryManagement.html)

![image-20230422164545244](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230422164545244.png)

<br>

# 기타

## Target Frame 지정

- 프레임을 제한하는 것은 발열 및 배터리 문제로 인해 발생하는 쓰로틀링을 줄이는 가장 강력한 해결법
- 필요 이상의 프레임을 사용하지 않도록 하는게 좋다



## LINQ 사용시 주의가 필요하다

- 아래는 마이크로 소프트에서 제공하는 Unity 가이드 문서의 일부이다.

![image-20230423222335337](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423222335337.png)



#### [LINQ는 충분히 느리다]

- 아래는 LINQ와 배열의 성능 테스트 결과이다.
- LINQ를 사용할 경우 코드가 간결해지는 장점이 있지만 성능상 문제가 될수 있다.

![image-20230423222035310](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423222035310.png)



#### [LINQ는 반복적으로 힙을 사용한다]

- LINQ는 느릴 뿐만 아니라 반복적인 힙 사용의 대상이 된다.

- 따라서 가급적으로 LINQ 사용을 피해야 한다.

  ```
  LINQ 사용으로 인한 GC.Alloc의 원인 중 하나는 LINQ 의 내부 구현이다. 
  LINQ의 메서드들은 IEnumerable를 받아 IEnumerable을 반환하는 경우가 많다.
  
  이때 LINQ는 내부적으로 IEnumerable를 구현한 클래스를 인스턴스화하고, 
  루프 처리를 구현하기 위해 GetEnumerator()의 호출 등이 이루어지기 때문에 내부적으로 GC.Alloc 이 발생하게 됩니다.
  ```



##  명시적 파기가 필요한 유니티 클래스

- 유니티에서 제공되는 일부 클래스는 명시적으로 파기하지 않으면 해제되지 않는다.

![image-20230423152015248](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230423152015248.png)



<br>

# Ref

- [https://unitysquare.co.kr/growwith/resource/form?id=154](https://unitysquare.co.kr/growwith/resource/form?id=154)
- [https://github.com/CyberAgentGameEntertainment/UnityPerformanceTuningBible/issues/35](https://github.com/CyberAgentGameEntertainment/UnityPerformanceTuningBible/issues/35)
- [https://learn.microsoft.com/ko-kr/windows/mixed-reality/develop/unity/performance-recommendations-for-unity?tabs=openxr](https://learn.microsoft.com/ko-kr/windows/mixed-reality/develop/unity/performance-recommendations-for-unity?tabs=openxr)

- [https://docs.unity3d.com/kr/2018.4/Manual/UnderstandingAutomaticMemoryManagement.html](https://docs.unity3d.com/kr/2018.4/Manual/UnderstandingAutomaticMemoryManagement.html)
