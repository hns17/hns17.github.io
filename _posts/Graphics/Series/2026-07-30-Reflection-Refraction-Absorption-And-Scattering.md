---
title: "[빛에서 픽셀까지 005] 빛이 물질에 닿으면 어떻게 나뉘는가: 반사, 굴절, 흡수와 산란"
categories: [Graphics/Series/Light-To-Pixel]
tags: ["Graphics", "Light", "Reflection", "Refraction", "Absorption", "Scattering", "Fresnel"]
series: graphics-foundations
series_title: "빛에서 픽셀까지"
series_url: "/category/graphics/series/light-to-pixel/"
series_id: G005
series_order: 5
---

> 핵심 요약
> - 빛이 물질에 닿으면 경계에서 일부는 반사되고 일부는 안으로 전달된다. 전달된 빛의 방향이 매질의 굴절률 때문에 바뀌는 현상이 굴절이다.
> - 물질 안으로 들어간 빛은 이동하는 동안 흡수되어 다른 에너지로 바뀌거나, 산란되어 진행 방향을 바꿀 수 있다. 산란은 빛을 없애는 것이 아니라 다른 경로로 재분배한다.
> - 그래픽스의 재질은 결국 들어온 빛을 어느 방향에 얼마나 남길지 정하는 모델이다. 이 관계를 수치로 계산하려면 다음 글에서 다룰 Radiometry가 필요하다.

[앞 글](/graphics/series/light-to-pixel/Newton-Prism-And-Spectrum-Of-Light/)에서는 흰빛이 여러 파장 성분을 포함하며, 프리즘의 파장별 굴절률 `n(λ)`가 그 성분들을 서로 다른 방향으로 갈라놓는다는 것을 살펴봤다. 이제 광선이 어떤 빛을 운반하는지는 알게 됐지만, 그 빛이 물체에 닿은 뒤 어디로 가는지는 아직 정하지 않았다.

같은 흰빛을 거울, 유리컵, 검은 천과 우유에 비추면 전혀 다른 결과가 보인다.

- 거울에서는 주변 장면이 선명하게 되돌아온다.
- 유리에서는 표면의 반사와 유리 너머의 장면이 함께 보인다.
- 검은 천에서는 돌아오는 빛이 매우 적다.
- 우유에서는 빛이 내부 여러 방향으로 퍼져 불투명하고 부드럽게 보인다.

물체의 모양만으로는 이 차이를 만들 수 없다. 렌더러가 재질을 표현하려면 빛이 물질과 만났을 때 **어디로 이동하고, 얼마나 남으며, 어떤 파장 성분이 달라지는지** 계산해야 한다.

## 네 현상은 한 지점의 네 갈래가 아니다

반사, 굴절, 흡수와 산란은 흔히 입사 광선 하나에서 네 개의 화살표가 동시에 갈라지는 그림으로 소개된다. 입문용 구분으로는 편리하지만, 그대로 받아들이면 경계에서 일어나는 일과 물질 내부에서 누적되는 일을 혼동하기 쉽다.

더 정확한 첫 번째 구조는 두 단계다.

1. **물질의 경계**에서 빛은 입사한 쪽으로 반사되거나 다른 물질 안으로 전달된다. 전달 방향이 바뀌면 굴절이라고 부른다.
2. **물질 내부**를 이동하는 빛은 거리에 따라 흡수되거나 다른 방향으로 산란될 수 있다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g005-light-material-interaction/interface-and-medium-processes-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g005-light-material-interaction/interface-and-medium-processes.svg" alt="입사광이 물질 경계에서 반사광과 굴절된 투과광으로 나뉘고 물질 내부로 들어간 빛이 이동하면서 흡수되거나 여러 방향으로 산란되는 두 단계 과정">
</picture>

*그림 1. 반사와 투과·굴절은 먼저 경계에서 갈리고, 흡수와 체적 산란은 안으로 들어간 빛의 경로를 따라 일어난다. 실제 재질에서는 이 과정이 파장마다 다르게 나타날 수 있다. 개념도, 직접 제작.*

| 현상 | 빛에 일어나는 일 | 그래픽스에서 결정할 정보 |
| --- | --- | --- |
| **반사 Reflection** | 입사한 매질 쪽으로 되돌아간다 | 반사 방향과 반사 비율 |
| **투과·굴절 Transmission·Refraction** | 경계를 넘어가며 속도와 방향이 달라질 수 있다 | 굴절 방향과 전달 비율 |
| **흡수 Absorption** | 빛 에너지가 열 같은 다른 형태로 전환된다 | 파장별 흡수율과 이동 거리 |
| **산란 Scattering** | 진행 방향이 다른 방향으로 바뀐다 | 산란량과 새로운 방향 분포 |

여기서 `투과`와 `굴절`은 완전히 같은 말은 아니다. 투과는 빛이 경계를 넘어갔다는 에너지 경로를 뜻하고, 굴절은 그 과정에서 진행 방향이 바뀌는 기하 현상을 뜻한다. 굴절률이 같은 두 영역의 경계라면 빛은 투과하지만 방향은 바뀌지 않을 수 있다.

## 반사 법칙과 Snell의 법칙은 방향을 정한다

매끄러운 경계에 광선이 닿으면 표면 법선 `N`을 기준으로 입사각과 반사각이 같다.

```text
θᵢ = θᵣ
```

- `θᵢ`: 입사 광선과 법선 사이의 각도
- `θᵣ`: 반사 광선과 법선 사이의 각도

완전한 거울 반사는 이 관계로 반사 방향 하나를 정할 수 있다. 표면이 거칠면 미세한 면들의 법선이 제각각이어서 반사광이 여러 방향으로 퍼지지만, 각각의 미세한 반사는 여전히 같은 원리를 따른다고 볼 수 있다.

경계를 통과한 광선의 방향은 Snell의 법칙으로 정한다.

```text
n₁(λ) sin θᵢ = n₂(λ) sin θₜ
```

- `n₁(λ)`, `n₂(λ)`: 경계 양쪽 매질의 파장별 굴절률
- `θₜ`: 전달된 광선과 법선 사이의 각도

빛이 공기에서 유리처럼 굴절률이 큰 물질로 들어가면 법선 쪽으로 꺾이고, 반대로 나올 때는 법선에서 멀어지는 쪽으로 꺾인다. 안쪽에서 바깥쪽으로 나가려는 각도가 임계각보다 커지면 전달 방향이 존재하지 않고 모든 빛이 되돌아오는 **전반사(Total Internal Reflection)**가 일어난다.

하지만 이 두 법칙만으로는 유리창에 반사된 얼굴이 얼마나 밝아야 하는지 알 수 없다. 반사 법칙과 Snell의 법칙이 답하는 질문은 **어디로 가는가**이지 **얼마나 가는가**가 아니다.

## Fresnel은 반사와 전달의 비율을 각도와 연결했다

공기와 유리처럼 굴절률이 다른 두 물질의 경계에서는 일반적으로 반사와 전달이 동시에 일어난다. 유리가 투명하다고 해서 표면 반사가 0이 되는 것도 아니고, 반사광을 계산했다고 해서 나머지 빛이 모두 사라지는 것도 아니다.

Augustin-Jean Fresnel은 파동 이론을 바탕으로 반사되는 빛의 양이 입사각과 편광 방향에 따라 달라지는 관계를 구했다. [1823년 1월 7일 Académie des sciences에서 발표한 회고록](https://fr.wikisource.org/wiki/Page:M%C3%A9moires_de_l%E2%80%99Acad%C3%A9mie_des_sciences,_Tome_11.djvu/631)의 첫머리부터 투명한 물질에서 모든 입사각에 대한 반사 세기를 두 편광 성분으로 나누어 다룬다고 밝힌다.

현대 렌더러가 편광을 생략할 때는 두 성분을 평균한 Fresnel 반사율을 주로 사용한다.

```text
F(θᵢ, λ) = 경계에서 반사되는 빛의 비율
```

흡수가 없는 이상적인 유전체 경계를 에너지 흐름 기준으로 정규화하면, 반사되지 않은 부분은 전달된다.

```text
R(θᵢ, λ) + T(θᵢ, λ) = 1
```

공기 `n₁ ≈ 1.0`에서 일반적인 유리 `n₂ ≈ 1.5`로 거의 수직 입사할 때 반사율은 약 4%다.

```text
R₀ = ((n₁ - n₂) / (n₁ + n₂))² ≈ 0.04
```

그래서 정면에서 본 깨끗한 유리는 대부분의 빛을 통과시키면서도 약한 반사를 보인다. 시선이 표면과 나란해지는 스침각에 가까워질수록 반사율은 크게 증가해, 같은 유리도 가장자리에서는 거울처럼 보이기 시작한다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g005-light-material-interaction/fresnel-angle-energy-split-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g005-light-material-interaction/fresnel-angle-energy-split.svg" alt="공기와 유리 경계에서 거의 수직으로 들어오는 빛은 약 4퍼센트만 반사되고 대부분 굴절되지만 스침각에 가까워질수록 반사 비율이 크게 증가하는 Fresnel 효과 비교">
</picture>

*그림 2. 반사 방향과 굴절 방향만 계산해서는 유리의 모습이 완성되지 않는다. Fresnel 반사율은 같은 경계에서도 입사각에 따라 두 경로에 배분되는 양이 달라진다는 것을 보여 준다. 공기–굴절률 1.5 유리의 비편광 근삿값, 직접 제작.*

[PBRT 4판의 Fresnel 설명](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)은 고정된 반사 계수 하나로는 이 방향 의존성을 표현할 수 없다고 강조한다. 전반사에서는 전달 경로가 사라지고 `F = 1`이 된다.

이 관계는 컴퓨터 그래픽스의 재질 모델에도 들어왔다. Cook과 Torrance는 [1982년 「A Reflectance Model for Computer Graphics」](https://doi.org/10.1145/357290.357293)에서 미세면의 방향 분포, 가려짐과 함께 Fresnel 항을 사용해 금속과 플라스틱의 반사를 기존 경험적 모델보다 물리적으로 설명했다. Fresnel은 광학 교과서의 부가 지식이 아니라, 물체의 가장자리와 재질 종류가 왜 다르게 반짝이는지를 계산하는 핵심 요소가 됐다.

## 흡수는 경계가 아니라 이동 거리에서 누적된다

경계를 통과한 빛이 물질 내부에서 그대로 유지된다고 가정하면 얇은 유리와 두꺼운 유리가 같은 색과 밝기로 보여야 한다. 하지만 같은 색유리도 두꺼울수록 더 어둡고 색이 짙어지며, 얕은 물과 깊은 물도 다르게 보인다.

흡수는 빛이 물질 내부를 이동하는 동안 특정 파장 성분의 에너지가 다른 형태로 전환되는 과정이다. 파장별 흡수 계수 `σₐ(λ)`는 단위 거리당 흡수될 가능성을 나타내며 단위는 `1/거리`다.

산란이 없는 균일한 물질에서 거리 `d`를 지난 뒤 남는 비율은 Beer의 법칙 형태로 쓸 수 있다.

```text
Tₐ(d, λ) = exp(-σₐ(λ)d)
```

이 식이 보여 주는 핵심은 일정량을 한 번 빼는 것이 아니라, **현재 남은 빛의 일정 비율이 거리마다 계속 줄어든다**는 점이다. 따라서 두께가 두 배가 되면 단순히 밝기가 절반으로 줄어드는 것이 아니라 지수적으로 감쇠한다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g005-light-material-interaction/path-length-absorption-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g005-light-material-interaction/path-length-absorption.svg" alt="같은 흡수 계수를 가진 색유리에서 짧은 거리 d를 통과한 광선보다 두 배 거리 2d를 통과한 광선의 세기가 지수적으로 더 줄고 파장별 흡수 차이로 색도 달라지는 비교">
</picture>

*그림 3. 흡수는 표면에 한 번 적용하는 색 곱셈이 아니라 내부 이동 거리에 따라 누적된다. 같은 재질에서도 광선이 지나간 두께가 다르면 투과광의 밝기와 스펙트럼이 달라진다. 개념도, 직접 제작.*

이 관계는 흔히 Beer–Lambert 법칙으로 불리지만 역사적으로는 한 사람이 한 번에 만든 식이 아니다. [Bouguer–Beer–Lambert 법칙의 역사 검토](https://pmc.ncbi.nlm.nih.gov/articles/PMC7540309/)에 따르면 Bouguer와 Lambert의 경로 길이 감쇠, Beer의 용액 농도 관계가 이후의 표기에서 결합됐다. 그래픽스에서 중요한 부분은 균일한 매질의 투과율이 이동 거리와 소멸 계수의 지수 함수라는 구조다.

## 산란은 빛을 없애지 않고 방향을 바꾼다

안개 속 손전등 빛줄기가 옆에서도 보이고, 우유와 밀랍이 내부에서 부드럽게 빛나는 이유는 빛이 곧은 한 경로만 유지하지 않기 때문이다. 입자나 미세 구조와 상호작용한 빛은 새로운 방향으로 진행할 수 있다.

특정 광선만 따라가면 산란도 빛이 줄어드는 현상처럼 보인다.

- **Out-scattering**은 현재 광선의 빛을 다른 방향으로 보내므로 그 경로의 밝기를 줄인다.
- **In-scattering**은 다른 방향의 빛을 현재 광선 방향으로 보내므로 카메라가 보는 밝기를 늘린다.
- **흡수**는 에너지를 빛이 아닌 다른 형태로 바꾸므로 다른 광선으로 되돌아오지 않는다.

이 차이 때문에 산란을 흡수와 같은 `빛의 소멸`로만 처리하면 안개 속 광선, 구름의 밝은 가장자리와 피부·밀랍의 부드러운 투과를 표현할 수 없다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g005-light-material-interaction/absorption-and-scattering-events-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g005-light-material-interaction/absorption-and-scattering-events.svg" alt="체적 안을 진행하는 기준 광선에서 흡수는 빛을 제거하고 out scattering은 다른 방향으로 빛을 보내며 in scattering은 다른 경로의 빛을 기준 광선 방향으로 더하는 과정">
</picture>

*그림 4. 흡수와 Out-scattering은 현재 광선의 빛을 줄이지만 이유가 다르다. 산란된 빛은 다른 방향에 남아 있으며, 다른 경로에서 들어오는 In-scattering은 현재 광선을 다시 밝힐 수 있다. 개념도, 직접 제작.*

[PBRT 4판의 Volume Scattering Processes](https://pbr-book.org/4ed/Volume_Scattering/Volume_Scattering_Processes)는 단위 거리당 흡수 계수를 `σₐ`, 산란 계수를 `σₛ`로 두고, 현재 방향의 빛이 줄어드는 두 효과의 합을 소멸 계수 `σₜ`로 정의한다.

```text
σₜ(λ) = σₐ(λ) + σₛ(λ)
```

균일한 매질에서 한 방향의 빛이 거리 `d` 동안 상호작용 없이 살아남는 비율은 다음과 같다.

```text
Tᵣ(d, λ) = exp(-σₜ(λ)d)
```

이 투과율 `Tᵣ`은 현재 빔에서 흡수되거나 밖으로 산란되지 않고 남은 비율이다. 전체 장면에서 빛 에너지가 모두 사라졌다는 뜻은 아니다. 산란된 빛이 다른 방향에서 다시 들어오는 양까지 계산해야 카메라에 도달하는 최종 빛을 구할 수 있다.

산란 뒤 어느 방향이 더 유력한지는 **Phase Function**으로 표현한다. 연기와 안개처럼 진행 방향 쪽으로 빛을 많이 보내는 매질도 있고, 여러 방향에 비교적 고르게 보내는 매질도 있다. 이는 표면에서 들어온 방향과 나가는 방향의 관계를 표현하는 BSDF와 비슷한 역할을 체적에서 수행한다.

## 그래픽스에서 Scattering은 더 넓은 말로 쓰인다

일상어로 산란이라고 하면 주로 안개나 우유 속에서 빛이 퍼지는 현상을 떠올린다. 하지만 렌더링 이론에서 **Scattering**은 빛의 방향이 상호작용으로 재분배되는 현상을 더 넓게 묶는 말이다.

[PBRT의 Reflection Models](https://www.pbr-book.org/4ed/Reflection_Models)은 표면의 반사를 BRDF, 투과를 BTDF로 나타내고, 둘을 합친 BSDF를 Bidirectional Scattering Distribution Function이라고 부른다. 즉 표면 반사와 투과도 넓은 의미에서는 표면 산란에 속한다.

이를 위치에 따라 구분하면 다음처럼 정리할 수 있다.

| 계산 위치 | 대표 모델 | 설명 |
| --- | --- | --- |
| **표면 한 점** | BRDF·BTDF·BSDF | 들어온 빛을 표면의 어느 방향으로 보낼지 계산한다 |
| **체적 내부 한 점** | Phase Function | 매질 안에서 산란된 빛을 어느 방향으로 보낼지 계산한다 |
| **체적 내부 구간** | Transmittance | 이동 거리 동안 흡수·Out-scattering 없이 남은 비율을 계산한다 |

표면과 체적을 구분하지 않으면 불투명 페인트, 투명 유리와 반투명 밀랍을 모두 같은 `표면 색` 값으로 설명하려 하게 된다. 간단한 실시간 모델에서는 이런 효과를 미리 근사해 표면 파라미터에 담기도 하지만, 무엇을 생략했는지 이해하려면 실제 빛의 경로를 먼저 알아야 한다.

## 같은 빛도 재질에 따라 다른 픽셀이 된다

이제 글의 시작에서 본 네 물질을 빛의 경로로 다시 설명할 수 있다.

- **거울**은 매끄러운 표면 반사가 지배적이어서 주변 장면의 방향 관계가 유지된다.
- **깨끗한 유리**는 Fresnel 반사와 굴절된 전달이 함께 있고, 내부 흡수와 산란이 작다.
- **색유리**는 표면에서는 유리처럼 반사·굴절하지만 내부에서 파장별 흡수가 누적된다.
- **우유와 밀랍**은 안으로 들어간 빛이 여러 번 산란해 입사 지점과 다른 위치와 방향으로 나온다.
- **검은 천**은 미세 구조에서 빛이 여러 번 상호작용하는 동안 많은 에너지를 흡수해 카메라로 돌아오는 양이 적다.

재질은 물체에 붙이는 색 이름이 아니다. 같은 입사광을 받아 어떤 경로와 스펙트럼으로 카메라에 돌려보낼지를 정하는 규칙의 집합이다. 훗날 다룰 Lambert, Blinn–Phong, Microfacet와 같은 반사 모델과 PBR은 모두 이 복잡한 상호작용에서 필요한 부분을 서로 다른 방식으로 근사한다.

## 정리

- 반사와 투과·굴절은 물질 경계에서 먼저 갈리고, 흡수와 체적 산란은 안으로 들어간 빛의 이동 경로에서 누적된다.
- 반사 법칙과 Snell의 법칙은 빛의 방향을 정하지만, 반사와 전달의 양은 Fresnel 관계가 정한다.
- 투명한 유리도 정면에서 약한 반사를 보이며, 스침각에 가까워질수록 반사 비율이 커진다.
- 흡수는 파장별 흡수 계수와 이동 거리에 따라 지수적으로 누적되므로 같은 재질도 두께에 따라 다르게 보인다.
- 산란은 빛을 제거하는 것이 아니라 방향을 재분배한다. Out-scattering은 현재 경로를 어둡게 하고 In-scattering은 다른 경로의 빛을 더한다.
- 렌더링에서 Scattering은 체적 산란뿐 아니라 표면의 반사와 투과를 포함하는 넓은 용어로도 사용된다.
- 재질 모델은 결국 입사한 빛을 어느 방향에 얼마나 분배할지를 계산하는 모델이다.

지금까지는 빛의 비율과 감쇠를 `얼마나 남는가`라는 말로 설명했다. 하지만 광원의 전체 출력, 특정 방향으로 가는 양, 표면에 도달한 양과 눈에 보이는 밝기는 모두 서로 다른 물리량이다. 다음 글에서는 이들을 혼동하지 않기 위해 **Radiometry와 Photometry가 무엇을 측정하며 왜 두 체계가 필요한지** 살펴본다.

## 참고

- [Augustin-Jean Fresnel, Mémoire sur la loi des modifications que la réflexion imprime à la lumière polarisée, 1823 — Académie des sciences 원문 스캔](https://fr.wikisource.org/wiki/Page:M%C3%A9moires_de_l%E2%80%99Acad%C3%A9mie_des_sciences,_Tome_11.djvu/631)
- [Robert L. Cook, Kenneth E. Torrance, A Reflectance Model for Computer Graphics, 1982 — ACM](https://doi.org/10.1145/357290.357293)
- [Physically Based Rendering, 4th Edition — Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)
- [Physically Based Rendering, 4th Edition — Reflection Models](https://www.pbr-book.org/4ed/Reflection_Models)
- [Physically Based Rendering, 4th Edition — Volume Scattering Processes](https://pbr-book.org/4ed/Volume_Scattering/Volume_Scattering_Processes)
- [Physically Based Rendering, 4th Edition — Transmittance](https://pbr-book.org/4ed/Volume_Scattering/Transmittance)
- [The Bouguer–Beer–Lambert Law: Shining Light on the Obscure](https://pmc.ncbi.nlm.nih.gov/articles/PMC7540309/)
