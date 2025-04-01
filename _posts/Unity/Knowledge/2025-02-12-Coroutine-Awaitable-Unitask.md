---
title: "Coroutine vs Awaitable vs UniTask 비교"
categories: [Unity/Knowledge]
tag : ["Unity", "Script", "Unitask", "Coroutine", "Awaitable"]

---



# 🚀 **Coroutine vs Awaitable vs UniTask 비교**

Unity6(2023)에서 await/async 기능에 대응하는 Awaitable이 빌트인으로 추가되었다.

Unity에서 비동기 프로그래밍을 처리하는 세 가지 주요 방식인 **Coroutine**, **Awaitable(Unity 6)**, 그리고 **UniTask**를 비교하고 각각의 특징, 장단점을 정리했습니다.

------

## **1. Coroutine (`IEnumerator`)**

### ✅ **특징**

- Unity의 전통적인 비동기 처리 방식.
- `IEnumerator`와 `yield return`을 사용하여 프레임 단위의 실행을 제어.
- **멀티스레딩이 아닌 단순한 게임 루프 제어**(비동기 함수 실행이 아닌 **스케줄링**에 가까움).

### 🔹 **예제**

```csharp
using UnityEngine;
using System.Collections;

public class CoroutineExample : MonoBehaviour
{
    private void Start()
    {
        StartCoroutine(ExampleCoroutine());
    }

    private IEnumerator ExampleCoroutine()
    {
        Debug.Log("첫 번째 실행");
        yield return new WaitForSeconds(2); // 2초 대기
        Debug.Log("2초 후 실행");
    }
}
```

### ⚖️ **장점**

✅ **간단한 문법** → `yield return`을 사용해 직관적인 코드 작성 가능. <br>
✅ **Unity와의 완벽한 통합** → `WaitForSeconds()`, `WaitForNextFrame()` 등의 Unity API와 자연스럽게 연동됨. <br>
✅ 실행 중지 처리가 편리함 <br>

### ❌ **단점**

❌ **비동기 반환값 처리 어려움**. 반환값을 받을 수 없음.<br>
❌ **콜백 헬(Coroutine Hell)**. 중첩 사용 시 코드가 복잡해짐..<br>
❌ **다른 스레드에서 실행 불가**. Unity의 메인 스레드에서만 실행 가능..<br>
❌ Monobehaviour에 종속됨, StartCoroutine 함수가 MonoBehaviour의 멤버함수.<br>
❌ 추가적인 힙 사용, StartCoroutine, 일부 yield return 기능

------



## **2. Awaitable (Unity 6)**

### ✅ **특징**

- Unity 6에서 추가된 새로운 **비동기 API**.
- `async/await`과 함께 사용하여 **더 깔끔한 코드 작성 가능**.
- Unity의 **프레임 루프와 자연스럽게 연동**됨.
- 내부적으로 **풀링(pooling)**을 사용하여 메모리 효율성을 높임.

### 🔹 **예제**

```csharp
using UnityEngine;

public class AwaitableExample : MonoBehaviour
{
    private async void Start()
    {
        Debug.Log("작업 시작");
        await Awaitable.WaitForSecondsAsync(2.0f); // 2초 대기
        Debug.Log("2초 후 실행");
    }
}
```

### ⚖️ **장점**

✅ **`async/await` 문법 사용 가능**. 가독성이 좋고, 유지보수가 쉬움..<br>
✅ **Coroutine보다 더 직관적이고 구조적**. `async/await`을 사용하므로 비동기 흐름이 명확함..<br>

### ❌ **단점**

❌ **풀링 문제**. 동일한 `Awaitable` 인스턴스를 여러 번 `await` 하면 예상치 못한 동작이 발생할 수 있음..<br>
❌ **일부 힙 할당 가능**. 내부적으로 상태 머신이 동작..<br>
❌ **Task보다 기능이 제한적**. `Task.Delay()`와 같은 기능이 부족하며, 특정 시나리오에서는 `UniTask`보다 활용성이 낮음..<br>
❌ 취소 처리가 불편함..<br>
❌ 2023 이상 버전을 사용해야 함..<br>

------



## **3. UniTask (외부 라이브러리)**

### ✅ **특징**

- `async/await`을 지원하는 **가장 최적화된 비동기 처리 라이브러리**.
- **값 타입(value type) 기반** → `GC-Free(가비지 컬렉션 없음)`으로 실행 가능.
- 다양한 **비동기 API 지원** (`WaitForSecondsAsync()`, `WaitForNextFrameAsync()`, `CancellationToken` 등).
- Unity뿐만 아니라 **일반 C# 프로젝트에서도 사용 가능**.

### 🔹 **예제**

```csharp
using UnityEngine;
using Cysharp.Threading.Tasks;

public class UniTaskExample : MonoBehaviour
{
    private async void Start()
    {
        Debug.Log("작업 시작");
        await UniTask.Delay(2000); // 2초 대기 (GC-Free)
        Debug.Log("2초 후 실행");
    }
}
```

### ⚖️ **장점**

✅ **`async/await` 문법 지원**. `Task`와 유사하지만 더 빠르고 효율적..<br>
✅ **힙 할당 없음 (GC-Free)**. 값 타입 기반으로 동작하여 성능 최적화..<br>
✅ **다양한 유틸리티 제공**. Tracker Window, WhenAll, DoTween.<br>

### ❌ **단점**

❌ **외부 라이브러리 설치 필요**. Unity 패키지 시스템을 통해 추가해야 함..<br>
❌ **초기 학습 비용**. 기존 Coroutine이나 Awaitable보다 설정이 필요할 수 있음..<br>
❌ **취소 처리가 불편함**..<br>

------

## 🔥 **Coroutine vs Awaitable vs UniTask 비교표**

| 기능                         | Coroutine (`IEnumerator`)         | Awaitable (Unity 6) | UniTask                    |
| ---------------------------- | --------------------------------- | ------------------- | -------------------------- |
| **`async/await` 지원**       | ❌ 불가능                          | ✅ 지원              | ✅ 지원                     |
| **힙 할당 (GC 부담)**        | ⚡⚡ 실행시 발생                    | ⚡ 일부 발생         | ✅ 없음 (값 타입 기반)      |
| **Unity 프레임 루프와 통합** | ✅ 기본 제공                       | ✅ 기본 제공         | ✅ 기본 제공                |
| **비동기 반환값 처리**       | ❌ 불가능                          | ✅ 가능              | ✅ 가능                     |
| **성능 (최적화)**            | ⚡ 보통                            | 🚀 빠름              | 🚀🚀 가장 빠름 (GC-Free)     |
| **외부 라이브러리 필요**     | ❌ 없음                            | ❌ 없음              | ✅ UniTask 패키지 설치 필요 |
| **코드 가독성**              | ❌ 가독성 낮음 (콜백 헬 발생 가능) | ✅ 가독성 좋음       | ✅ 가독성 좋음              |
| **기능 확장성**              | ❌ 제한적                          | ⚡ 제한적            | ✅ 풍부한 기능 제공         |

------

## 🎯 **언제 무엇을 사용할까?**

✅ **Coroutine 사용 추천 (간단한 게임 루프 제어)**

- `yield return`을 사용한 간단한 애니메이션, 타이머, UI 애니메이션 제어 시
- Unity 기본 기능에 잘 맞음
- 단, 복잡한 비동기 로직에는 부적합

✅ **Awaitable 사용 추천 (Unity 6 이상, 간단한 `async/await` 필요 시)**

- Unity 6의 `async/await`을 활용하고 싶을 때
- Coroutine보다 더 직관적인 코드가 필요할 때
- 하지만 **같은 인스턴스를 여러 번 `await` 하면 문제가 생길 수 있음**

✅ **UniTask 사용 추천 (최고 성능 & 확장성이 필요할 때)**

- **GC-Free**가 필요할 때 (메모리 최적화가 중요한 경우)
- 멀티스레드 환경에서도 **안전하게 비동기 처리**를 해야 할 때
- `await Task.Delay()` 같은 기능이 필요할 때
- 단, **외부 라이브러리를 추가해야 함**

👉 **결론:**

- 간단한 `yield return`이 필요하면 **Coroutine**
- Unity 6에서 `async/await`이 필요하면 **Awaitable**
- 최고의 성능과 확장성을 원하면 **UniTask** 🚀

------



# Ref

------

- [https://www.unitysquare.co.kr/growwith/unityblog/webinarView?id=566](https://www.unitysquare.co.kr/growwith/unityblog/webinarView?id=566)
- [https://hns17.github.io/unity/external(asset/lib/etc)/UniTask/](https://hns17.github.io/unity/external(asset/lib/etc)/UniTask/)



