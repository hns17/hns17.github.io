# Graphics Series Plan

이 문서는 엔진 독립적 그래픽스 연재의 작성 순서와 진행 상태를 관리한다.
글의 범위, 문체, 이미지와 검증 기준은 `GRAPHICS_POST_GUIDE.md`를 따른다.

## 연재 정보

- 내부 ID: `graphics-foundations`
- 연재 제목: `빛에서 픽셀까지`
- 카테고리: `Graphics/Series/Light-To-Pixel`
- 연재 페이지: `/category/graphics/series/light-to-pixel/`
- 글 제목 형식: `[빛에서 픽셀까지 NNN] 주제`
- 설명: 사물 인식에서 출발해 빛, 셰이딩, 그림자와 렌더링 기술의 계보를 원인과 결과로 연결한다.

이 계획표는 `빛에서 픽셀까지` 연재만 관리한다. 다른 그래픽스 연재는 고유한 내부 ID, 제목,
`Graphics/Series/<Series-Key>` 카테고리, 연재 페이지와 계획표를 별도로 가진다.

## 상태 규칙

- `[ ]`: 미완료. 미작성, 작성 중, 검토 중, 수정 중인 상태를 모두 포함한다.
- `[x]`: 사용자가 최종 승인했고, 완료 표시를 포함한 커밋이 원격 저장소에 푸시된 상태다.
- 글, 이미지와 Jekyll 빌드 검증이 끝나도 사용자 승인 전에는 `[ ]`로 남긴다.
- 예약 작업은 모든 앞 항목이 `[x]`일 때만 다음 미작성 항목의 초안을 한 편 작성할 수 있다.
- 가장 앞의 `[ ]` 항목에 같은 `series_id`의 초안이 이미 있으면 예약 작업은 아무것도 수정하지 않고
  사용자 검토·수정 또는 완료 승인을 기다린다.
- 사용자가 명시적으로 완료를 승인하면 계획표 표시, 커밋과 푸시를 수행하고 원격 반영을 확인한다.
- 검증, 커밋 또는 푸시에 실패한 항목은 완료로 간주하지 않으며 다음 글로 진행하지 않는다.
- 완료된 항목의 제목이나 순서를 임의로 바꾸지 않는다.

## 0부. 왜 그래픽스는 빛에서 시작하는가

연재 전체가 답할 질문과 그래픽스의 범위를 세운다.

- [x] G001 — 왜 3D 그래픽스는 빛에서 시작하는가
- [x] G002 — Lighting, Shading, Shadow는 무엇이 다른가

## 1부. 사람은 빛을 어떻게 이해하고 측정했는가

셰이딩과 그림자를 계산하기 전에 빛을 설명하고 측정하는 언어를 만든다.

- [ ] G003 — 빛은 무엇이며 어떻게 이동하고 그래픽스에서는 왜 광선으로 다루는가
- [ ] G004 — Newton의 프리즘 실험과 빛의 스펙트럼
- [ ] G005 — 반사, 굴절, 흡수와 산란
- [ ] G006 — Radiometry와 Photometry는 무엇이 다른가
- [ ] G007 — 입체각과 Steradian은 왜 필요한가
- [ ] G008 — Candela는 특정 방향의 빛을 어떻게 나타내는가
- [ ] G009 — Lumen은 광원의 전체 빛을 어떻게 나타내는가
- [ ] G010 — Lux와 거리 역제곱 법칙
- [ ] G011 — Luminance와 Nit는 보이는 밝기를 어떻게 나타내는가
- [ ] G012 — 광원의 크기, 색온도와 빛의 인상

## 2부. 빛은 어떻게 색과 픽셀이 되는가

물리적인 빛이 사람의 시각과 디스플레이를 거쳐 RGB 이미지가 되고, 렌더러의 한 픽셀로
기록되는 과정을 다룬다.

- [ ] G013 — 사람의 눈은 빛을 어떻게 색으로 인식하는가
- [ ] G014 — 파장, 색 지각과 Metamerism
- [ ] G015 — 빛의 삼원색은 왜 RGB인가
- [ ] G016 — 감산 혼합은 가산 혼합과 무엇이 다른가
- [ ] G017 — CIE 색 일치 실험과 XYZ 색 공간
- [ ] G018 — 색역, White Point와 색도도
- [ ] G019 — sRGB와 Gamma Encoding의 역사
- [ ] G020 — Linear 공간에서 조명을 계산해야 하는 이유
- [ ] G021 — HDR, 카메라 노출과 EV
- [ ] G022 — Tone Mapping은 장면의 빛을 화면에 어떻게 담는가
- [ ] G023 — 3D 장면에서 한 픽셀이 만들어지는 과정
- [ ] G024 — 현실의 빛과 실시간 렌더링의 타협

## 3부. 3D 공간은 어떻게 2D 화면이 되는가

빛을 계산할 표면이 어느 픽셀에 놓이는지 설명한다.

- [ ] G025 — 원근법은 왜 필요했고 어떻게 발전했는가
- [ ] G026 — 벡터는 왜 그래픽스의 언어가 되었는가
- [ ] G027 — 내적과 외적은 방향 관계를 어떻게 나타내는가
- [ ] G028 — Object, World, View와 Screen 좌표 공간
- [ ] G029 — 행렬로 이동, 회전과 크기를 결합하는 이유
- [ ] G030 — View Matrix는 세계를 카메라 기준으로 어떻게 바꾸는가
- [ ] G031 — Perspective와 Orthographic Projection
- [ ] G032 — Homogeneous Coordinate와 Perspective Division
- [ ] G033 — View Frustum과 Clipping
- [ ] G034 — Depth 값이 비선형인 이유
- [ ] G035 — Z-fighting과 Reversed-Z

## 4부. 메시에서 픽셀까지

연속적인 표면을 삼각형으로 근사하고 화면의 Fragment로 바꾸는 과정을 다룬다.

- [ ] G036 — 곡면을 왜 삼각형 Mesh로 표현하는가
- [ ] G037 — Vertex, Index와 Mesh Topology
- [ ] G038 — Face Normal, Vertex Normal과 Smooth Edge
- [ ] G039 — Hidden Surface Problem과 Painter's Algorithm
- [ ] G040 — Back-face, Frustum과 Occlusion Culling
- [ ] G041 — Z-buffer는 가려진 표면을 어떻게 찾는가
- [ ] G042 — Rasterization은 삼각형을 어떻게 Fragment로 바꾸는가
- [ ] G043 — Barycentric Coordinate와 정점 데이터 보간
- [ ] G044 — Perspective Correct Interpolation이 필요한 이유
- [ ] G045 — Depth, Stencil과 Blending
- [ ] G046 — 한 프레임이 Framebuffer에 완성되는 과정

## 5부. Sampling과 Aliasing

연속적인 신호를 제한된 픽셀과 프레임으로 기록할 때 생기는 손실을 다룬다.

- [ ] G047 — 연속적인 세계를 이산적인 Sample로 표현한다는 것
- [ ] G048 — Nyquist–Shannon Sampling Theorem
- [ ] G049 — Spatial Aliasing과 Moiré Pattern
- [ ] G050 — Temporal Aliasing과 움직임의 떨림
- [ ] G051 — Supersampling과 Multisampling
- [ ] G052 — FXAA와 SMAA 같은 후처리 Anti-Aliasing
- [ ] G053 — Temporal Anti-Aliasing과 누적의 장단점
- [ ] G054 — 렌더링 해상도, Dynamic Resolution과 Upscaling

## 6부. GPU와 Shader는 왜 등장했는가

그래픽스 전용 하드웨어와 프로그래머블 파이프라인이 필요해진 배경을 다룬다.

- [ ] G055 — Vector Display, Raster Display와 Framebuffer
- [ ] G056 — CPU만으로 그래픽스를 계산하기 어려웠던 이유
- [ ] G057 — GPU의 병렬 구조와 그래픽스 계산
- [ ] G058 — 고정 기능 파이프라인은 무엇이었는가
- [ ] G059 — Programmable Shader가 등장한 이유
- [ ] G060 — 현대 Graphics Pipeline의 전체 구조
- [ ] G061 — Vertex Shader가 정점을 처리하는 과정
- [ ] G062 — Rasterizer와 Fragment Shader
- [ ] G063 — Geometry, Tessellation과 Compute Shader의 역할
- [ ] G064 — Shader, Material, Render State와 Pass의 차이

## 7부. 표면은 어떻게 빛을 받아 밝아졌는가

초기 셰이딩 모델이 앞선 방식의 시각적 한계를 어떻게 해결했는지 역사 순서로 다룬다.

- [ ] G065 — 단색 삼각형은 왜 입체적으로 보이지 않는가
- [ ] G066 — Lambert의 측광 연구와 코사인 법칙
- [ ] G067 — Lambert Diffuse와 N dot L
- [ ] G068 — Diffuse와 Albedo는 무엇이 다른가
- [ ] G069 — Flat Shading은 왜 면이 갈라져 보이는가
- [ ] G070 — Gouraud Shading과 정점 명암 보간
- [ ] G071 — Gouraud Shading이 작은 하이라이트를 놓치는 이유
- [ ] G072 — Phong Shading과 법선 보간
- [ ] G073 — Phong Shading과 Phong Lighting의 차이
- [ ] G074 — Specular Highlight와 Reflection Vector
- [ ] G075 — Phong Specular는 반짝임을 어떻게 근사하는가
- [ ] G076 — Blinn–Phong과 Half Vector
- [ ] G077 — Phong과 Blinn–Phong의 차이
- [ ] G078 — 점광원의 거리 감쇠
- [ ] G079 — Half-Lambert와 Wrap Lighting
- [ ] G080 — Rim Lighting과 보기 좋은 셰이딩

## 8부. Texture와 표면 정보

기하를 늘리지 않고 표면의 색과 세부 정보를 표현하려는 흐름을 다룬다.

- [ ] G081 — 모든 표면의 세부 형태를 Mesh로 만들 수 있을까
- [ ] G082 — Catmull과 Texture Mapping의 등장
- [ ] G083 — UV Coordinate는 2D 이미지와 3D 표면을 어떻게 연결하는가
- [ ] G084 — Texel, Pixel과 Texture Sampling
- [ ] G085 — Sampler State와 Wrap Mode
- [ ] G086 — Point와 Bilinear Filtering
- [ ] G087 — Minification과 Magnification
- [ ] G088 — Mipmap은 왜 피라미드 형태로 등장했는가
- [ ] G089 — Mip Level, LOD Bias와 Trilinear Filtering
- [ ] G090 — Anisotropic Filtering이 비스듬한 표면을 개선하는 이유
- [ ] G091 — Texture Atlas와 경계 이음새
- [ ] G092 — Texture Array가 Atlas의 문제를 피하는 방법
- [ ] G093 — Texture Compression과 Color·Data Texture의 차이

## 9부. 메시를 늘리지 않고 표면을 바꾸는 방법

표면 세부를 색이 아니라 방향과 높이 정보로 표현하는 기술을 다룬다.

- [ ] G094 — Bump Mapping은 왜 등장했는가
- [ ] G095 — Height Map은 표면 높이를 어떻게 표현하는가
- [ ] G096 — Normal Map과 Tangent Space
- [ ] G097 — TBN Matrix는 좌표 공간을 어떻게 연결하는가
- [ ] G098 — Object Space와 Tangent Space Normal Map
- [ ] G099 — Parallax Mapping
- [ ] G100 — Parallax Occlusion Mapping
- [ ] G101 — Displacement Mapping과 Tessellation

## 10부. 물리 기반 렌더링

임의적인 재질 값에서 일관된 빛 반사 모델로 이동한 이유를 다룬다.

- [ ] G102 — Phong 재질은 왜 조명이 바뀌면 일관성을 잃는가
- [ ] G103 — BRDF는 무엇을 설명하는 함수인가
- [ ] G104 — 에너지 보존과 Reciprocity
- [ ] G105 — Fresnel은 비스듬한 표면을 왜 더 반사되게 만드는가
- [ ] G106 — 금속과 비금속은 빛을 어떻게 다르게 반사하는가
- [ ] G107 — Microfacet 모델은 거친 표면을 어떻게 바라보는가
- [ ] G108 — Normal Distribution Function
- [ ] G109 — Geometry Function의 Shadowing과 Masking
- [ ] G110 — Cook–Torrance 반사 모델
- [ ] G111 — Roughness가 하이라이트를 바꾸는 방법
- [ ] G112 — Metallic–Roughness와 Specular Workflow
- [ ] G113 — Image Based Lighting이 필요한 이유
- [ ] G114 — Diffuse Irradiance와 Specular Prefilter
- [ ] G115 — BRDF LUT와 실시간 PBR의 한계

## 11부. 셰이딩만으로는 왜 그림자가 생기지 않는가

표면의 반응과 광원 가시성이 별개의 문제임을 설명한다.

- [ ] G116 — 표면 밝기와 빛의 가려짐은 왜 다른가
- [ ] G117 — Hard Shadow, Soft Shadow, Umbra와 Penumbra
- [ ] G118 — 점광원과 면광원의 그림자
- [ ] G119 — Shadow Volume은 그림자를 어떻게 기하로 만드는가
- [ ] G120 — Shadow Map은 왜 광원 시점의 Depth Buffer인가
- [ ] G121 — Shadow Acne와 Self-shadowing
- [ ] G122 — Depth Bias, Normal Bias와 Peter Panning
- [ ] G123 — Shadow Map Resolution과 Perspective Aliasing
- [ ] G124 — Percentage-Closer Filtering
- [ ] G125 — Variance와 Exponential Shadow Map
- [ ] G126 — Cascaded Shadow Map
- [ ] G127 — Contact Shadow와 Screen Space Shadow
- [ ] G128 — Baked Shadow와 Mixed Shadow의 일반 원리
- [ ] G129 — 그림자 품질과 계산 비용의 균형

## 12부. 한 번 반사된 빛은 어디로 가는가

직접광을 넘어 장면 전체의 빛 전달을 계산하는 기술로 확장한다.

- [ ] G130 — Ambient 상수는 왜 사용되었는가
- [ ] G131 — 직접광만으로 실내가 검게 보이는 이유
- [ ] G132 — Rendering Equation은 무엇을 하나로 묶었는가
- [ ] G133 — Ray Casting과 Ray Tracing
- [ ] G134 — Whitted-style Ray Tracing
- [ ] G135 — Monte Carlo Integration을 렌더링에 사용하는 이유
- [ ] G136 — Path Tracing은 빛의 경로를 어떻게 선택하는가
- [ ] G137 — Sample, Noise와 Variance
- [ ] G138 — Importance Sampling
- [ ] G139 — Russian Roulette가 긴 경로를 끝내는 방법
- [ ] G140 — Radiosity와 확산 간접광
- [ ] G141 — Lightmap, Irradiance Cache와 Probe
- [ ] G142 — Ambient Occlusion과 Screen Space AO
- [ ] G143 — 실시간 Ray Tracing, Hybrid Rendering과 Denoising

## 13부. 렌더링 경로는 왜 여러 종류가 되었는가

정확한 조명을 제한된 프레임 시간 안에 계산하기 위한 구조적 선택을 다룬다.

- [ ] G144 — 실시간 프레임 예산과 Render Pass
- [ ] G145 — Forward Rendering의 기본 구조
- [ ] G146 — Forward에서 라이트가 늘어나면 생기는 문제
- [ ] G147 — Deferred Rendering은 무엇을 나중으로 미루는가
- [ ] G148 — Geometry Pass와 G-Buffer
- [ ] G149 — Deferred Lighting Pass
- [ ] G150 — Deferred의 메모리 대역폭과 투명도 문제
- [ ] G151 — Tiled Deferred Rendering
- [ ] G152 — 화면과 공간에서 Light Culling하기
- [ ] G153 — Forward+ Rendering
- [ ] G154 — Clustered Rendering
- [ ] G155 — Tile-based GPU와 Immediate Mode GPU
- [ ] G156 — Forward, Deferred와 Forward+를 선택하는 기준

## 14부. 투명 렌더링

Depth Buffer와 그리기 순서만으로 풀기 어려운 투명 표면의 문제를 다룬다.

- [ ] G157 — Alpha는 투명도를 어떻게 표현하는가
- [ ] G158 — Straight Alpha와 Premultiplied Alpha
- [ ] G159 — Blend Equation
- [ ] G160 — 투명 오브젝트의 정렬과 Depth Write
- [ ] G161 — Alpha Test와 Cutout
- [ ] G162 — Overdraw와 투명 렌더링 비용
- [ ] G163 — Order Independent Transparency와 굴절

## 15부. 비사실적 렌더링과 스타일

물리적인 기준을 이해한 뒤 의도적으로 단순화하거나 변형하는 방법을 다룬다.

- [ ] G164 — 물리적으로 정확한 이미지가 항상 좋은가
- [ ] G165 — Non-Photorealistic Rendering의 목표
- [ ] G166 — Cel Shading과 명암 단계화
- [ ] G167 — Ramp Texture, Toon Specular와 Rim
- [ ] G168 — Geometry와 Screen Space Outline
- [ ] G169 — Hatching과 Painterly Rendering
- [ ] G170 — 물리 기반 조명과 스타일 셰이딩의 결합

## 16부. 공기와 볼륨은 어떻게 렌더링하는가

표면이 아닌 공기, 안개와 구름 안에서 일어나는 빛의 변화를 다룬다.

- [ ] G171 — 공기는 정말 비어 있는가
- [ ] G172 — Participating Media와 흡수
- [ ] G173 — Beer–Lambert 법칙과 Optical Depth
- [ ] G174 — In-scattering과 Out-scattering
- [ ] G175 — Phase Function과 산란 방향
- [ ] G176 — Ray Marching과 Step Size
- [ ] G177 — Fog와 Height Fog
- [ ] G178 — Volumetric Light와 God Ray
- [ ] G179 — Noise와 구름의 밀도 표현
- [ ] G180 — Volumetric Cloud와 볼륨 렌더링 비용

## 17부. 최종 이미지를 만드는 후처리

렌더링된 장면을 사람이 보게 될 최종 이미지로 바꾸는 과정을 다룬다.

- [ ] G181 — 렌더링이 끝난 뒤에도 계산이 필요한 이유
- [ ] G182 — HDR Buffer와 Tone Mapping 다시 연결하기
- [ ] G183 — Bloom
- [ ] G184 — Color Grading과 LUT
- [ ] G185 — Depth of Field
- [ ] G186 — Motion Blur
- [ ] G187 — Lens Flare, Vignette와 Chromatic Aberration
- [ ] G188 — Screen Space Reflection과 Global Illumination
- [ ] G189 — MSAA, FXAA, SMAA와 TAA 비교
- [ ] G190 — Dynamic Resolution, Upscaling과 디스플레이 출력

## 18부. 렌더링 성능은 무엇으로 결정되는가

특정 엔진의 도구가 아니라 일반적인 프레임 비용과 병목을 다룬다.

- [ ] G191 — 프레임 시간과 FPS를 함께 봐야 하는 이유
- [ ] G192 — CPU Bound와 GPU Bound
- [ ] G193 — Draw Call과 Render State 변경 비용
- [ ] G194 — Batching과 Instancing
- [ ] G195 — Vertex 처리와 Fragment 처리 비용
- [ ] G196 — Fill Rate와 Overdraw
- [ ] G197 — Texture Sampling, Bandwidth와 Cache
- [ ] G198 — Render Target과 G-Buffer 비용
- [ ] G199 — Shader Branch와 Variant
- [ ] G200 — LOD, Culling, Dynamic Resolution과 측정 기반 최적화
