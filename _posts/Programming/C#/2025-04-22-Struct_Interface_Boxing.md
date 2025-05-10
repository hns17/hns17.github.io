---
title: "Struct와 Interface의 Boxing 문제"
categories: [Programming/C#]
tags: [Memory, Boxing, Interface, Struct, Heap]
---

# C# Struct와 Interface의 Boxing 문제
## 1. C# Struct와 Class의 상속

C#에서 `struct`와 `class`는 모두 데이터를 저장하고 기능을 제공하는 데 사용되지만, 상속(inheritance) 측면에서 중요한 차이점을 갖습니다.

- **클래스 (Class)**: 클래스는 상속을 지원합니다. 즉, 한 클래스(`자식 클래스`)가 다른 클래스(`부모 클래스`)의 속성과 메서드를 상속받아 확장할 수 있습니다. 이는 코드 재사용성을 높이고, 클래스 간의 계층 구조를 만들 수 있게 합니다.
- **구조체 (Struct)**: 구조체는 상속을 지원하지 않습니다. 구조체는 다른 구조체 또는 클래스를 상속받을 수 없으며, 다른 구조체나 클래스의 기반(base)이 될 수도 없습니다. 하지만, 구조체는 인터페이스를 구현할 수 있습니다.

## 2. 캐스팅할 때 발생하는 Boxing 문제
C#에서 Struct는 스택 메모리에 할당되는 값 형식이고, 인터페이스는 힙 메모리에 할당되는 참조 형식입니다.

### 2.1 Casting에서 발생하는 Boxing 문제
Struct를 인터페이스 타입으로 캐스팅할 때, **Boxing**이 발생합니다. 이는 값 형식인 struct를 참조 형식인 interface로 변환해야 하기 때문입니다.
**Boxing**은 값 형식(Struct)을 참조 형식(Interface)으로 변환하는 과정입니다. 이 과정에서 다음과 같은 일이 일어납니다.

1. **힙(Heap) 메모리 할당**: 값 형식의 데이터를 저장하기 위한 공간이 힙 메모리에 할당됩니다.
2. **데이터 복사**: 값 형식의 데이터가 힙에 새로 할당된 공간으로 복사됩니다.
3. **참조 반환**: 힙에 생성된 객체에 대한 참조가 반환됩니다.

Unboxing은 boxing된 참조 형식을 값 형식으로 다시 변환하는 과정입니다. Boxing/Unboxing은 힙 메모리 할당 및 데이터 복사를 수반하므로 성능 저하를 일으킬 수 있습니다.

다음은 Struct를 인터페이스로 캐스팅할 때 Boxing이 발생하는 예제 코드입니다.

```csharp
using System;

interface IMyInterface
{
    int GetValue();
}

struct MyStruct : IMyInterface
{
    public int Value { get; set; }

    public int GetValue()
    {
        return Value;
    }
}

class Program
{
    static void Main(string[] args)
    {
        MyStruct myStruct = new MyStruct { Value = 10 };
        IMyInterface myInterface = myStruct; // Boxing 발생

        Console.WriteLine($"Value: {myInterface.GetValue()}");
        Console.WriteLine($"Type of myInterface: {myInterface.GetType()}"); // Boxing된 타입을 출력: System.Int32
    }
}
```

### 2.2 foreach와 IEnumerator의 Boxing 문제

이러한 문제는 C# 내부 기능에서도 종종 찾아 볼 수 있습니다.

대표적인 예로 C#의 `foreach` 루프는 컬렉션의 요소를 순회하는 편리한 방법이지만, 특정 컬렉션 인터페이스와 함께 struct를 사용할 때 예기치 않은 boxing을 발생시킬 수 있습니다. 특히, `IEnumerator`와 `IEnumerator<T>` 인터페이스를 통해 컬렉션을 순회하는 과정에서 boxing이 발생할 수 있습니다.

**문제의 원인**

`foreach` 루프는 컬렉션의 요소를 순회하기 위해 `GetEnumerator()` 메서드를 호출합니다. 이 메서드는 `IEnumerator` 또는 `IEnumerator<T>` 인터페이스를 구현하는 열거자(enumerator) 객체를 반환합니다.

- `IEnumerator`: 이 인터페이스는 `object` 형식의 요소를 반환하는 `Current` 속성을 가지고 있습니다. 따라서, struct와 같은 값 형식을 `IEnumerator`를 통해 반환하면 boxing이 발생합니다.
- `IEnumerator<T>`: 이 인터페이스는 제네릭 타입 `T`의 요소를 반환하는 `Current` 속성을 가지고 있습니다. 컬렉션이 struct 타입의 요소를 포함하고 있고, `IEnumerator<T>`를 통해 순회하는 경우 boxing을 피할 수 있습니다.

다음은 `List`를 대상으로 `IList`와 `IReadOnlyList`에 대한 예제 코드와 결과입니다.

```csharp
private List<int> _dataList;

[SetUp]
public void SetUp()
{
    _dataList = new List<int> { 1, 2, 3, 4, 5 };
}

[Test, Category("Collection")]
public void CheckAllocIListForeach()
{
    IList<int> dataList = _dataList;
    Assert.That(() =>                
    {
        foreach (var data in dataList)
        {

        }
    }, Is.Not.AllocatingGCMemory());
}

[Test, Category("Collection")]
public void CheckAllocIReadOnlyListForeach()
{
    IReadOnlyList<int> dataList = _dataList;
    Assert.That(() =>                
    {
        foreach (var data in dataList)
        {

        }
    }, Is.Not.AllocatingGCMemory());
}

[Test, Category("Collection")]
public void CheckAllocListForeach()
{
    List<int> dataList = _dataList;
    Assert.That(() =>                
    {
        foreach (var data in dataList)
        {

        }
    }, Is.Not.AllocatingGCMemory());
}
```

![image-20250504165146844](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20250504165146844.png)

`List`를 제외한 `IList`와 `IReadOnlyList`의 경우 `foreach`를 이용해 순회할 시 GC 할당이 발생하는 걸 확인할 수 있습니다.

#### 위 내용의 IL 코드 비교
### ✅ `List<int>`
- 반환 타입: `List<int>.Enumerator` (구조체)
- **Boxing 발생 없음**

```c#
IL_0002: ldarg.0      // this  
IL_0003: ldfld        class System.Collections.Generic.List<int32> AllocationTest/'<>c__DisplayClass2_0'::dataList  
IL_0008: callvirt     instance valuetype System.Collections.Generic.List<int32>.Enumerator System.Collections.Generic.List<int32>::GetEnumerator()  
IL_000D: stloc.0      // V_0  
```

------

### ⚠️ `IList<int>`
- 반환 타입: `IEnumerator<int>` (인터페이스)
- **Boxing 발생**: `List<int>.Enumerator` 구조체가 `IEnumerator<int>` 인터페이스 타입으로 변환될 때 Boxing이 발생하여 힙에 할당됩니다.

```c#
IL_0002: ldarg.0      // this  
IL_0003: ldfld        class System.Collections.Generic.IList<int32> AllocationTest/'<>c__DisplayClass3_0'::dataList  
IL_0008: callvirt     instance class System.Collections.Generic.IEnumerator<int32> System.Collections.Generic.IEnumerable<int32>::GetEnumerator()  
IL_000D: stloc.0      // V_0  
```

------

### ⚠️ `IReadOnlyList<int>`
- 반환 타입: `IEnumerator<int>` (인터페이스)
- **Boxing 발생**: `List<int>.Enumerator` 구조체가 `IEnumerator<int>` 인터페이스 타입으로 변환될 때 Boxing이 발생하여 힙에 할당됩니다.

```c#
IL_0002: ldarg.0      // this  
IL_0003: ldfld        class System.Collections.Generic.IReadOnlyList<int32> AllocationTest/'<>c__DisplayClass4_0'::dataList  
IL_0008: callvirt     instance class System.Collections.Generic.IEnumerator<int32> System.Collections.Generic.IEnumerable<int32>::GetEnumerator()  
IL_000D: stloc.0      // V_0  
```

------

## Boxing 발생 원인
- `List<T>.Enumerator`는 구조체 (`struct`, value type)입니다.

- `foreach`는 내부적으로 `GetEnumerator()` 호출 결과를 `IEnumerator<T>`로 받아 사용합니다.

- **value type을 interface 타입으로 받을 경우 boxing이 발생**합니다. (`struct` → `interface` 변환)

  | 타입                 | Enumerator 반환                 | Boxing 발생 여부 | 설명                     |
| -------------------- | ------------------------------- | ---------------- | ------------------------ |
| `List<int>`          | `List<int>.Enumerator` (struct) | ✅ 없음           | 구조체 그대로 사용       |
| `IList<int>`         | `IEnumerator<int>` (interface)  | ⚠️ 발생           | 구조체 → 인터페이스 변환 |
| `IReadOnlyList<int>` | `IEnumerator<int>` (interface)  | ⚠️ 발생           | 구조체 → 인터페이스 변환 |

------

## Ref
- https://tsgcpp.hateblo.jp/entry/2021/11/21/001927
- https://referencesource.microsoft.com/#mscorlib/system/collections/generic/list.cs,574