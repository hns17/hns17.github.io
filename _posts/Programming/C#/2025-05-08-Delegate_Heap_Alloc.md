---
title: Delegate와 Heap
categories: [Programming/C#]
tags: [Memory, Delegate, Heap]

---

> 핵심 요약
> - `delegate`는 단순한 함수 포인터가 아니라 객체다.
> - 인스턴스 메서드 참조, 람다 캡처, 멀티캐스트 결합에서는 힙 할당이 발생할 수 있다.
> - 자주 호출되는 경로에서는 delegate 캐싱과 클로저 최소화가 중요하다.

`delegate`는 편하지만, 비용을 모르고 쓰면 GC 할당 지점이 숨어들기 쉽다. 이 글은 delegate가 왜 힙을 사용하는지, 어떤 패턴에서 할당이 생기는지, 그리고 실무에서 어떻게 줄일 수 있는지 정리한다.

## delegate가 힙을 쓰는 이유

delegate는 다음 정보를 담는 복합 객체다.

- 타겟 인스턴스
- 메서드 정보
- 멀티캐스트 호출 목록

즉, 단순히 "메서드 주소만 저장하는 값"이 아니라 런타임이 관리해야 하는 참조형 객체에 가깝다. 그래서 상황에 따라 힙 할당이 뒤따른다.

### 타겟 인스턴스

인스턴스 메서드를 참조하면 delegate 내부에 해당 객체 참조가 저장된다. 정적 메서드는 인스턴스가 필요 없어서 `Target`이 `null`이다.

```csharp
class MyClass
{
    public void InstanceMethod() => Console.WriteLine("Instance");
    public static void StaticMethod() => Console.WriteLine("Static");
}

MyClass obj = new MyClass();
Action a1 = obj.InstanceMethod;
Action a2 = MyClass.StaticMethod;

Console.WriteLine(a1.Target); // 출력: MyClass 인스턴스
Console.WriteLine(a2.Target); // 출력: null
```

### 메서드 정보

delegate는 참조 중인 메서드의 메타데이터를 `MethodInfo`로 들고 있다. 이름, 반환형, 정적 여부 같은 정보가 여기에 포함된다.

```csharp
Action<string> greet = (name) => Console.WriteLine($"Hello, {name}");

MethodInfo info = greet.Method;
Console.WriteLine(info.Name);       // ex: <Main>b__0_0
Console.WriteLine(info.ReturnType); // ex: System.Void
Console.WriteLine(info.IsStatic);   // ex: True
```

### 호출 목록

`+=`로 여러 메서드를 묶으면 내부적으로 invocation list가 생긴다. 이 목록을 유지하기 위한 추가 메모리도 필요하다.

```csharp
void A() => Console.WriteLine("A");
void B() => Console.WriteLine("B");

Action multi = A;
multi += B;

foreach (var del in multi.GetInvocationList())
{
    Console.WriteLine(del.Method.Name); // 출력: A, B
}
```

## 힙 할당이 생기는 대표 패턴

### 인스턴스 메서드 참조

```csharp
Action actEvent = MemberMethod;
actEvent.Invoke();
```

- 인스턴스 메서드를 참조하면 `this`가 함께 묶인다.
- 이 시점에 delegate 객체가 생성되면서 힙 할당이 발생할 수 있다.

### 프로퍼티에서 delegate 반환

```csharp
private Action TempAction => MemberMethod;
TempAction.Invoke();
```

- 프로퍼티에 접근할 때마다 새 delegate를 만들게 된다.
- 반복 호출 경로에 두면 GC 압력이 커진다.

### 정적 메서드 참조

```csharp
Action actEvent = StaticMethod;
actEvent.Invoke();
```

- 정적 메서드는 `Target`은 없지만 delegate 객체 자체는 만들어진다.
- JIT 환경에서는 최적화될 수도 있지만, AOT를 기준으로 보면 안전하게 "할당 가능성이 있다"라고 보는 편이 낫다.

### 람다와 클로저

```csharp
void Test()
{
    int x = 5;
    Action a = () => Console.WriteLine(x);
}
```

- 외부 변수 `x`를 캡처하면 클로저 객체가 먼저 만들어진다.
- 여기에 delegate 객체까지 추가되어 이중 할당이 생긴다.

### 반복적인 delegate 결합

```csharp
void A() => Console.WriteLine("A");
void B() => Console.WriteLine("B");

Action multi = null;
multi += A;
multi += B;
```

- `MulticastDelegate`는 호출 목록을 유지해야 한다.
- 결합과 해제가 반복되면 내부 배열 재구성이 일어나면서 추가 할당이 생길 수 있다.

## 할당을 줄이는 방법

| 방법 | 설명 |
| --- | --- |
| delegate 캐싱 | 멤버 필드에 저장해 재사용한다. |
| 캡처 줄이기 | 람다에서 외부 변수를 가능한 한 잡지 않는다. |
| 결합 횟수 줄이기 | `+=`, `-=`, `Delegate.Combine` 호출을 최소화한다. |

### delegate 캐싱

한 번 만든 delegate를 반복 호출에 재사용하면 불필요한 재할당을 줄일 수 있다.

```csharp
private Action MemberAction;

public void Initialize()
{
    MemberAction = MemberMethod;
}
```

### 클로저 피하기

- 로컬 변수를 캡처하는 대신 멤버 필드를 직접 참조한다.
- 굳이 람다가 필요 없다면 메서드 그룹을 사용하는 편이 낫다.

### 결합 지점 줄이기

```csharp
Action A = () => Console.WriteLine("A");
Action B = () => Console.WriteLine("B");

Action combined = (Action)Delegate.Combine(A, B);
combined.Invoke();
```

반복 루프 안에서 계속 결합하는 것보다, 필요한 시점에 한 번 만들고 재사용하는 편이 낫다.

## 테스트 코드

아래 테스트는 어떤 패턴에서 GC 할당이 생기는지 확인하기 위해 사용했다.

```csharp
public class AllocationTest_Delegate
{
    private Action MemberAction;
    private Action TempAction => MemberMethod;

    [SetUp]
    public void SetUp()
    {
        MemberAction = MemberMethod;
    }

    [Test, Category("Delegate")]
    public void CheckAllocAccessActionCached()
    {
        Assert.That(() =>
        {
            MemberAction();
        }, Is.Not.AllocatingGCMemory());
    }

    [Test, Category("Delegate")]
    public void CheckAllocAccessFunction()
    {
        Assert.That(() =>
        {
            MemberMethod();
        }, Is.Not.AllocatingGCMemory());
    }

    [Test, Category("Delegate")]
    public void CheckAllocAction()
    {
        Action actEvent;
        Assert.That(() =>
        {
            actEvent = MemberMethod;
            actEvent.Invoke();
        }, Is.Not.AllocatingGCMemory());
    }

    [Test, Category("Delegate")]
    public void CheckAllocStaticAction()
    {
        Assert.That(() =>
        {
            Action actEvent = StaticMethod;
            actEvent.Invoke();
        }, Is.Not.AllocatingGCMemory());
    }

    [Test, Category("Delegate")]
    public void CheckAllocTempAction()
    {
        Assert.That(() =>
        {
            TempAction.Invoke();
        }, Is.Not.AllocatingGCMemory());
    }

    private void MemberMethod()
    {
    }

    private static void StaticMethod()
    {
    }
}
```

![image-20250509000533322](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20250509000533322.png)

테스트를 보면 메서드 호출 자체보다 "delegate를 만드는 순간"과 "캡처가 발생하는 순간"이 핵심 포인트라는 걸 확인할 수 있다.

## 정리

- delegate는 참조형 객체이기 때문에 상황에 따라 힙 할당이 발생한다.
- 특히 인스턴스 메서드 참조, 람다 캡처, 멀티캐스트 결합은 비용이 커질 수 있다.
- 성능 민감 구간에서는 "언제 delegate를 새로 만들고 있는가"를 먼저 의심하는 편이 좋다.

## 참고

- [Microsoft C# 언어 참조: delegate](https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/delegate)
- [.NET Internals: Delegate Implementation Deep Dive](https://learn.microsoft.com/archive/msdn-magazine/2003/september/net-delegates)
- [C# delegates and memory allocation summary](https://www.mattgibson.dev/blog/csharp-delegates-memory-summary)
