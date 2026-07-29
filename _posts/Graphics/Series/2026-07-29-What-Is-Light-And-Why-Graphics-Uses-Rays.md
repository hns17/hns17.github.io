---
title: "[빛에서 픽셀까지 003] 빛은 무엇이며 어떻게 이동하고 그래픽스에서는 왜 광선으로 다루는가"
categories: [Graphics/Series/Light-To-Pixel]
tags: ["Graphics", "Light", "Wave", "Photon", "Ray", "Geometric Optics"]
series: graphics-foundations
series_title: "빛에서 픽셀까지"
series_url: "/category/graphics/series/light-to-pixel/"
series_id: G003
series_order: 3
---

> 핵심 요약
> - 현실의 빛은 전자기파이며 물질과 에너지를 주고받을 때는 광자라는 양자적 성질도 드러난다. 파동, 광자와 광선은 서로 경쟁하는 그림이 아니라 서로 다른 질문에 답하는 모델이다.
> - 보통의 3D 장면은 빛의 파장보다 훨씬 크므로, 회절과 간섭을 잠시 생략하고 빛이 진행하는 방향을 광선으로 나타내는 기하광학이 효과적이다.
> - 광선은 시작점과 방향으로 정의되어 교차, 가시성, 반사와 굴절을 계산하기 쉽다. 다만 광선 자체가 작은 빛 알갱이의 실제 궤적은 아니다.

[앞 글](/graphics/series/light-to-pixel/Lighting-Shading-Shadow/)에서는 그림자를 판단할 때 표면에서 광원으로 `Shadow Ray`를 보내 가려졌는지 검사한다고 설명했다. 그런데 현실의 방 안을 들여다보면 광원과 표면 사이에 노란 선이 그어져 있지는 않다.

손전등 빛은 곧게 나아가는 것처럼 보인다. 아주 좁은 틈을 지나면 퍼지고, 두 빛이 겹치면 밝고 어두운 무늬가 생길 수 있다. 카메라 센서는 연속적인 물결을 그대로 저장하기보다 흡수한 빛에 따라 전기 신호를 만든다.

빛은 선일까, 파동일까, 입자일까? 그래픽스가 이 질문에 답하려면 먼저 **어떤 현상을 계산하려는가**를 정해야 한다.

## 하나의 빛을 세 가지 모델로 본다

모델은 현실 그 자체가 아니라, 필요한 관계를 남기고 나머지를 잠시 생략한 설명 도구다. 지도에서 지하철 노선만 보고도 환승 경로를 찾을 수 있지만 건물의 실제 크기까지 알 수는 없는 것과 비슷하다.

| 모델 | 잘 설명하는 질문 | 주로 생략하는 것 |
| --- | --- | --- |
| 전자기파 | 빛이 어떻게 전파되고 간섭·회절·편광하는가 | 개별 검출에서 드러나는 양자적 사건 |
| 광자 | 물질이 빛의 에너지를 어떤 단위로 흡수·방출하는가 | 장면 전체의 경로를 직관적으로 계산하는 기하 |
| 광선 | 어느 방향으로 진행해 무엇과 만나고 가려지는가 | 파동의 위상, 회절과 간섭 |

세 모델의 역할을 먼저 나란히 보면 그래픽스가 물리학을 무시해서 광선을 쓰는 것이 아니라, 장면을 그리는 데 필요한 질문에 맞춰 표현을 고른다는 점이 보인다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g003-light-and-rays/models-of-light-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g003-light-and-rays/models-of-light.svg" alt="같은 빛을 전자기파, 광자와 광선 모델로 나누어 각각 설명할 수 있는 현상을 비교한 도해">
</picture>

*그림 1. 파동, 광자와 광선은 서로 하나를 폐기하는 답이 아니라 관찰할 현상과 계산 규모에 따라 선택하는 설명이다. 직접 제작.*

이 글의 목표는 양자전기역학을 모두 설명하는 것이 아니다. 빛의 여러 모습 가운데 일반적인 렌더링이 왜 **경로와 가시성**을 잘 나타내는 광선 모델에서 출발하는지 이해하는 데 있다.

## 빛의 정체를 둘러싼 논쟁은 한쪽의 완승으로 끝나지 않았다

빛을 작은 입자의 흐름으로 볼 것인지 파동으로 볼 것인지는 오랫동안 경쟁하는 설명처럼 여겨졌다. 그러나 새로운 실험은 한 그림만으로 모든 현상을 설명하기 어렵다는 사실을 반복해서 보여 주었다.

[Thomas Young의 1802년 Bakerian Lecture](https://doi.org/10.1098/rstl.1802.0004)는 빛의 두 부분이 겹칠 때 서로 강화되거나 약화되는 간섭 원리로 여러 광학 현상을 연결했다. 1804년의 [후속 실험 보고](https://doi.org/10.1098/rstl.1804.0001)는 그림자 가장자리의 색 띠를 이용해 빛의 간섭을 실험적으로 제시했다. 빛을 독립된 알갱이의 직선 운동만으로 생각하면 이런 밝고 어두운 무늬를 설명하기 어렵다.

[James Clerk Maxwell의 1865년 논문 *A Dynamical Theory of the Electromagnetic Field*](https://doi.org/10.1098/rstl.1865.0008)은 전기와 자기 현상을 하나의 장 이론으로 연결하고, 그 이론에서 나오는 전자기적 교란의 전파 속도가 알려진 빛의 속도와 일치한다는 점에서 빛을 전자기적 교란으로 해석했다. [Heinrich Hertz의 1888년 실험 보고](https://doi.org/10.1002/andp.18882700708)는 전자기 작용이 공간을 통해 파동으로 전파된다는 예측을 실험으로 뒷받침했다.

그렇다고 파동 설명만으로 끝난 것도 아니다. [Albert Einstein의 1905년 논문](https://doi.org/10.1002/andp.19053220607)은 빛의 에너지가 공간에 연속적으로 퍼져 있다는 고전적 그림만으로 설명하기 어려운 광전 효과를 다루며, 빛 에너지가 독립적인 양자 단위로 전달될 수 있다고 제안했다.

여기서 중요한 결론은 `빛은 사실 파동이다` 또는 `빛은 사실 입자다` 가운데 하나를 고르는 것이 아니다.

> 빛은 전자기장으로 전파되며, 물질과 상호작용할 때 양자적인 에너지 교환을 보인다. 어떤 실험을 설명하는지에 따라 필요한 모델의 해상도가 달라진다.

그래픽스의 광선도 이 역사에서 살아남은 세 번째 실체가 아니다. 파동의 진행을 장면 규모에서 다루기 쉽게 축약한 **기하광학의 계산 도구**다.

## 파동 모델은 무엇이 이동하는지를 설명한다

진공에서 빛은 서로 연결된 전기장과 자기장의 변화가 공간을 따라 전파되는 전자기파로 설명된다. 밧줄 조각이 출발점에서 도착점까지 날아가는 것처럼 물질 덩어리가 이동하는 것은 아니다. 공간의 장 상태와 에너지가 전파된다.

파동을 나타내는 가장 기본적인 두 값은 다음과 같다.

- **파장 `λ`**: 같은 위상 상태가 공간에서 반복되는 거리
- **진동수 `ν`**: 한 지점에서 1초 동안 반복되는 진동 횟수

진공에서는 두 값이 다음 관계를 가진다.

`c = λν`

`c`는 진공에서의 빛의 속도다. [NIST의 SI 상수 설명](https://www.nist.gov/si-redefinition/meet-constants)에 따르면 이 값은 정확히 `299,792,458 m/s`로 정의되어 있다. 진동수가 높으면 같은 속도로 이동하는 동안 한 번의 진동이 차지하는 거리가 짧아지므로 파장도 짧아진다.

다만 렌더러가 벽 하나를 비출 때마다 전기장과 자기장의 빠른 진동을 직접 계산한다면 다뤄야 할 공간과 시간의 해상도가 지나치게 작아진다. 일반적인 장면의 표면과 물체는 가시광선의 파장보다 매우 크다. 이 크기 차이가 광선 근사를 가능하게 한다.

## 광선은 파동을 버리는 것이 아니라 진행 방향만 남긴다

파동에서 같은 위상을 가진 지점들을 이은 면을 **파면**이라고 한다. 균일한 매질에서 파면이 앞으로 이동할 때 그 면에 수직인 방향을 따라 선을 그리면 빛의 진행 방향을 나타내는 광선이 된다.

[PBRT 4판의 Radiometry 절](https://pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Radiometry)은 물체의 크기가 빛의 파장보다 훨씬 큰 거시적 장면에서는 기하광학 수준의 복사 전달 모델이 적합하다고 설명한다. 파동의 매 순간을 계산하는 대신 광선을 따라 에너지가 어느 방향으로 전달되는지 다루는 것이다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g003-light-and-rays/wavefront-to-ray-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g003-light-and-rays/wavefront-to-ray.svg" alt="파면의 수직 방향에서 광선을 얻고 시작점과 방향 벡터로 광선 위의 점을 나타내는 과정">
</picture>

*그림 2. 기하광학은 파면의 세밀한 진동 대신 진행 방향을 광선으로 남기고, 렌더러는 그 선 위의 점을 매개변수로 계산한다. 직접 제작.*

이 근사가 잘 작동하는 조건은 단순히 `빛은 언제나 직진한다`가 아니다.

- 매질이 균일하면 광선은 곧게 진행한다고 볼 수 있다.
- 서로 다른 매질의 경계에서는 반사되거나 굴절되어 방향이 바뀐다.
- 연기, 안개나 불균일한 매질에서는 진행 중 흡수·산란되거나 경로가 휠 수 있다.
- 틈이나 표면 구조의 크기가 파장과 비슷해지면 회절과 간섭처럼 광선만으로 설명하기 어려운 현상이 커진다.

즉 광선은 현실의 빛이 반드시 자를 대고 그은 선처럼 움직인다는 선언이 아니다. **관심 있는 장면 규모에서 파동 효과를 생략해도 경로 계산이 충분히 정확하다**는 가정이다.

## 광선 하나는 시작점과 방향으로 정의된다

렌더러에서 광선은 보통 시작점 `O`와 방향 벡터 `D`로 정의한다. 광선 위의 점 `P(t)`는 다음처럼 나타낼 수 있다.

`P(t) = O + tD,  t ≥ 0`

| 기호 | 의미 |
| --- | --- |
| `O` | 광선이 시작하는 3D 위치 |
| `D` | 광선이 나아가는 방향 |
| `t` | 시작점에서 광선을 따라 얼마나 진행했는지 나타내는 매개변수 |
| `P(t)` | 주어진 `t`에서 광선이 지나는 위치 |

`D`를 길이 1로 정규화했다면 `t`를 장면의 거리처럼 사용할 수 있다. 정규화하지 않았다면 `t`는 단순한 비율 매개변수이므로 실제 거리와 같다고 가정하면 안 된다.

[PBRT의 Rays 절](https://www.pbr-book.org/4ed/Geometry_and_Transformations/Rays)도 광선을 시작점과 방향으로 정해지는 반직선으로 정의하고 같은 매개변수 형태를 사용한다. 이 표현이 강력한 이유는 그래픽스의 여러 질문을 하나의 기하 문제로 바꿀 수 있기 때문이다.

- 카메라 광선과 가장 먼저 만나는 삼각형은 무엇인가?
- 표면과 광원 사이의 유한한 구간에 차폐물이 있는가?
- 거울에서 반사된 새 방향은 어느 물체와 만나는가?
- 안개 속 구간을 얼마나 길게 통과했는가?

광선은 색이나 밝기를 스스로 갖는 물체가 아니다. 렌더러가 광선을 따라 스펙트럼이나 복사량을 함께 계산한다. 그 양을 어떤 단위로 나타낼지는 뒤의 Radiometry와 Photometry 글에서 다룬다.

## 카메라에서 출발하는 광선은 Ray Tracing의 계산 전략이다

현실에서는 광원이 매우 많은 방향으로 빛을 내고, 여러 표면을 거친 일부만 카메라 센서의 특정 픽셀에 도달한다. 이 과정을 광원에서 무작정 따라가면 대부분의 경로는 지금 계산하려는 픽셀과 관계가 없다.

그래서 많은 Ray-based Renderer는 먼저 화면의 **Pixel Sample** 하나를 고른다. 그러면 카메라 모델이 카메라의 위치에서 그 Sample을 통과해 장면으로 향하는 **Camera Ray**를 만든다. 흔히 `픽셀에서 광선을 보낸다`고 줄여 말하지만, 광선의 시작점이 픽셀이라는 뜻은 아니다. Pixel Sample은 카메라가 바라볼 방향을 정하고, 광선은 카메라에서 출발한다.

Camera Ray를 장면의 삼각형들과 교차 검사하면 그 방향에서 가장 먼저 보이는 표면을 찾을 수 있다. Ray Tracing에서 `Tracing`은 바로 이렇게 **광선이 장면의 어디와 만나는지 따라가며 검사하는 과정**을 뜻한다. 첫 교차점에서는 광원 쪽으로 `Shadow Ray`를 보내 직접광 경로가 막혔는지 확인하거나, 반사·굴절 방향으로 새 광선을 이어 갈 수도 있다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g003-light-and-rays/camera-first-rays-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g003-light-and-rays/camera-first-rays.svg" alt="광원에서 가능한 모든 경로를 따라가는 방법과 카메라 픽셀에서 필요한 경로를 먼저 찾는 방법의 비교">
</picture>

*그림 3. 카메라에서 시작하는 광선은 빛을 물리적으로 발사하는 것이 아니라, 최종 픽셀에 기여할 가능성이 있는 경로를 먼저 묻는 계산 순서다. 직접 제작.*

[PBRT의 Ray Tracing 소개](https://pbr-book.org/4ed/Introduction/Photorealistic_Rendering_and_the_Ray-Tracing_Algorithm)는 카메라에서 Viewing Ray를 생성하고, 교차점에서 광원 가시성과 표면 산란을 평가하는 흐름을 설명한다. 카메라에서 광선을 보낸다는 표현은 **빛이 실제로 카메라에서 나온다**는 뜻이 아니다. 결과 픽셀에서 원인을 거꾸로 찾는 계산 전략이다.

이 전략도 모든 빛 경로를 자동으로 찾는 것은 아니다. 작은 광원을 여러 번 반사한 뒤 카메라에 도달하는 경로나 유리를 통과해 모인 빛처럼 찾기 어려운 경로가 있다. Path Tracing, Bidirectional Path Tracing과 Photon Mapping은 어떤 경로를 어떤 방향에서 표본화할지 서로 다르게 선택한다. 이 차이는 전역 조명 부분에서 다시 다룬다.

## Rasterization은 광선 대신 모델을 화면에 투영한다

지금까지의 카메라 광선 설명은 **Ray Tracing이라는 특정 렌더링 방식**의 이야기다. `그래픽스는 빛을 광선으로 설명할 수 있다`는 말과 `모든 렌더러가 광선을 장면과 교차 검사한다`는 말은 다르다.

화면의 한 Sample과 장면의 여러 삼각형이 있다고 생각해 보자. Ray Tracing은 카메라에서 그 Sample을 통과하는 광선을 만들고 `이 방향에서 가장 먼저 만나는 삼각형은 무엇인가?`라고 묻는다. 광선과 삼각형의 교차를 추적한 뒤 가장 가까운 Hit를 남긴다.

Rasterization은 Camera Ray를 추적하지 않고 모델 쪽에서 시작한다. 장면의 삼각형 세 정점을 카메라 화면으로 투영한 다음, 화면에 생긴 2D 삼각형이 `어떤 Sample들을 덮는가?`를 찾는다. 여기서 Sample은 픽셀 값을 결정하기 위해 화면을 검사하는 위치다. 한 픽셀 안에 Sample을 하나만 둘 수도 있고 Anti-Aliasing을 위해 여러 개 둘 수도 있다.

두 방식은 모두 `이 Sample에 어떤 표면이 보이는가?`를 해결하지만 **보이는 표면을 찾는 계산 순서**가 다르다.

- Ray Tracing: `카메라 → Pixel Sample 방향의 광선 → 장면과 교차`
- Rasterization: `장면의 삼각형 → 카메라 화면에 투영 → 덮이는 Sample`

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g003-light-and-rays/ray-tracing-rasterization-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g003-light-and-rays/ray-tracing-rasterization.svg" alt="Ray Tracing이 카메라에서 Pixel Sample 방향으로 광선을 만들어 교차점을 추적하는 과정과 Rasterization이 삼각형을 화면에 투영해 덮이는 Sample을 찾는 과정의 비교">
</picture>

*그림 4. Ray Tracing은 카메라에서 Pixel Sample 방향으로 광선을 만들어 교차점을 추적하고, Rasterization은 삼각형을 화면으로 투영해 덮이는 Sample을 찾는다. 두 방식 모두 이후의 조명 계산에서는 빛 방향 벡터를 사용할 수 있다. 직접 제작.*

Rasterization의 흐름을 한 단계씩 풀면 다음과 같다.

1. 3D 삼각형의 세 정점을 카메라 화면의 2D 위치로 투영한다.
2. 투영된 삼각형 내부에 들어오는 화면 Sample을 찾는다.
3. 각 Sample에 대해 깊이, 색, 법선과 텍스처 좌표를 보간해 **Fragment 후보**를 만든다.
4. 여러 삼각형이 같은 Sample을 덮으면 Depth Test가 더 가까운 후보를 남긴다.

Fragment는 `이 Sample에 이 삼각형이 보일 수 있다`는 후보이지, 아직 최종 픽셀과 같은 말은 아니다. 깊이 검사에서 탈락할 수 있고, 투명도와 Blending 같은 뒤 단계에서 다른 결과와 결합될 수도 있다.

따라서 Rasterization은 광선을 사용하지 못해서 생긴 불완전한 방식이 아니다. Pixel Sample마다 Camera Ray와 장면의 교차점을 찾는 대신, 각 삼각형이 영향을 줄 화면 영역을 연속적으로 처리하도록 계산 순서를 바꾼 방식이다.

### 광선을 추적하지 않아도 빛의 방향은 필요하다

여기서 `Rasterization에는 광선이 필요 없다`고만 말하면 또 다른 오해가 생긴다. Rasterization이 사용하지 않는 것은 **보이는 표면을 찾기 위한 Camera Ray의 교차 추적**이다. 화면에 투영된 표면의 밝기를 계산할 때는 여전히 빛과 카메라의 방향이 필요하다.

Lambert 조명을 예로 들면, 표면의 밝기는 법선 `N`과 표면에서 광원으로 향하는 단위 방향 벡터 `L`의 내적으로 계산할 수 있다.

```text
밝기 = max(N · L, 0)
```

두 방향이 가까울수록 표면은 밝고, 빛이 표면 뒤쪽에 있으면 결과를 0으로 제한한다. 이 계산에 사용하는 `L`은 빛이 들어오는 **방향을 나타내는 벡터**다. 하지만 렌더러가 그 방향을 따라 장면의 물체들과 실제로 교차 검사하는 것은 아니므로, 이것만으로는 Ray Tracing이라고 부르지 않는다.

일반적인 Raster Renderer는 조명을 계산할 때 다음과 같은 기하광학의 방향 관계를 사용한다.

- 표면에서 광원으로 향하는 Light Direction `L`
- 표면에서 카메라로 향하는 View Direction `V`
- 반사 방향 `R`과 Blinn–Phong의 Half Vector `H`
- 광원에서 본 깊이를 비교해 가려짐을 근사하는 Shadow Map

방향 벡터는 `어느 쪽인가`를 알려 준다. 반면 Ray Tracing의 광선은 시작점 `O`와 방향 `D`를 가진 `P(t) = O + tD`를 장면과 교차 검사하여 `그 길에서 무엇을 만나는가`까지 확인한다.

따라서 **Rasterization은 모델을 투영해 보이는 표면을 찾고**, **Ray Tracing은 광선을 추적해 보이는 표면과 추가 경로를 찾는다**. 둘 다 Lambert, Blinn–Phong 같은 조명 계산에 빛 방향 벡터를 사용할 수 있다. 여기에 Rasterization으로 기본 화면을 만들고 그림자나 반사에만 Ray를 추적하면 Hybrid Rendering이 된다.

## 광선 모델이 놓치는 현상도 화면에 필요할 수 있다

기하광학은 매우 유용하지만 만능은 아니다.

| 화면에 필요한 현상 | 광선만으로 부족한 이유 | 필요한 확장 |
| --- | --- | --- |
| 아주 좁은 틈 뒤로 빛이 퍼지는 회절 | 빛이 경계에서 단순히 직진한다고 가정함 | 파동광학 |
| 얇은 막이나 미세 구조의 색 변화 | 파동의 위상 차이를 저장하지 않음 | 간섭·스펙트럼 모델 |
| 편광 필터와 결정의 방향성 | 일반적인 광선이 전기장의 진동 방향을 생략함 | 편광을 포함한 광 전달 |
| 저조도 센서의 Shot Noise | 연속적인 빛의 양만으로 개별 검출 사건을 생략함 | 광자 통계와 센서 모델 |

최근의 물리 기반 렌더러는 필요에 따라 광선에 파장, 편광이나 위상에 관한 정보를 더하거나 별도의 파동 시뮬레이션을 사용한다. 그러나 모든 장면에서 가장 미세한 모델을 쓰는 것이 항상 좋은 선택은 아니다. 설명하려는 현상보다 훨씬 작은 규모까지 계산하면 비용만 커지고 결과 차이는 보이지 않을 수 있다.

렌더링 모델을 고르는 기준은 `가장 물리적으로 복잡한가`가 아니라 다음 질문에 가깝다.

> 최종 이미지에서 구분해야 할 현상을 보존하면서, 어떤 세부를 안전하게 생략할 수 있는가?

## 정리

- 빛은 전자기파로 전파되며 물질과의 에너지 교환에서는 광자라는 양자적 성질이 드러난다.
- 파동, 광자와 광선은 같은 현상을 서로 다른 해상도로 설명하는 모델이며, 어느 하나를 모든 상황의 그림으로 사용해서는 안 된다.
- 보통의 3D 장면에서는 물체가 빛의 파장보다 훨씬 크기 때문에 진행 방향만 남긴 기하광학이 효과적이다.
- 렌더러의 광선은 시작점 `O`와 방향 `D`로 정의되는 수학적 반직선이며, 교차와 가시성을 계산하는 도구다.
- Ray Tracing은 카메라에서 Pixel Sample 방향으로 광선을 생성하고 장면과의 교차를 추적해 보이는 표면을 찾는다.
- Rasterization은 모델의 삼각형을 카메라 화면에 투영하고, 덮이는 Sample과 깊이를 검사해 보이는 표면을 찾는다.
- Rasterization도 Lambert 같은 조명 계산에는 빛 방향 벡터를 사용한다. 방향 벡터를 사용하는 것과 광선을 장면과 교차 추적하는 것은 다른 일이다.

광선은 빛이 **어디로 이동하는가**를 간단히 나타내지만, 그 빛이 어떤 색 성분으로 이루어졌는지는 아직 말해 주지 않는다. 다음 글에서는 Newton의 프리즘 실험을 따라가며 하나로 보이던 흰빛이 스펙트럼으로 나뉜다는 사실과, 이것이 그래픽스의 색 표현에 왜 필요한지 살펴본다.

## 참고

- [Thomas Young, The Bakerian Lecture: On the Theory of Light and Colours, 1802](https://doi.org/10.1098/rstl.1802.0004)
- [Thomas Young, Experiments and Calculations Relative to Physical Optics, 1804](https://doi.org/10.1098/rstl.1804.0001)
- [James Clerk Maxwell, A Dynamical Theory of the Electromagnetic Field, 1865](https://doi.org/10.1098/rstl.1865.0008)
- [Heinrich Hertz, Ueber die Ausbreitungsgeschwindigkeit der electrodynamischen Wirkungen, 1888](https://doi.org/10.1002/andp.18882700708)
- [Albert Einstein, Über einen die Erzeugung und Verwandlung des Lichtes betreffenden heuristischen Gesichtspunkt, 1905](https://doi.org/10.1002/andp.19053220607)
- [NIST, Meet the Constants — Speed of Light and Planck Constant](https://www.nist.gov/si-redefinition/meet-constants)
- [Physically Based Rendering, 4th Edition — Radiometry](https://pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Radiometry)
- [Physically Based Rendering, 4th Edition — Rays](https://www.pbr-book.org/4ed/Geometry_and_Transformations/Rays)
- [Physically Based Rendering, 4th Edition — Photorealistic Rendering and the Ray-Tracing Algorithm](https://pbr-book.org/4ed/Introduction/Photorealistic_Rendering_and_the_Ray-Tracing_Algorithm)
