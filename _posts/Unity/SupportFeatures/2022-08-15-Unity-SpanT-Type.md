---
title: "Unity Span< T > Type"
categories: [Unity/SupportFeatures]
tags: ["Unity", "Unity Span<T>"]
---

> 핵심 요약
> - 이 글은 `Unity Span< T > Type` 기능이나 라이브러리의 사용 포인트를 정리한다.
> - 핵심 개념과 적용 방법을 중심으로 살펴본다.
> - 실제로 사용할 때 주의할 점도 함께 정리한다.

![image-20220815164824306](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220815164824306.png)

- Unity 2021.2 버전부터 Span 타입이 추가되었다는 사실을 확인
- 덕분에 안전영역에서 편하게 stackalloc 사용이 가능해짐

- Unity2021.3에서 간단히 테스트 코드를 작성해보면 별도의 dll 추가없이 사용가능

  ![image-20220815170813215](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220815170813215.png)
