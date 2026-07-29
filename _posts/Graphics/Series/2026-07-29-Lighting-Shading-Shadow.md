---
title: "[빛에서 픽셀까지 002] Lighting, Shading, Shadow는 무엇이 다른가"
categories: [Graphics/Series/Light-To-Pixel]
tags: ["Graphics", "Light", "Lighting", "Shading", "Shadow", "Visibility"]
series: graphics-foundations
series_title: "빛에서 픽셀까지"
series_url: "/category/graphics/series/light-to-pixel/"
series_id: G002
series_order: 2
---

> 핵심 요약
> - Lighting은 광원이 표면을 향해 어떤 빛을 보내는지 설명하는 입력이고, Shading은 그 빛에 표면과 재질이 어떻게 반응해 카메라 방향의 밝기와 색을 만드는지 계산하는 과정이다.
> - Shadow는 광원에서 표면까지의 경로가 가려졌는지를 판단하는 가시성 문제다.
> - 실제 렌더러에서는 세 계산이 한 식이나 Shader 안에서 만날 수 있지만, 원인을 진단하고 기술의 역할을 이해하려면 서로 다른 질문으로 구분해야 한다.

[앞 글](/graphics/series/light-to-pixel/Why-3D-Graphics-Starts-With-Light/)에서는 사람이 색과 명암, 그림자를 단서로 사물의 형태와 위치를 추론하고, 그 단서들이 결국 빛에서 시작한다는 것을 살펴봤다. 이제 장면에 빛을 하나 놓았다고 해 보자.

빛이 있다는 사실만으로 표면의 최종 색은 정해지지 않는다. 같은 빛을 받아도 흰 종이와 검은 플라스틱은 다르게 보이고, 구의 앞면과 옆면은 밝기가 다르다. 그 사이에 다른 물체가 끼어 있으면 빛은 표면까지 도달하지 못한다.

여기에는 서로 다른 세 질문이 숨어 있다.

1. **어떤 빛이 어느 방향과 세기로 표면을 향하는가?**
2. **표면은 그 빛을 카메라 방향으로 어떻게 돌려보내는가?**
3. **빛이 표면까지 오는 길은 열려 있는가?**

이 세 질문에 각각 대응하는 말이 Lighting, Shading, Shadow다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g002-lighting-shading-shadow/three-questions-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g002-lighting-shading-shadow/three-questions.svg" alt="Lighting, Shading과 Shadow가 같은 장면에서 서로 다른 질문을 담당하는 구조">
</picture>

*그림 1. Lighting은 빛의 입력, Shading은 표면의 반응, Shadow는 광원 가시성을 묻는다. 직접 제작.*

## 먼저 세 용어를 한눈에 구분해 보자

| 용어 | 핵심 질문 | 주요 입력 | 알아내는 것 |
| --- | --- | --- | --- |
| **Lighting** | 어떤 빛이 표면을 향하는가 | 광원의 위치·방향·크기·세기·색, 거리 | 차폐 적용 전의 빛 기여 후보 |
| **Shading** | 표면은 그 빛에 어떻게 반응하는가 | 들어오는 빛, 표면 방향, 재질, 관찰 방향 | 카메라 쪽으로 나가는 밝기와 색 |
| **Shadow** | 광원과 표면 사이가 가려졌는가 | 광원, 표면 위치, 차폐물의 기하 | 직접광의 가시성 |

이 구분은 세 기능이 반드시 서로 다른 프로그램이나 Render Pass에 있어야 한다는 뜻이 아니다. 작은 실시간 Shader에서는 세 결과를 한 함수 안에서 곱할 수도 있고, Path Tracer에서는 광선 경로 전체를 추적하면서 함께 평가할 수도 있다.

구분의 목적은 **어떤 원인이 어떤 결과를 만들었는지 설명하는 것**이다. 화면이 어둡다는 결과만 보고는 광원이 약한지, 표면이 빛을 등지고 있는지, 다른 물체가 빛을 막았는지 알 수 없다.

## Lighting은 장면에 빛을 놓는 것보다 넓다

일상에서 Lighting은 조명을 배치하고 분위기를 만드는 일을 뜻한다. 그래픽스에서도 광원의 위치, 방향, 색과 세기를 정하는 작업을 Lighting이라고 부른다. 그러나 렌더링 계산의 관점에서는 한 단계 더 구체적인 질문이 필요하다.

> 지금 계산하려는 표면 지점에 어느 방향에서 얼마만큼의 빛이 들어오는가?

[PBRT 4판의 Light Sources 장](https://pbr-book.org/4ed/Light_Sources)은 스스로 빛을 내지 않는 물체가 보이려면 광원에서 나온 빛이 표면에서 반사되어 카메라 센서에 도달해야 한다는 관계에서 출발한다. 점광원, 면광원과 환경광은 빛을 내보내는 공간적·방향적 분포가 서로 다르다. 거리와 광원의 크기까지 고려하면 같은 세기의 광원이라도 표면을 향하는 빛은 달라진다.

이 글에서는 차폐를 적용하기 전에 **표면을 향하는 빛의 조건과 분포**를 Lighting이라고 부르겠다. 그 빛이 실제로 표면까지 도달하는지는 뒤에서 Shadow 가시성으로 구분한다.

Lighting이 결정하는 대표적인 값은 다음과 같다.

- 빛이 오는 방향
- 표면에 도달하기 전의 빛의 세기와 색
- 광원까지의 거리와 거리 감쇠
- 점, 선, 면 또는 환경처럼 광원이 차지하는 범위
- 직접광인지 다른 표면을 거쳐 온 간접광인지

하지만 광원 정보만으로 픽셀 색을 바로 정할 수는 없다. 같은 빛이 도달해도 표면의 방향과 재질에 따라 카메라로 돌아오는 양이 달라지기 때문이다.

## Shading은 빛을 표면의 모습으로 바꾼다

Shading은 보이는 표면의 한 지점에서 최종 밝기와 색을 정하는 과정이다. 들어오는 빛뿐 아니라 표면의 법선, 재질의 반사 성질과 카메라 방향을 함께 사용한다.

무광 종이는 여러 방향으로 빛을 넓게 흩뜨리고, 매끄러운 플라스틱은 특정 방향에 밝은 하이라이트를 만든다. 같은 재질의 구에서도 광원을 정면으로 향한 부분과 비스듬히 향한 부분의 밝기가 다르다. Shading은 이런 차이를 계산해 평면의 삼각형 집합을 굽은 형태와 재질을 가진 물체처럼 보이게 한다.

[PBRT의 Surface Reflection 절](https://pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Surface_Reflection)은 표면에 들어온 빛이 표면의 산란 성질에 따라 관찰 방향으로 얼마나 나가는지를 반사 방정식으로 설명한다. 이후 살펴볼 Lambert, Phong, Blinn–Phong과 물리 기반 BRDF는 모두 이 **표면 반응을 어떤 규칙으로 계산할 것인가**에 대한 서로 다른 답이다.

여기서 자주 생기는 오해가 있다.

- **Shading은 그림자를 그리는 일과 같지 않다.** 빛이 도달한다고 가정한 뒤에도 표면 방향과 재질 때문에 명암이 생긴다.
- **Shader가 모두 Shading만 하는 것은 아니다.** Shader 프로그램은 정점 변환, 후처리, 입자 계산처럼 빛과 무관한 일도 수행할 수 있다.
- **Shading Model과 Shading 방식도 구분할 필요가 있다.** Phong 반사 모델은 빛에 대한 표면 반응을 근사하고, Phong Shading은 보간된 법선을 이용해 표면 지점마다 그 반응을 계산하는 방식이다.

이 차이는 뒤의 Lambert, Gouraud와 Phong을 다룰 때 다시 자세히 연결한다.

## Shadow는 어두운 색이 아니라 빛 경로의 가시성이다

표면이 광원을 향하고 있고 밝은 재질을 가졌더라도, 광원과 표면 사이에 다른 물체가 있으면 직접광은 도달하지 못한다. Shadow가 답하는 질문은 다음처럼 단순하다.

> 표면 지점에서 광원을 볼 수 있는가?

[PBRT의 Visibility 절](https://pbr-book.org/4ed/Introduction/Photorealistic_Rendering_and_the_Ray-Tracing_Algorithm#Visibility)은 표면에서 광원으로 Shadow Ray를 보내고, 그 사이에서 다른 물체와 교차하는지 검사하는 방식으로 이 문제를 설명한다. 불투명한 물체와 하나의 점광원만 생각하면 가시성은 두 값으로 표현할 수 있다.

- `1`: 광원이 보인다. 직접광이 표면에 도달한다.
- `0`: 광원이 가려졌다. 해당 광원의 직접광은 도달하지 않는다.

Shadow는 단순히 어두운 색을 덧칠한 영역이 아니다. 광원의 위치가 바뀌거나 차폐물이 움직이면 가시성 관계도 바뀌어야 한다. 바닥에 검은 얼룩을 그려 두는 것만으로는 이 관계를 설명할 수 없다.

표면 자체가 빛을 등져 `N · L`이 0 이하가 된 경우와 다른 물체가 빛을 막은 경우도 구분해야 한다. 둘 다 직접광이 없는 어두운 결과를 만들 수 있지만 원인은 다르다.

- 표면이 빛을 등짐: **표면 방향과 Shading의 문제**
- 다른 물체가 빛을 막음: **광원 가시성과 Shadow의 문제**

미술에서는 전자를 물체에 붙어 있는 `attached shadow`, 후자를 다른 표면에 드리워진 `cast shadow`로 함께 설명하기도 한다. 이 연재에서 렌더링 알고리즘을 구분할 때는 `Shadow`를 주로 **차폐에 의한 광원 가시성**이라는 좁은 의미로 사용한다.

## 세 계산은 마지막에 하나의 빛으로 만난다

하나의 점광원이 불투명한 표면을 직접 비추는 단순한 상황을 생각해 보자. 카메라 방향으로 나가는 빛은 다음 관계로 정리할 수 있다.

```text
나가는 빛
= 표면이 스스로 내는 빛
+ 광원 가시성 × 들어오는 빛 × 표면 반사 × 빛과 표면의 방향 관계
```

기호로 압축하면 다음과 같은 형태다.

`L_o = L_e + V × L_i × f_r × max(0, N · L)`

| 항 | 이 글에서 연결할 역할 |
| --- | --- |
| `L_i` | Lighting이 제공하는 차폐 적용 전의 빛 기여 후보 |
| `f_r`, `N · L` | Shading이 평가하는 재질과 표면 방향의 반응 |
| `V` | Shadow 계산이 제공하는 광원 가시성 |
| `L_o` | 카메라 방향으로 나가 최종 픽셀에 기여할 빛 |

이 식은 한 점광원의 직접광만 보여 주기 위한 개념적 축약이다. 실제 [Kajiya의 1986년 Rendering Equation](https://doi.org/10.1145/15886.15902)은 표면을 향해 모든 방향에서 들어오는 빛을 적분하고, 다른 표면에서 반사되어 온 간접광까지 같은 관계 안에 포함한다.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g002-lighting-shading-shadow/direct-light-terms-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g002-lighting-shading-shadow/direct-light-terms.svg" alt="들어오는 빛, 표면 반응과 가시성이 곱해져 직접광 기여를 만드는 관계">
</picture>

*그림 2. Lighting, Shading과 Shadow는 별개의 질문이지만 한 표면 지점의 직접광을 만들 때 함께 결합된다. 직접 제작.*

이 관계를 이용하면 서로 비슷해 보이는 어두운 결과를 원인별로 나눌 수 있다.

- `L_i`가 작다: 광원이 약하거나 멀어서 어둡다.
- `N · L`이 0에 가깝다: 표면이 빛을 비스듬히 받거나 등져서 어둡다.
- `f_r`이 작다: 재질이 해당 빛을 거의 반사하지 않아 어둡다.
- `V = 0`이다: 다른 물체가 광원을 가려 직접광이 없다.

결과 색만 보면 모두 어둡지만, 고쳐야 할 데이터와 알고리즘은 전혀 다르다.

## 왜 오래된 논문에서도 용어가 섞여 보일까

오늘날에도 Lighting, Illumination, Shading은 문서와 도구마다 범위가 조금씩 다르다. 초기 그래픽스 논문의 제목과 설명을 따라가면 그 이유를 볼 수 있다.

[Arthur Appel의 1968년 논문 *Some Techniques for Shading Machine Renderings of Solids*](https://doi.org/10.1145/1468075.1468082)은 선으로만 그린 입체보다 형태와 깊이를 강하게 전달하기 위해 기계적으로 명암을 만드는 문제를 다뤘다. 이 시기의 `shading`은 표면 밝기뿐 아니라 그림자를 포함한 사실적인 명암 생성이라는 넓은 목표에 가까웠다.

[Henri Gouraud의 1971년 논문 *Continuous Shading of Curved Surfaces*](https://doi.org/10.1109/T-C.1971.223313)은 다각형으로 근사한 곡면에서 면마다 밝기가 끊겨 보이는 문제를 줄이는 데 초점을 맞췄다. 정점에서 계산한 명암을 표면 안쪽으로 보간함으로써 더 적은 다각형으로도 부드러운 곡면을 표현하려 했다. 여기서 Shading은 **표면의 밝기를 어디에서 계산하고 어떻게 이어 붙일 것인가**라는 의미로 좁아진다.

[Bui Tuong Phong의 1975년 논문 *Illumination for Computer Generated Pictures*](https://doi.org/10.1145/360825.360839)은 제목에는 Illumination을 사용하지만, 본문에서는 물체 모델링, Hidden Surface와 Shading 기법이 서로 연결된 문제라고 설명한다. 오늘날 `Phong Lighting Model`, `Phong Reflection Model`, `Phong Shading`이라는 표현이 종종 뒤섞이는 것도 반사 규칙과 보간 방법이 같은 연구 흐름에서 소개된 역사와 무관하지 않다.

[Franklin Crow의 1977년 논문 *Shadow Algorithms for Computer Graphics*](https://people.csail.mit.edu/ericchan/bib/pdf/p242-crow.pdf)은 그림자가 장면 이해와 사실감을 높인다고 설명하면서, 당시의 Shadow 계산을 세 부류로 분류했다. 그림자를 Scanout 중 계산하는 방법, 표면을 그림자 안과 밖으로 미리 나누는 방법, 가려진 공간을 Shadow Volume으로 표현하는 방법이다. 이 분류는 Shadow가 단순한 표면색 규칙이 아니라 **장면 기하 전체를 대상으로 하는 별도의 가시성 문제**였음을 보여 준다.

용어가 처음부터 엄격한 소프트웨어 모듈 이름으로 태어난 것은 아니다. 연구자들은 `더 입체적으로 보이게 만들기`, `다각형 경계를 숨기기`, `광원 가림을 계산하기`처럼 서로 다른 문제에서 출발했다. 그래서 문맥을 보지 않고 단어만 외우면 같은 말이 넓게도, 좁게도 쓰이는 것처럼 보인다.

이 연재에서는 이후의 기술을 일관되게 연결하기 위해 다음 기준을 사용한다.

> Lighting은 표면을 향하는 빛, Shading은 그 빛에 대한 표면의 반응, Shadow는 그 빛이 실제 도달하는지를 정하는 광원 가시성이다.

## 같은 장면에서 하나씩 빼 보면 차이가 선명해진다

같은 구와 바닥, 같은 카메라를 유지하고 한 요소씩 바꿔 보자.

<picture>
  <source media="(max-width: 640px)" srcset="/assets/images/posts/graphics-series/g002-lighting-shading-shadow/controlled-comparison-mobile.svg">
  <img src="/assets/images/posts/graphics-series/g002-lighting-shading-shadow/controlled-comparison.svg" alt="같은 장면에서 Lighting, Shading과 Shadow를 순서대로 적용했을 때 달라지는 시각 단서">
</picture>

*그림 3. 광원 정보만으로는 표면의 모습이 정해지지 않으며, Shading은 형태를, Shadow는 물체와 바닥의 공간 관계를 보강한다. 직접 제작.*

### Lighting 정보만 있는 경우

광원의 위치와 세기를 알고 있어도 표면 반응을 계산하지 않으면 구 전체를 한 색으로 칠할 수밖에 없다. 렌더러는 빛이 어디에 있는지는 알지만, 구의 어느 부분이 더 밝아야 하는지는 아직 평가하지 않았다.

### Shading까지 계산한 경우

표면 법선과 재질을 이용하면 구에 밝고 어두운 변화가 생긴다. 둥근 형태는 읽히지만, 광원 가시성을 검사하지 않았다면 구가 바닥으로 빛을 막아도 바닥은 계속 밝다. 구가 바닥과 분리되어 떠 있는 것처럼 느껴질 수 있다.

### Shadow까지 계산한 경우

광원에서 바닥으로 향하는 경로를 구가 막는 영역의 직접광을 제거하면 바닥에 그림자가 생긴다. 이제 구의 형태뿐 아니라 광원의 방향, 구와 바닥의 접촉 관계도 읽기 쉬워진다.

이 비교에서 중요한 점은 Shadow가 Shading을 대신하지 않는다는 것이다. 그림자를 계산해도 구 표면의 재질과 명암은 별도로 계산해야 한다. 반대로 구를 매끄럽게 Shading해도 바닥 그림자는 자동으로 생기지 않는다.

## 화면 문제를 세 질문으로 진단할 수 있다

세 용어의 경계를 알면 렌더링 문제를 볼 때 먼저 조사할 지점이 달라진다.

| 화면에서 보이는 현상 | 먼저 확인할 질문 |
| --- | --- |
| 장면 전체가 지나치게 어둡거나 광원 색이 이상하다 | Lighting 입력과 빛의 세기·거리·색이 맞는가 |
| 물체가 각져 보이거나 하이라이트 위치가 이상하다 | Shading에 사용하는 법선, 재질과 관찰 방향이 맞는가 |
| 물체가 바닥에서 떠 보이거나 빛이 벽을 뚫는다 | Shadow 가시성에서 차폐물을 놓치지 않았는가 |
| 그림자 안이 완전히 검어서 부자연스럽다 | 직접광 외에 간접광이나 다른 광원이 있는가 |
| 표면의 빛 반대쪽이 어둡다 | 차폐 때문인지 `N · L` 때문인지 구분했는가 |

물론 실제 렌더러의 버그는 여러 원인이 겹칠 수 있다. 잘못된 법선은 Shading뿐 아니라 Shadow Bias에도 영향을 줄 수 있고, 면광원의 크기는 표면 하이라이트와 부드러운 그림자를 동시에 바꾼다. 경계가 있다는 말은 서로 무관하다는 뜻이 아니라, **상호작용을 이해하기 위한 출발 질문이 다르다**는 뜻이다.

## 현실의 빛에서는 경계가 다시 흐려진다

지금까지는 하나의 직접광을 기준으로 세 역할을 나눴다. 현실의 빛을 더 정확하게 계산하면 단순한 구분만으로 끝나지 않는다.

- 그림자 영역도 다른 벽과 바닥에서 반사된 간접광을 받을 수 있다.
- 면광원은 표면의 위치마다 보이는 비율이 달라 부드러운 그림자를 만든다.
- 반투명한 차폐물은 가시성을 `0`이나 `1`이 아니라 파장별 투과량으로 바꾼다.
- 거울과 유리에서는 카메라로 오는 빛이 다른 표면과 경로를 거쳐 도달한다.

따라서 고급 렌더러에서 Lighting은 장면 전체의 Light Transport를 뜻하기도 하고, Shading은 재질 평가뿐 아니라 텍스처와 가시성 결과를 조합하는 넓은 실행 단계를 뜻하기도 한다. 그래도 세 질문은 사라지지 않는다. 들어오는 빛, 표면의 반응, 경로의 가시성을 어떤 순서와 방식으로 계산할지 선택할 뿐이다.

## 정리

- Lighting은 광원의 배치만이 아니라 차폐 적용 전 표면을 향하는 빛의 방향, 세기와 분포를 설명한다.
- Shading은 들어오는 빛과 표면 방향, 재질, 관찰 방향을 이용해 카메라 쪽으로 나가는 빛을 계산한다.
- Shadow는 표면과 광원 사이가 다른 물체에 가려졌는지 판단하는 광원 가시성 문제다.
- 표면이 빛을 등져 어두운 것과 다른 물체가 빛을 막아 어두운 것은 결과가 비슷해도 원인이 다르다.
- 세 역할은 실제 코드에서 함께 계산될 수 있지만, 기술을 이해하고 화면 문제를 진단하려면 구분해야 한다.

이제 빛과 표면, 가시성이 서로 다른 질문이라는 것을 알게 되었다. 그렇다면 그 출발점인 빛은 무엇이며, 공간과 물질 속에서 어떻게 이동할까? 다음 글에서는 현실의 빛이 전자기파와 광자로 설명되는 방식과, 그래픽스가 복잡한 빛의 이동을 광선으로 추상화하는 이유를 살펴본다.

## 참고

- [Physically Based Rendering, 4th Edition — Photorealistic Rendering and the Ray-Tracing Algorithm](https://pbr-book.org/4ed/Introduction/Photorealistic_Rendering_and_the_Ray-Tracing_Algorithm)
- [Physically Based Rendering, 4th Edition — Light Sources](https://pbr-book.org/4ed/Light_Sources)
- [Physically Based Rendering, 4th Edition — Surface Reflection](https://pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Surface_Reflection)
- [Arthur Appel, Some Techniques for Shading Machine Renderings of Solids, 1968](https://doi.org/10.1145/1468075.1468082)
- [Henri Gouraud, Continuous Shading of Curved Surfaces, 1971](https://doi.org/10.1109/T-C.1971.223313)
- [Bui Tuong Phong, Illumination for Computer Generated Pictures, 1975](https://doi.org/10.1145/360825.360839)
- [Franklin C. Crow, Shadow Algorithms for Computer Graphics, 1977](https://doi.org/10.1145/563858.563901)
- [James T. Kajiya, The Rendering Equation, 1986](https://doi.org/10.1145/15886.15902)
