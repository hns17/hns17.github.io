---
title: Delegate와 Heap
categories: [Programming/C#]
tags: [Memory, Delegate, Heap]

---

# 📘 C# Delegate 생성과 힙 할당 (Heap Allocation)

------

## 🔍 개요

C#에서 **delegate(대리자)** 는 단순한 메서드 포인터가 아닌 **객체**입니다. 인스턴스 메서드를 참조하거나 람다를 사용하는 경우, **힙(Heap)** 메모리에 객체가 생성되어 **GC 할당(Garbage Collection Allocation)** 이 발생할 수 있습니다.

------

## 📌 Delegate가 힙에 할당되는 이유

대리자는 다음 정보를 포함하는 복합 객체입니다:

- **타겟 인스턴스 (Target Instance)**
- **메서드 정보 (MethodInfo)**
- **멀티캐스트 리스트 (Invocation List)**

이로 인해 단순 메서드 참조 이상의 메모리 자원을 필요로 하며, 대부분의 경우 **힙 할당이 수반**됩니다.

------

### ✅ 대리자 핵심 구성 요소 분석

#### 1. 타겟 인스턴스 (Target Instance)

- 대리자가 **인스턴스 메서드**를 참조하는 경우, **해당 인스턴스에 대한 참조**를 보관합니다.
- **정적 메서드**를 참조하는 경우에는 인스턴스가 필요 없으므로 **null**입니다.

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

------

#### 2. 메서드 정보 (MethodInfo)

- 대리자는 참조 중인 메서드의 **정확한 메타데이터**를 `MethodInfo` 형태로 가지고 있습니다.
- 이름, 반환형, 매개변수, 정적 여부 등을 포함합니다.

```csharp
Action<string> greet = (name) => Console.WriteLine($"Hello, {name}");

MethodInfo info = greet.Method;
Console.WriteLine(info.Name);       // ex: <Main>b__0_0
Console.WriteLine(info.ReturnType); // ex: System.Void
Console.WriteLine(info.IsStatic);   // ex: True
```

------

#### 3. 멀티캐스트 리스트 (Multicast Invocation List)

- C#의 대리자는 하나 이상의 메서드를 호출할 수 있습니다.
- `+=` 연산자를 통해 여러 메서드를 체인처럼 연결하면 내부적으로 **Invocation List**라는 리스트에 저장됩니다.

```csharp
void A() => Console.WriteLine("A");
void B() => Console.WriteLine("B");

Action multi = A;
multi += B;

foreach (var del in multi.GetInvocationList())
{
    Console.WriteLine(del.Method.Name);  // 출력: A, B
}
```

------

## 🚨 힙 할당이 발생하는 코드 예시와 분석

### ❌ `Member Method`

```csharp
Action actEvent = MemberMethod;
actEvent.Invoke();
```

- 인스턴스 메서드 참조 → **`this`가 캡처됨**
- **대리자 객체가 런타임에 생성** → **힙 할당**

------

### ❌ `Property`

```csharp
private Action TempAction => MemberMethod;
TempAction.Invoke();
```

- **속성 호출마다 새로운 대리자 생성**
- 매 호출 시 **GC 할당** 발생 가능성 높음

------

### ❌ `Static Method`

```csharp
Action actEvent = StaticMethod;
actEvent.Invoke();
```

- 정적 메서드라도 **대리자 객체 생성**은 발생
- 일부 JIT 환경에선 최적화 가능, AOT에서는 할당 거의 확정

------

### ❌ 람다 및 클로저 사용 시

```csharp
void Test()
{
    int x = 5;
    Action a = () => Console.WriteLine(x); // 클로저 객체 + 대리자 객체 생성
}
```

- 외부 변수 `x` 캡처 → **클로저 객체 생성**
- 대리자 객체도 별도로 생성됨 → **이중 힙 할당**

------

### ❌ 반복적으로 대리자 결합

- 여러 대리자를 결합하면 내부적으로 `MulticastDelegate`의 **Invocation List**가 생성되며, 이는 새로운 배열이 필요하므로 **힙 할당이 발생**합니다.

```
void A() => Console.WriteLine("A");
void B() => Console.WriteLine("B");

Action multi = null;
multi += A;  
multi += B;  
```

------



## 💡 할당 최소화를 위한 팁

| 전략                                    | 설명                                          |
| --------------------------------------- | --------------------------------------------- |
| ✅ **대리자 캐싱**                       | 대리자 인스턴스를 멤버 변수에 저장하여 재사용 |
| ✅ **외부 변수 캡처 피하기**             | 람다에서 캡처된 변수가 없도록 설계            |
| ✅ **Delegate.Combine / += / -= 최소화** | Invocation List 생성을 최소화                 |



#### ✅대리자 캐싱

- 최초 할당시에만 인스턴스가 생성됨.

```csharp
private Action MemberAction;

public void Initialize()
{
    MemberAction = MemberMethod; // 한 번만 생성
}
```

#### ✅클로저 피하기

- 로컬 변수를 사용하지 않고 멤버 변수를 사용
- 외부 변수가 필요하지 않는 경우 사용X

#### ✅Delegate.Combine 사용하기

- `Delegate.Combine`을 명시적으로 사용해 반복적인 힙 사용 최소화 하기

```
Action A = () => Console.WriteLine("A");
Action B = () => Console.WriteLine("B");

Action combined = (Action)Delegate.Combine(A, B); // 명시적으로 한 번만 결합
combined.Invoke();
```

------



## ✅ 테스트

```c#
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



## 📎 요약

- 대리자는 할당시 인스턴스를 생성하므로 힙을 사용
- 외부 변수 사용시 클로저를 생성하므로 추가로 힙 사용
- MulticastDelegate를 이용할 경우 주의하지 않으면 반복적으로 힙 사용 발생

------



## 📘 참고

- [Microsoft C# 언어 참조: delegate](https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/delegate)
- [.NET Internals: Delegate Implementation Deep Dive](https://learn.microsoft.com/archive/msdn-magazine/2003/september/net-delegates)

- [https://www.mattgibson.dev/blog/csharp-delegates-memory-summary](https://www.mattgibson.dev/blog/csharp-delegates-memory-summary)
