---
title: "[빛에서 픽셀까지 004] Newton의 프리즘 실험은 흰빛의 스펙트럼을 어떻게 드러냈는가"
categories: [Graphics/Series/Light-To-Pixel]
tags: ["Graphics", "Light", "Spectrum", "Prism", "Dispersion", "Newton"]
series: graphics-foundations
series_title: "빛에서 픽셀까지"
series_url: "/category/graphics/series/light-to-pixel/"
series_id: G004
series_order: 4
---

> 핵심 요약
> - 프리즘은 흰빛에 새로운 색을 칠하는 도구가 아니다. 흰빛에 함께 들어 있던 성분들이 유리에서 서로 다르게 굴절되기 때문에 공간적으로 갈라져 보인다.
> - Newton은 첫 번째 프리즘으로 나뉜 빛의 일부를 같은 조건으로 두 번째 프리즘에 통과시켜, 각 성분의 굴절 성질과 색이 계속 유지된다는 것을 보였다. 분리한 성분을 다시 모으면 흰빛에 가까운 빛으로 돌아왔다.
> - 현대 그래픽스는 이 관계를 파장 `λ`에 따른 분포 `S(λ)`와 파장별 굴절률 `n(λ)`로 표현한다. RGB는 이 연속적인 빛을 화면에 담기 위한 이후 단계의 표현이다.

[앞 글](/graphics/series/light-to-pixel/What-Is-Light-And-Why-Graphics-Uses-Rays/)에서는 빛의 진행 방향을 광선으로 나타내면 교차, 가시성과 경로를 계산하기 쉬워진다고 설명했다. 하지만 시작점 `O`와 방향 `D`만 있는 광선은 그 경로를 따라 **어떤 빛**이 이동하는지 말해 주지 않는다.

흰 손전등을 유리 프리즘에 비추면 벽에 빨강부터 보라까지 이어지는 색띠가 나타난다. 여기에는 서로 다른 두 설명이 가능하다.

> - 프리즘이 들어온 흰빛을 변화시켜 여러 색을 만든 것일까?
> - 아니면 흰빛 안에 이미 있던 성분을 서로 다른 방향으로 갈라놓은 것일까?

이 차이는 그래픽스에서도 중요하다. 프리즘이 색을 새로 만든다면 재질 경계에서 색을 생성하는 규칙이 필요하다. 반대로 기존 성분을 분리한 것이라면 광선이 운반하는 빛을 성분별로 기록하고, 각 성분의 경로를 다르게 계산해야 한다.

## 둥근 빛이 길게 늘어난 것이 첫 번째 문제였다

Newton의 출발점은 무지개를 감상하는 일이 아니라 광학 기구의 화질 문제였다. 그는 망원경에 사용할 렌즈를 다듬으며, 렌즈의 곡면을 더 정확히 만들면 흐린 상을 개선할 수 있다고 생각했다.

[Newton이 1672년 Royal Society에 보낸 보고](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00006)에 따르면 그는 1666년 어두운 방의 창문 덧문에 작은 둥근 구멍을 만들고, 그 구멍으로 들어온 햇빛을 삼각 유리 프리즘에 통과시켰다. 둥근 구멍으로 들어온 태양의 상이라면 굴절된 뒤에도 대체로 둥근 형태가 옆으로 이동할 것이라고 예상할 수 있었다.

그런데 반대편 벽에는 둥근 흰 점이 아니라 길게 늘어난 색상이 나타났다. Newton은 이 **예상보다 긴 상**을 단순한 프리즘 흠집, 태양의 크기나 입사각 차이로 설명할 수 있는지 먼저 검사했다. 프리즘을 바꾸고 돌려도 길쭉한 형태가 유지됐고, 측정한 길이는 당시의 단순한 굴절 계산으로 예상한 범위를 크게 벗어났다.

이 장면에서 중요한 것은 색 이름보다 형태다. 만약 들어온 모든 빛이 같은 정도로 굴절한다면 둥근 상 전체가 함께 움직여야 한다. 길게 늘어났다는 것은 한 묶음처럼 보였던 빛이 서로 다른 각도로 나뉘었다는 단서였다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/unexpected-oblong-spectrum-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/unexpected-oblong-spectrum.svg" alt="둥근 구멍을 지난 햇빛이 모두 같은 각도로 굴절될 때 예상되는 둥근 상과 프리즘 뒤에서 실제로 관찰된 길쭉한 색 스펙트럼의 비교">
</picture>

*그림 1. 둥근 상이 단순히 이동할 것이라는 예상과 달리, 실제 상은 굴절 방향을 따라 길게 늘어났다. [Newton의 1672년 실험 보고](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00006)의 원리를 바탕으로 재구성. 직접 제작.*

## 한 번의 프리즘만으로는 두 설명을 구분할 수 없었다

길어진 색띠를 보았다고 곧바로 `흰빛은 여러 성분의 혼합이다`라고 결론 내릴 수는 없다. 당시에도 굴절이나 유리와의 상호작용이 균일한 흰빛을 변형해 색을 만든다는 설명이 가능했다.

| 가능한 설명 | 첫 번째 프리즘에서 일어난 일 | 두 번째 프리즘에서 예상할 결과 |
| --- | --- | --- |
| **변형 설명** | 유리가 흰빛에 서로 다른 색 성질을 새로 부여한다 | 다시 굴절하면 다른 색으로 더 변하거나 원래 상태로 돌아갈 수 있다 |
| **분리 설명** | 흰빛에 섞여 있던 서로 다른 굴절 성분이 갈라진다 | 선택한 성분은 다시 굴절해도 고유한 색과 굴절 경향을 유지한다 |

[Robert Hooke가 1672년에 제출한 비판](https://newtonproject.ox.ac.uk/view/texts/normalized/NATP00005)도 첫 프리즘에서 나타난 현상 자체보다 그 현상이 Newton의 설명만을 유일하게 증명하는지 문제를 제기했다. 이 반론은 단순한 방해가 아니었다. 같은 관찰을 설명하는 가설이 둘 이상이라면, 두 가설이 서로 다른 결과를 예측하는 실험이 더 필요하다.

Newton은 이 구분을 위해 자신이 `Experimentum Crucis`, 즉 **결정적 실험**이라고 부른 구성을 사용했다.

## 두 번째 프리즘은 색이 어디에서 왔는지 시험했다

실험의 핵심은 첫 번째 프리즘이 만든 색띠 전체를 그대로 두 번째 프리즘에 넣지 않는 것이다. 그러면 두 번째 프리즘에서도 다시 색띠가 보일 뿐, 각 성분이 원래부터 달랐는지 알기 어렵다.

Newton은 두 개의 판에 작은 구멍을 뚫어 빛의 입사 경로를 고정했다. 첫 번째 프리즘을 천천히 돌리면 길쭉한 색띠의 서로 다른 부분이 같은 구멍을 차례로 통과한다. 선택된 좁은 빛은 고정된 두 번째 프리즘에 같은 입사 조건으로 들어간다.

[1672년 보고의 Experimentum Crucis 부분](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00006)은 첫 번째 프리즘에서 더 크게 굴절된 쪽의 빛이 두 번째 프리즘에서도 더 크게 굴절됐다고 기록한다. 구멍과 두 번째 프리즘이 고정되어 입사 조건은 같은데도 도착 위치가 달라졌으므로, 차이는 단순히 `프리즘의 어느 부분을 지났는가`만으로 설명되지 않았다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/experimentum-crucis-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/experimentum-crucis.svg" alt="첫 프리즘에서 분리된 빨간색과 보라색 성분을 같은 구멍과 두 번째 프리즘에 통과시켰을 때 보라색 성분이 더 크게 굴절되는 결정적 실험">
</picture>

*그림 2. 같은 구멍과 같은 두 번째 프리즘을 사용해 입사 조건을 통제해도, 첫 프리즘에서 더 크게 꺾인 성분은 다시 더 크게 꺾였다. [Royal Society가 보관한 1672년 실험 도해](https://pictures.royalsociety.org/image-rs-15005)와 Newton의 설명을 바탕으로 재구성. 직접 제작.*

이 실험은 오늘날의 말로 다음 두 관계를 분리해 확인한 것이다.

- **색띠에서의 위치**는 첫 번째 프리즘이 성분을 갈라놓은 결과다.
- **다시 굴절되는 정도**는 선택한 성분이 가진 광학적 관계와 연결된다.

Newton은 잘 분리한 색광을 다른 프리즘, 반사체와 매질에 통과시키는 실험도 이어 갔다. 밝기는 약해지거나 다른 빛과 섞여 달라질 수 있었지만, 충분히 분리된 성분을 단순히 다시 굴절한다고 해서 빨강이 보라로 바뀌지는 않았다. 프리즘은 색을 덧칠하는 장치라기보다 서로 다른 굴절 성분을 공간적으로 펼치는 장치에 가까웠다.

## 분리된 빛을 다시 모으면 흰빛으로 돌아왔다

분리 설명에는 반대 방향의 검증도 필요하다. 정말 흰빛이 여러 성분의 혼합이라면, 프리즘으로 펼친 빛을 다시 한곳에 모았을 때 흰빛에 가까운 결과가 나와야 한다.

Newton은 프리즘 뒤의 여러 색광을 렌즈로 모아 한 지점에 겹쳤다. [1672년 보고의 재결합 실험](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00006)에서는 색들이 모이는 위치에서 다시 흰빛이 나타나고, 그 지점을 지난 뒤에는 색들의 순서가 뒤집혀 다시 갈라지는 과정을 설명한다.

모든 성분을 적절한 비율로 모았을 때는 흰빛이 되었지만, 중간에서 한 성분을 가리면 결과는 더 이상 같은 흰빛이 아니었다. 이는 흰빛이 하나의 `흰 파장`이 아니라 여러 성분의 조합이라는 설명을 강화한다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/separate-and-recombine-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/separate-and-recombine.svg" alt="프리즘이 흰빛을 여러 색 성분으로 분리하고 렌즈가 모든 성분을 다시 모으면 흰빛이 되지만 일부 성분을 차단하면 다른 색의 빛이 되는 과정">
</picture>

*그림 3. 분리된 모든 성분을 다시 겹치면 흰빛에 가까워지고, 일부를 제외하면 조합의 결과가 달라진다. [Newton의 1672년 재결합 실험](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00006)을 바탕으로 재구성. 직접 제작.*

여기서 빛의 혼합과 물감의 혼합을 같은 현상으로 생각하면 안 된다. 빛을 겹치는 것은 눈으로 들어오는 에너지를 더하는 과정이고, 물감을 섞는 것은 각 안료가 흡수하고 남기는 성분을 바꾸는 과정이다. 가산 혼합과 감산 혼합의 차이는 뒤의 별도 글에서 자세히 다룬다.

## 일곱 색은 일곱 개의 물리적 칸이 아니다

무지개는 흔히 빨강, 주황, 노랑, 초록, 파랑, 남색, 보라의 일곱 칸으로 그려진다. 하지만 Newton의 결론도 빛이 정확히 일곱 종류의 조각으로만 구성됐다는 뜻은 아니었다.

1672년 보고는 대표적인 색 이름들과 함께 그 사이에 불특정하게 많은 중간 단계가 있다고 설명한다. [1704년 『Opticks』](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00033)에서는 색의 원을 일곱 구간으로 나누고 음계의 간격과 대응시켰지만, 이것은 연속적인 색띠에 이름과 비율을 부여한 모델이었다.

색 이름은 연속적인 변화를 대화하기 쉽게 나눈 경계다. `초록이 끝나는 정확한 한 줄 다음부터 파랑이 시작한다`는 물리적 절단면이 프리즘 안에 들어 있는 것은 아니다.

이 점을 놓치면 스펙트럼을 다음처럼 잘못 이해하기 쉽다.

- 흰빛은 빨강·초록·파랑 세 광선만을 포함한다.
- 프리즘은 일곱 종류의 색광만 분리한다.
- 한 색 이름에는 언제나 정확히 하나의 파장만 대응한다.

이 셋은 모두 일반적인 스펙트럼을 지나치게 단순화한 설명이다. RGB가 왜 유용한지는 빛의 물리적 성분 수가 세 개라서가 아니라, 뒤에서 살펴볼 사람의 색 지각과 디스플레이 구조에 관계된다.

## 현대 광학은 파장에 따른 굴절률로 설명한다

Newton은 전자기파나 나노미터 단위의 파장을 알지 못했다. 그는 빛 성분마다 서로 다른 `굴절 가능성`, 즉 Refrangibility가 있다고 표현했다. 현대 광학은 같은 현상을 매질의 굴절률이 파장에 따라 달라지는 관계로 나타낸다.

공기에서 유리로 들어가는 한 경계의 굴절은 Snell의 법칙으로 쓸 수 있다.

```text
n₁(λ) sin θ₁ = n₂(λ) sin θ₂
```

- `λ`: 빛의 파장
- `n₁(λ)`, `n₂(λ)`: 두 매질의 파장별 굴절률
- `θ₁`: 입사 광선과 표면 법선 사이의 각도
- `θ₂`: 굴절 광선과 표면 법선 사이의 각도

이 식에서 입사각 `θ₁`이 같아도 굴절률 `n(λ)`이 파장에 따라 달라지면 굴절각 `θ₂`도 달라진다. 보통의 가시광 영역에서 정상 분산을 보이는 유리는 짧은 파장 쪽의 굴절률이 더 큰 편이므로 보라 쪽 성분이 빨강 쪽 성분보다 더 크게 편향된다.

프리즘은 평행한 유리판과 달리 들어가는 면과 나오는 면이 기울어져 있다. 첫 번째 경계에서 생긴 파장별 방향 차이가 두 번째 경계에서 상쇄되지 않고 더 벌어지기 때문에 벽에서 연속적인 색띠로 보인다. 이 현상을 **분산, Dispersion**이라고 한다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/wavelength-dependent-dispersion-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/wavelength-dependent-dispersion.svg" alt="같은 방향으로 프리즘에 들어온 빨강 초록 보라 성분이 파장별 굴절률 차이 때문에 서로 다른 각도로 나가며 보라색이 가장 크게 편향되는 과정">
</picture>

*그림 4. 입사 경로가 같아도 파장별 굴절률 `n(λ)`가 다르면 출사 방향이 갈라진다. 정상 분산을 보이는 일반적인 유리에서는 보라 쪽 성분의 굴절률과 전체 편향이 빨강 쪽보다 크다. 개념도, 직접 제작.*

[PBRT 4판의 굴절과 분산 설명](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)은 굴절률의 가시광 영역 변화가 몇 퍼센트에 불과해도 렌더링된 유리에서 눈에 보이는 색 분리를 만들 수 있다고 설명한다. 따라서 유리를 하나의 고정 굴절률로 계산하면 투명한 형태는 만들 수 있어도 프리즘의 색 분산은 재현할 수 없다.

## 스펙트럼은 파장마다 얼마가 있는지를 나타내는 함수다

현대 그래픽스에서 스펙트럼은 색 이름의 목록이 아니라 파장 `λ`에 따라 어떤 물리량이 얼마나 있는지를 나타내는 분포다. 이를 일반적인 기호로 다음처럼 쓸 수 있다.

```text
S(λ) = 파장 λ에서의 양
```

`S`가 무엇을 뜻하는지는 문맥에 따라 달라진다. 광원이 방출하는 양일 수도 있고, 표면이 반사하는 비율이나 카메라 센서의 반응일 수도 있다. 핵심은 하나의 `흰색` 숫자 대신 파장에 따라 값이 달라지는 함수로 빛과 재질을 표현한다는 점이다.

[PBRT의 Radiometry, Spectra, and Color 장](https://www.pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color)은 사람이 볼 수 있는 전자기 복사 범위를 대략 `380 nm`에서 `780 nm`로 두고, 파장에 따른 물리량의 변화를 Spectral Distribution으로 정의한다. 경계 값은 문헌과 관찰 조건에 따라 조금씩 다르게 제시되므로 절대적인 칼선이라기보다 실용적인 범위로 이해하는 편이 좋다.

연속 함수를 컴퓨터에서 무한히 저장할 수는 없다. 스펙트럼 렌더러는 파장 구간을 촘촘하게 저장하거나, 몇 개의 파장을 표본화해 전체 적분을 추정한다. [PBRT의 스펙트럼 표현](https://www.pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Representing_Spectral_Distributions)도 연속적인 분포를 조각별 선형 함수 또는 선택한 파장의 Sample로 계산한다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/spectral-distribution-rendering-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/spectral-distribution-rendering.svg" alt="연속적인 가시광 스펙트럼 S 람다를 여러 파장에서 표본화하고 광원, 재질 반사, 파장별 굴절을 거쳐 최종 RGB 픽셀로 변환하는 흐름">
</picture>

*그림 5. 스펙트럼은 일곱 색 칸이 아니라 파장별 양의 연속적인 분포이며, 렌더러는 필요한 파장을 Sample해 빛의 이동을 계산한 뒤 표시용 색으로 변환한다. 개념도, 직접 제작.*

## 광선의 방향만으로는 색을 운반할 수 없다

앞 글의 광선 식은 한 경로의 위치를 계산했다.

```text
P(t) = O + tD
```

프리즘과 스펙트럼을 다루려면 여기에 파장별 빛의 양과 파장에 따라 달라질 수 있는 방향을 함께 생각해야 한다.

- **광원**은 파장별로 서로 다른 양의 빛을 방출할 수 있다.
- **표면**은 파장별로 일부를 더 반사하고 일부를 더 흡수할 수 있다.
- **투명 매질**은 파장별 굴절률 `n(λ)` 때문에 서로 다른 방향으로 빛을 보낼 수 있다.
- **센서와 눈**은 같은 스펙트럼에도 파장별로 다르게 반응한다.

같은 `O`와 `D`를 가진 광선이라도 따뜻한 백열등의 빛, 푸른 하늘빛과 좁은 파장대의 빛을 모두 운반할 수 있다. 기하 정보가 같다는 사실은 빛의 구성까지 같다는 뜻이 아니다. 따라서 렌더러는 광선의 경로와 함께 파장별 양 `S(λ)` 또는 이를 근사한 색 정보를 별도의 **운반 정보**로 유지해야 한다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/ray-geometry-and-spectral-payload-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g004-newton-prism-spectrum/ray-geometry-and-spectral-payload.svg" alt="시작점 O와 방향 D만 있는 기하 광선은 이동 위치만 나타내며 스펙트럼 S 람다를 함께 가진 광선은 파장별 빛의 양과 분산 뒤의 방향 D 람다까지 계산할 수 있음을 비교">
</picture>

*그림 6. `O`와 `D`는 광선이 어디를 지나는지 알려 주고, `S(λ)`는 그 경로로 어떤 빛이 얼마나 이동하는지 알려 준다. 분산이 일어나면 하나였던 경로도 파장에 따른 `D(λ)`로 갈라진다. 개념도, 직접 제작.*

분산이 없다면 여러 파장 Sample을 하나의 광선 경로에 묶어 계산할 수 있다. 하지만 프리즘처럼 파장마다 굴절 방향이 달라지면 광선의 방향도 사실상 `D(λ)`가 된다. [PBRT의 스펙트럼 구현](https://www.pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Representing_Spectral_Distributions)은 이런 분산 사건 뒤에는 여러 파장을 한 광선으로 계속 추적할 수 없으므로 경로에서 특정 파장을 선택해 이어 가는 방법을 사용한다.

많은 실시간 렌더러는 성능을 위해 빛과 재질을 처음부터 RGB 세 값으로 계산한다. 대부분의 화면에서는 매우 효율적이고 충분히 좋은 선택이다. 그러나 RGB 세 값만으로는 원래의 연속 스펙트럼을 하나로 복원할 수 없기 때문에, 파장별 굴절이나 복잡한 조명·재질 조합에서는 스펙트럼 렌더링이 더 자연스러운 결과를 만들 수 있다.

## Newton이 해결한 것과 아직 남은 것

Newton의 실험이 현대 빛 이론 전체를 완성한 것은 아니다. 그는 파장이나 전자기장을 사용하지 않았고 빛의 본성에 대해서는 입자적 설명을 선호했다. 이후의 파동광학과 양자 이론은 그 물리적 해석을 크게 확장했다.

그럼에도 프리즘 실험에서 확립된 다음 구조는 오늘날에도 그대로 중요하다.

1. 흰빛은 광학적으로 서로 다르게 행동하는 성분을 포함한다.
2. 투명 매질은 그 성분을 새로 칠하기보다 파장별 굴절 차이로 분리할 수 있다.
3. 분리된 성분을 적절히 다시 모으면 흰빛에 가까운 조합으로 돌아간다.
4. 빛과 재질의 색을 정확히 계산하려면 파장별 분포를 생각해야 한다.

하지만 스펙트럼을 안다고 물체의 색이 자동으로 결정되는 것은 아니다. 빛이 물질에 닿았을 때 어떤 파장은 반사되고, 어떤 파장은 안으로 들어가거나 흡수되며, 어떤 빛은 여러 방향으로 흩어진다. 같은 광원의 스펙트럼도 물질과 만난 뒤에는 전혀 다른 분포가 될 수 있다.

## 정리

- Newton은 둥글 것으로 예상한 태양의 상이 프리즘 뒤에서 길게 늘어나는 현상에서 출발했다.
- 첫 프리즘만으로는 유리가 색을 만든다는 설명과 흰빛의 성분을 분리한다는 설명을 구분할 수 없었다.
- Experimentum Crucis는 같은 입사 조건에서도 선택한 성분에 따라 두 번째 굴절량이 다르고 색이 유지된다는 점을 보였다.
- 분리된 성분을 다시 모으면 흰빛에 가까워졌고, 일부를 제외하면 조합의 색이 달라졌다.
- 일곱 색 이름은 연속 스펙트럼을 나눈 언어이지, 빛이 정확히 일곱 종류로만 구성됐다는 뜻이 아니다.
- 현대 그래픽스는 스펙트럼을 `S(λ)`, 분산을 파장별 굴절률 `n(λ)`로 나타내며 필요에 따라 여러 파장을 Sample한다.
- RGB는 물리적인 스펙트럼 자체가 아니라, 그 빛을 사람과 디스플레이에 맞게 표현하는 이후 단계의 압축된 색 표현이다.

빛이 여러 파장 성분을 가진다는 사실을 알았으니, 다음 질문은 그 빛이 물질에 닿았을 때 무엇이 남는가다. 다음 글에서는 **반사, 굴절, 흡수와 산란**이 한 번의 빛–물질 상호작용에서 어떻게 갈라지며, 이 구분이 재질과 셰이딩에 왜 필요한지 살펴본다.

## 참고

- [Isaac Newton, A Letter Containing His New Theory about Light and Colors, 1672 — Newton Project](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00006)
- [Newton의 1672년 New Theory about Light and Colours 원고 — Royal Society Archive](https://makingscience.royalsociety.org/items/rbo_4_44/a-discourse-of-mr-isaac-newton-containing-his-new-theory-about-light-and-colours-sent-by-him-from-cambridge-february-6-1672)
- [Newton의 Experimentum Crucis 도해 — Royal Society Picture Library](https://pictures.royalsociety.org/image-rs-15005)
- [Robert Hooke, Critique of Newton's Theory of Light and Colors, 1672 — Newton Project](https://newtonproject.ox.ac.uk/view/texts/normalized/NATP00005)
- [Isaac Newton, Opticks, Book I Part I, 1704 — Newton Project](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00033)
- [Isaac Newton, Opticks, Book I Part II, 1704 — Newton Project](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00034)
- [Physically Based Rendering, 4th Edition — Radiometry, Spectra, and Color](https://www.pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color)
- [Physically Based Rendering, 4th Edition — Representing Spectral Distributions](https://www.pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Representing_Spectral_Distributions)
- [Physically Based Rendering, 4th Edition — Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)
