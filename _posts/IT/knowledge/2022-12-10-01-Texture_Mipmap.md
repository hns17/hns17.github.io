---
title: Texture와 Mipmap
categories: IT/Knowledge
tags: ["Mipmap", "Texture", "Sampling", "Texel"]
---

# Texture와 Mipmap

## 1. Texture Sampling

![image-20221210015659830](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210015659830.png)

[https://wildfiregames.com](https://wildfiregames.com/forum/topic/39808-tutorial-texels-and-making-textures-for-3d-2d-advanced-3d-basic/)

- 모니터 화면의 Object는 Mesh로 이루어져있으며 이런 Mesh에 입히는 이미지를 Texture라고 한다
  - 이 외에도 이미지 데이터는 용도에 따라 NormalMap, Lookup용 Table, Depth, RTT 등 여러 종류로 사용
- FragmentShader에서 Pixel단위로 Mesh에 대응되는 Texture의 Texel 정보를 가져오는 작업을 Texture Sampling이라고 한다

### (1). UV Coordinate

- 각 Mesh의 위치에 맞는 Texture의 위치정보(Texel)를 uv라고 한다
- uv는 Texture에 대한 texel의 좌표이며 0~1로 표현
- 보통 가로 방향 u의 값은 왼쪽에서 오른쪽으로 증가하지만 세로 방향 v의 값은 그래픽 라이브러리나 엔진, 툴마다 다르다

[D3D]

![image-20221210014756552](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210014756552.png)



[Unreal]

![image-20221210015152278](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210015152278.png)

```
왼쪽 상단이 시작점인 대표적인 경우 : D3D, Unreal
```

[OpenGL]

![image-20221210014825871](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210014825871.png)



[3DsMax & Unity]

![image-20221210014853906](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210014853906.png)

[http://www.aclockworkberry.com](http://www.aclockworkberry.com/uv-coordinate-systems-3ds-max-unity-unreal-engine/)

[https://www.puredevsoftware.com](https://www.puredevsoftware.com/blog/2018/03/17/texture-coordinates-d3d-vs-opengl/)

```
왼쪽 하단이 시작점인 대표적인 예 : OpenGL, Unity, 3Ds Max
```



### (2) SamplerState

- 메쉬에 Texture를 입히기 위해 몇 가지 규칙이 필요하다.
- SamplerState는 이러한 규칙 WrapMode와 FilterMode에 대한 정보를 담아둔 집합이다.
- 전통적으로 Texture 정보에 포함시켜왔지만 필요에 따라 별도로 적용이 가능하다

#### 가. WrapMode

- UV 좌표는 일반적으로 0~1 사이 값에 대응되지만 이 범위 밖의 값에 대한 표현도 허용한다.

- WrapMode는 좌표 범위를 벗어난 값에 대한 대응 규칙으로 아래와 같다

  - Repeat : 이미지를 반복한다.

  - Mirror : Repeat과 같지만 반복할때마다 미러링된다.
  - Clamp : 마지막(테두리) 값을 늘린다.
  - Border : 벗어난 값을 지정한 색으로 채운다.

![image-20221210102215622](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210102215622.png)

[https://learnopengl.com/Getting-started/Textures](https://learnopengl.com/Getting-started/Textures)

#### 나. Fillter Mode

- Texture Sampling하는 과정에서 Texture의 정보(해상도)와 표현하려는 Mesh에 대응되는 Pixel의 정보가 1:1이 아니기 때문에 문제가 발생

![image-20221210023124970](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210023124970.png)

```
위 그림을 보면 Texture와 메쉬에 대응되는 Pixel의 수가 다르다. 
또한 카메라에 따라 메쉬에 대응되는 Pixel 정보는 계속 달라진다.
```

- 이 같은 상황 때문에  Pixel에 대응되는 Texel 정보를 가져오는 규칙, Filter Mode가 있다
- Filter Mode는 크게 3가지의 필터가 존재
  - Point : Pixel에서 가장 가까운 Texel를 가져오며 나머지는 버린다
  - Linear : Pixel 주변의 4개의 Texel을 가져와 평균값을 구한다.
  - TriLinear : 방식은 Linear와 같으나 Mipmap을 사용할 경우 Mipmap Level 사이의 차이도 추가로 고려한다.

<div class = "cocoen">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210024910587.png" style="max-width:none; zoom:150%;"/>
<img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210025115853.png" style="zoom:150%;"/>
</div>

------

```
위는 Point와 Linear 필터의 차이를 보여준다
Point는 선명하나 Texel이 손실되어 계단처럼 층이 생기며, 이런 계단현상을 Aliasing 이라고 한다.
반대로 Linear는 흐리게 보이지만 Point와 비교했을때 Aliasing 문제가 어느정도 해결된 것을 볼수 있다.
이렇게 Texel의 손실이나 보간을 통해 Aliasing이 생기거나 흐려져 품질이 변하는 현상을 Texture Bleeding이라고 한다.

또한 필터는 Min(Texture보다 Mesh가 작은 경우), Mag(Texture보다 Mesh가 큰 경우),
Mip(Mipmap의 Level간 규칙) 상황에 대해 각각 설정이 가능하다
```



### (3) Anisotrophy Filter

- 일반적으로 Texture는 가로, 세로 크기가 같은 정방성이며 위의 FilterMode 또한 정방성에 기준을 둔다
- 하지만 화면에 표시되는 메쉬는 항상 정방성일 수 없다. 기본적으로 3D화면은 원근감을 가지며 카메라의 각도에 따라 비등방성으로 화면에 표시되기 때문이다
- 이런 비등방성 메쉬에 그대로 샘플링하게되면 또 다시 손실이 생기게 되는데 이를 개선하기 위해 비등방성에 맞게 텍스처를 변경하는 작업이 비등방성 필터이다.

![image-20221210104715974](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210104715974.png)

[https://www.intel.in/content/www/in/en/gaming/resources/what-is-anisotropic-filtering.html](https://www.intel.in/content/www/in/en/gaming/resources/what-is-anisotropic-filtering.html)

```
위 사진은 정방성 Filter를 사용했을때와 비등방성 Filter를 사용했을때의 차이를 보여준다.
바닥 부분의 품질 차이가 큰 것을 알수 있다.
```



## 2. Mipmap

![](https://docs.unity3d.com/kr/2022.1/uploads/Main/mipmaps.png)

[https://docs.unity3d.com/kr/2022.1/Manual/texture-mipmaps-introduction.html](https://docs.unity3d.com/kr/2022.1/Manual/texture-mipmaps-introduction.html)

- Mipmap은 원본 Texture를 단계별로 축소해 더 낮은 해상도의 Texture를 제공한다.
- 때문에 Mipmap을 사용하면 자연스레 메모리 사용률이  증가(30% 정도)하게 되지만 이로인해 얻을수 있는 장점이 생각보다 크다.

### (1) Texture Bleeding 완화

- 앞서 Texel과 Pixel이 1:1 대응되지 않으므로 Sampling 과정에서 손실이 발생하는 것과 그에 따라 Aliasing이나 블러링(흐려짐) 현상이 생긴다는 것을 보였다.
- 이러한 손실은 Texel과 Pixel 사이의 간극이 클수록 더 심각해진다.

#### 가. No_Mipmap

![1_uZXjZ_9bYO-blnI6S-gmsQ](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/1_uZXjZ_9bYO-blnI6S-gmsQ.gif)

```
위는 No_Mipmap, Linear Filter 상태에서 거리에 따라 생기는 손실된 상태를 보여준다.
거리가 멀어질수록 원본 Texture의 해상도와 메쉬의 Pixel 비율이 크게 달라져 샘플링시 손실이 커지며 
그로인해 Aliasing 문제가 크게 발생하는 것을 볼 수 있다.
```



#### 나. Mipmap

- Mipmap을 사용할 경우 거리에 따라 작아진 메쉬의 Pixel에 대응되는 축소된 Texture(가장 잘 맞는)를 사용하여 이러한 문제를 어느정도 해소해준다.

![1_88BbPuG2NSyfOlFdjWICYg](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/1_88BbPuG2NSyfOlFdjWICYg.gif)

```
위는 Mipmap, Linear Filter 상태에서 거리에 따른 비교이다.
Mipmap을 쓰지 않은 경우와 비교하면 Aliasing 현상이 많이 줄어들었다.
하지만 반대로 블러링이 생기며 특히 비등방성인 바닥의 품질 문제가 Level별로 심하게 떨어지는 것이 눈에 띈다.
```



#### 다. Anisotrophy

- 비등방성에 대한 Mipmap 문제를 해소하는 가장 쉬운 방법은 Anisotrophy Filter를 사용하는 것이다.

![1_HMi0_WQIiNE1TwKyLxSUTA](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/1_HMi0_WQIiNE1TwKyLxSUTA.gif)

```
Filter 상태에 따라 바닥의 품질에 크게 변하는 것을 확인할 수 있다.
```



#### 라.  Mipmap Level

- 비등방성 외에도 Mip Level 선택과 그 차이로 생기는 문제가 있다.
- 적절할 Mip Level의 선택과 조절을 통해 화면의 품질을 올릴 수 있다.

<div class = "cocoen">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Compare_Mip.png" style = "max-width:none;">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/Compare_Mip2.png">
</div>  

<p> </p>

```
위는 Mipmap, TriLinear 상태에서 Level Sampling을 조절한 결과이다.
Default : 기본 샘플링이며, 첫번째 칸 끝부분 부터 빠르게 흐려진다.
FixLOD : 0으로 고정한 상태로 샘플링한 것이며 블러링은 없지만 3번째 칸 부터 앨리어싱이 일어난다.
LOD(calc) : Level계산을 통해 FixLOD를 한 결과로 Default와 비교시 흐려지는 거리가 약간 차이가 난다.
SampleGrad : uv에 대한 ddx, ddy 정보를 파라미터로 전달하면 내부적으로 Level을 계산해 선택한다. 결과적으로 LOD(calc)와 동일.
Grad_Bias : Bias 값을 이용해 상황에 맞게 선택할 Level을 적절하게 조정한다.
보통 Bias값을 통해 필요해 따라 조정하는 방법을 많이 사용한다.
```



#### 마. 기타

- 위 방법 외에도 품질을 올리는 방법이 있는데 단순하게 샘플링을 여러번 하면된다.
- 기본적으로 GPU는 Texture Sampling을 한번만 수행하는데, 이를 반복적으로 수행해서 더 좋은 결과를 얻을 수 있다.
- 단점은 느리다.



### (2) Memory Bandwidth

- Mipmap 사용의 또 다른 장점은 메모리 대역폭의 최적화이다.
- GPU가 Texture를 읽을때 Pixel에 Origianl Texture가 아닌 Pixel 대응되는 적절한 Mip Level을 읽어들이면 된다.
- 일반적으로 Texture는 비디오 메모리에 로드된 상태이며 Sampling시 L1 캐시로 정보를 가져오게 되는데 이때 항상 데이터가 큰 Origianal Texture를 가져올 필요가 없어진다. 쉽게 말해 매우 작게 표시되는 메쉬에 굳이 데이터가 큰 Original Texture를 읽을 필요가 없다는 이야기



### (3)  Mipmap은 항상 사용하는게 좋은가?

- 위에서도 언급했다시피 Mipmap은 추가로 Memory를 사용한다.
- 거리의 개념이 없는 2D나 고정된 View를 제공하는 Topdown 형태의 게임에서는 Mipmap을 이용한 이점을 얻기 어렵다.
- 프로젝트의 환경과 플랫폼을 잘 고려해서 사용하자.

<br>



# Ref

- [https://bgolus.medium.com/sharper-mipmapping-using-shader-based-supersampling-ed7aadb47bec](https://bgolus.medium.com/sharper-mipmapping-using-shader-based-supersampling-ed7aadb47bec)