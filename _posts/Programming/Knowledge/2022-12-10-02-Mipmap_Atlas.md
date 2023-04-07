---
title: Mip과 Atlas
categories: Programming/Knowledge
tags: ["Mipmap", "Texture", "AtlasSheet", "Atlas"]
---



# Mipmap과 AtlasSheet

## Atlas Sheet

![image-20221210180019875](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210180019875.png)

[https://www.gamedeveloper.com](https://www.gamedeveloper.com/programming/practical-texture-atlases)

- 단일 마테리얼을 사용하여 드로우 콜을 줄이기 위해 여러개의 텍스처를 하나의 시트로 통합하여 사용하는 것
- 렌더링 최적화를 위해 전통적으로 많이 사용되고 있지만 단점 또한 존재한다.



### (1) UV 계산

- 사용하려면 UV 계산이 필요하다.
- 어느 위치에 어느 Texture를 가져올지 인덱스 단위로 좌표화할 필요가 있다.
- 사용하는 엔진이나 그래픽스 라이브러리의 UV Coordinate도 신경써야 한다



### (2) Sheet 화

- Sheet를 만들어야 한다.
- 텍스처를 추가할 때마다 추가 작업을 수행해야하는데 툴이 있지만 생각보다 번거롭다.



### (3) Mipmap Issue

- 사실 위의 두 가지는 크게 문제가 되지 않지만, Mipmap과 관련된 문제는 상당히 난처하다.
- 아틀라스 시트를 사용하게 되면 경계선과 관련된 이음새 문제가 발생하며 특히 Mipmap을 사용하게 되면 눈에 띄게 문제가 심각해진다.



#### 가.  타일의 경계를 넘어 가져오는 텍셀에 대한 이음새 문제

- 텍스처 샘플링시 경계선 근처에서 샘플링 하게 될 경우 잘못된 텍셀 선택으로 인한 이음새가 생긴다

- 이음새 문제는 타일과 타일 사이에 패딩 값을 넣어 어느정도 해결이 가능하다.

![image-20221210181650569](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20221210181650569.png)

[https://0fps.net](https://0fps.net/2013/07/09/texture-atlases-wrapping-and-mip-mapping/)

```
아틀라스 텍스처의 경계선 근처에서 발생하는 문제
```



#### 나. Mip Level 간에 생기는 해상도 문제

- 서로 다른 Mip Level로 인해 품질 문제가 생기며 이 또한 경계선의 이음새 문제로 발전한다.



#### 다. 아래 부터는 각 상황 별로 발생하는 문제를 비교해보았다

[No_Mipmap Point, Linear]

<div class = "cocoen">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img//No_mip_point.png" style = "max-width:none;">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/No_mip_biliner.png">
</div>

<p> </p>

```
Point의 경우 샘플링 특성상 가장 가까운 정보를 가져오기 때문에 밉맵을 사용하지 않으면 이음새 문제를 확인하기 어렵다
Linear의 경우 자세히 보면 검은색 점선이 그어져 있는것이 보인다
```

<br>

[Mipmap Point, Linear]

<div class = "cocoen">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/mip_point.png" style = "max-width:none;">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/mip_biliner.png">
</div>

<p> </p>

```
Mipmap을 사용하게되면 문제가 확실하게 보인다.
이음새도 명확하게 보이며 뒷 쪽을 보면 레벨간 텍스처가 뭉게진게 보인다.
Point와 Linear 샘플링을 서로 비교해보면 주변 Texel 정보를 참조해서 Pixel 값을 정하는 
Linear에서 오류가 심해지는 것을 알 수 있다.
```

<br>

[Mipmap Point, Linear SampleGradBias]

<div class = "cocoen">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/grad_02_point.png" style = "max-width:none;">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/grad_02_liner.png">
</div>

<p> </p>

```
위는 SampleGrad 함수를 통해 적절한 Mip Level을 선택하도록 한 결과이다
적절하지 못한 레벨 선택으로 인한 이슈가 없어져 뒷 쪽의 뭉게지는 현상이 사라졌다
Point의 경우 크게 문제가 없어 보이나 Linear의 경우 많이 개선되었지만 여전히 경계선에서 Texel 정보를 가져올 때 문제가 생긴다.
```

<br>

[Mipmap Point, Linear Multi Sampling]

<div class = "cocoen">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/4tap_point.png" style = "max-width:none;">
    <img src = "https://raw.githubusercontent.com/hns17/ImageContainer/main/img/4tap_liner.png">
</div>

<p> </p>

```
위는 특수한 방법에 의해 여러번 샘플링된 결과이다
Point는 물론이고 Linear에서도 이음새 문제가 눈에띄게 개선되었다.
문제는 샘플링을 여러번(4번)하기 때문에 무겁다.
```



## Result

- 기본적으로 아틀라스 시트와 Mipmap은 서로 어울리지 않는 느낌이다.
- 아틀라스 시트와 Mipmap을 같이 사용 할 경우 적절한 Mip Level을 계산하고 Bias 등으로 조절하는 것이 좋다.
- 아틀라스 시트와 Mipmap을 같이 사용 할 경우 경계선 샘플링 문제로 인해 패딩 값을 넣거나 그렇지 않으면 Sampling을 Point로 사용해야 한다.
- Texture Array를 사용할 수 있다면  Texture Array를 사용하자