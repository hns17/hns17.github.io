---
title: "Coroutine vs Awaitable vs UniTask 비교"
categories: [Unity/Knowledge]
tags: ["Unity", "Script", "Unitask", "Coroutine", "Awaitable"]

---

> 핵심 요약
> - 간단한 흐름 제어는 `Coroutine`이 가장 가볍다.
> - Unity 기본 `async/await` 흐름이 필요하면 `Awaitable`이 자연스럽다.
> - 성능과 확장성이 중요하면 `UniTask`가 가장 유리하다.

Unity에서는 비동기 흐름을 처리하는 방식이 하나만 있는 게 아니다. `Coroutine`, `Awaitable`, `UniTask`는 모두 비슷한 문제를 해결하지만, 쓰임새와 비용이 다르다. 이 글은 세 방식을 "무엇을 할 수 있는가"보다 "언제 무엇을 선택해야 하는가"에 맞춰 정리한다.

## 한눈에 비교

| 항목 | Coroutine | Awaitable | UniTask |
| --- | --- | --- | --- |
| 기본 방식 | 🔁 `IEnumerator` + `yield return` | 🧩 Unity 내장 `async/await` | 📦 외부 라이브러리 기반 `async/await` |
| 반환값 처리 | ⚠️ 어려움 | ✅ 가능 | ✅ 가능 |
| 힙 할당 | ⚠️ 상황에 따라 발생 | ⚠️ 일부 발생 가능 | ✅ 매우 적음 |
| Unity 통합 | ✅ 매우 좋음 | ✅ 좋음 | ✅ 좋음 |
| 학습 비용 | ✅ 낮음 | ✅ 낮음 | ⚠️ 중간 |
| 확장성 | ⚠️ 제한적 | ⚠️ 중간 | 🚀 높음 |

가장 중요한 차이는 문법보다도 "성능과 유지보수에서 무엇을 우선할 것인가"에 있다.

## Coroutine

### 특징

- Unity에서 가장 오래된 비동기 흐름 제어 방식이다.
- `yield return`으로 프레임 단위 흐름을 제어한다.
- 엄밀히 말해 멀티스레드 비동기라기보다 게임 루프 기반 스케줄링에 가깝다.

### 예제

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
        yield return new WaitForSeconds(2);
        Debug.Log("2초 후 실행");
    }
}
```

### 장점

- 문법이 단순하다.
- `WaitForSeconds`, `WaitForNextFrame` 같은 Unity API와 바로 연결된다.
- 중단과 재개 흐름을 이해하기 쉽다.

### 단점

- 반환값을 다루기 불편하다.
- 중첩이 깊어지면 흐름이 금방 복잡해진다.
- `MonoBehaviour`에 의존적이다.
- 성능 민감한 코드에서는 힙 사용을 계속 점검해야 한다.

## Awaitable

### 특징

- Unity 6 계열에서 사용할 수 있는 내장 비동기 API다.
- `async/await` 문법으로 코드를 더 직선적으로 쓸 수 있다.
- Unity 프레임 루프와 자연스럽게 맞물린다.

### 예제

```csharp
using UnityEngine;

public class AwaitableExample : MonoBehaviour
{
    private async void Start()
    {
        Debug.Log("작업 시작");
        await Awaitable.WaitForSecondsAsync(2.0f);
        Debug.Log("2초 후 실행");
    }
}
```

### 장점

- `async/await` 문법을 그대로 쓸 수 있어 읽기 쉽다.
- 별도 라이브러리 없이 사용할 수 있다.
- Coroutine보다 흐름이 선형적이라 유지보수가 편하다.

### 단점

- 동일한 `Awaitable` 인스턴스를 여러 번 `await`하면 문제가 생길 수 있다.
- 상태 머신 비용 때문에 일부 힙 할당이 남을 수 있다.
- `Task`나 `UniTask`에 비해 확장 유틸리티는 적다.

## UniTask

### 특징

- Unity에서 `async/await`를 성능 지향적으로 쓰기 위해 많이 사용하는 라이브러리다.
- 값 타입 기반이라 GC 부담을 낮추는 데 유리하다.
- 다양한 비동기 헬퍼와 취소 처리 패턴을 함께 제공한다.

### 예제

```csharp
using UnityEngine;
using Cysharp.Threading.Tasks;

public class UniTaskExample : MonoBehaviour
{
    private async void Start()
    {
        Debug.Log("작업 시작");
        await UniTask.Delay(2000);
        Debug.Log("2초 후 실행");
    }
}
```

### 장점

- `async/await`를 유지하면서도 성능 비용을 낮추기 쉽다.
- 반환값, 취소, 병렬 처리 같은 패턴을 다루기 좋다.
- 규모가 커질수록 생산성과 확장성이 좋아진다.

### 단점

- 외부 라이브러리 설치가 필요하다.
- 팀이 익숙하지 않으면 초기 학습 비용이 생긴다.
- 프로젝트 규칙 없이 섞어 쓰면 오히려 비동기 스타일이 분산될 수 있다.

## 언제 무엇을 쓰면 좋을까

### Coroutine이 맞는 경우

- 간단한 애니메이션, 타이머, 페이드 같은 흐름 제어
- 반환값이 필요 없는 짧은 시퀀스
- Unity 기본 기능만으로 충분한 경우

### Awaitable이 맞는 경우

- Unity 기본 제공 방식 안에서 `async/await`를 쓰고 싶은 경우
- Coroutine보다 직선적인 코드가 필요한 경우
- 외부 의존성을 늘리고 싶지 않은 경우

### UniTask가 맞는 경우

- 성능과 GC 비용을 신경 써야 하는 경우
- 취소, 병렬 실행, 반환값 처리 등 비동기 조합이 많은 경우
- 프로젝트 전반에 일관된 async 패턴을 만들고 싶은 경우

## 정리

- 가장 단순한 흐름 제어에는 `Coroutine`이 여전히 유효하다.
- Unity 기본 `async/await` 경험이 필요하면 `Awaitable`이 적절하다.
- 성능과 확장성까지 함께 가져가려면 `UniTask`가 가장 강하다.

실제로는 "무조건 하나만 쓴다"보다, 프로젝트 성격에 맞게 기준을 정하고 혼용 범위를 통제하는 쪽이 더 중요하다.

## 참고

- [Unity Awaitable 관련 웨비나](https://www.unitysquare.co.kr/growwith/unityblog/webinarView?id=566)
- [작성한 UniTask 정리 글](https://hns17.github.io/unity/external(asset/lib/etc)/UniTask/)
- [Cysharp UniTask discussion](https://github.com/Cysharp/UniTask/discussions/627)
- [Unity Manual: Await support](https://docs.unity3d.com/kr/2023.2/Manual/AwaitSupport.html)
