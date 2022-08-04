---
title: GitPage 이미지 관리하기
categories: IT/GitPage
tags: ["GitPage"]
---





# Jekyll Theme 사용시 이미지 관리하는 방법

- Jekyll Theme가 적용된 GitPage에서 포스팅에 사용되는 이미지 관리 방법들을 정리






## 1. Relative URL

- Repository 기준의 상대경로를 사용하여 표시

  

#### (1) Root-Relative URL

- 루트에 고정된 폴더를 기준으로 사용
- 주로 Asset/Image를 사용한다.
- Typora Edit를 사용할 경우 문서에 삽입되는 이미지의 저장 경로를 지정해서 작업완료 후 같이 업로드하면 편리하다
- 이미지 경로 Setting으로 인해 GitPage 가 아닌 다른 문서 작성시에도 작성 문서 기준 저장 경로에 이미지 사본이 저장되어 불편함



#### (2) Document-Relative URL

- Jekyll을 사용한 GitPage와 Github의 Document 기준 상대경로 인식방식이 달라 사용하기 어렵다.



#### (3) Test

![assets/images/test_image.png](/assets/images/test_image.png)

![/assets/images/test_image.png](/assets/images/test_image.png)

![/_posts/IT/GitPage/Images/test_image.png](/assets/images/test_image.png)

![Image/test_image.png](Image/test_image.png)

![/Image/test_image.png](Image/test_image.png)

![./Image/test_image.png](Image/test_image.png)

| Link | GitPage | GitHub |
| ---- | ------- | ------ |
|      | Failed  | Good   |
|      | Failed  | Good   |
|      | Failed  | Good   |



## 2. Absoulte URL

#### (1) Github Issue 활용하기

- Github의 이슈 트래커에 이미지를 끌어다 놓을 경우 나오는 Link를 문서에 사용
- 편리한 방법이라고 여기저기 소개되어 있는데.... 이게 편한가?



#### (2) Typora Upload

- Typora를 사용하는 경우 문서에 사용된 이미지를 Github의 레포지토리와 연결해 Upload가 가능하다.
- 현재 사용중인 방법으로 가장 편한것 같다.
- Page용으로만 문서를 작성하는  경우 GitPage Repository를 연결하면 됨
  - 나 같은 경우는 다른 문서에 사용될 이미지도 같이 관리하기 위해 Image 저장용 레포지토리를 따로 구성함