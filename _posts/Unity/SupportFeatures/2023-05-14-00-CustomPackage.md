---
title: "Unity CustomPackage"
categories: [Unity/SupportFeatures]
tags: ["Unity", "CustomPackage", "PackageManager", "Install", "GitURL"]
---



# Unity Custom Package

- Unity PackageManager는 공식 패키지 뿐만 아니라 사용자가 만든 패키지의 관리도 지원한다.
- 해당 문서에서는 PackageManager의 git url을 통해 추가하는 Custom Package를 만드는 방법을 작성한다.



> # Custom Package 구성하는 방법

- 공식문서에서는 두 가지 방식을 제안하고 있다.

  - Ref : [https://docs.unity3d.com/kr/2019.4/Manual/CustomPackages.html](https://docs.unity3d.com/kr/2019.4/Manual/CustomPackages.html)

  - 내장 패키지 : 프로젝트 내의 Packages 폴더 안에 구성
  - 로컬 패키지 : 별도의 사용자 저장소에 구성

- Git을 이용한다면 개인적으로 두 방식보다는 프로젝트의 Assets 폴더 내에서 로컬 패키지 형태로 구성하는 것을 선호한다.

  - Assets 폴더 내에서 구성할 경우 필요할 때 Test하고, Update 하기 쉽다.
  - 배포는 Package가 설치된 url을 이용하거나, 필요한 파일만 unity package 파일로 export하면 됨.

- Package에 포함될 수 있는 파일은 아래와 같다.
  - C# 스크립트
  - 어셈블리
  - 네이티브 플러그인
  - 모델, 텍스처, 애니메이션 및 오디오 클립, 기타 에셋.



> # Git을 통해 배포되는 CustomPackge 만들어 보기

가. Repo 생성하기

- Github에 Unity Project 용 Repo를 만든다.
  - [https://github.com/hns17/UpmTest/tree/main](https://github.com/hns17/UpmTest/tree/main)

나. 유니티 프로젝트 생성하기
- 클론 받은 폴더에 유니티 프로젝트를 생성한다.

다. Assets 폴더 내에 패키지 폴더 생성하기

- Unity를 실행 후 패키지 파일이 위치할 폴더를 만든다.
  - 해당 문서에서는 UpmTest로 만들었다.

- 패키지 폴더의 기본적인 구조는 [공식 문서](https://docs.unity3d.com/kr/2021.3/Manual/cus-layout.html)에서 확인할 수 있다.

라. package.json 파일 만들기
- package.json 작성에 대한 자세한 내용은 [공식 문서]()를 참고한다.
- 아래는 간단한 정보로 작성한 package.json 파일의 내용이다.

```json
{
	"name": "com.hns17.upmtest",
	"displayName": "Unity Package json Test",
	"version": "1.0.0",
	"unity": "2019.4",
	"description": "My Unity Utility Test.",
	"author": {
		"name": "HNS17",
		"email": "hns17@naver.com"
	}
}
```

마. 지금까지 작업한 내용을 Git에 Push한다.

바. PackageManager용 Git Url
- PackageManager를 통해 추가할 CustomPackage의 git url은 package.json이 있는 위치를 가리켜야 한다.
- Install url 규칙은 아래와 같다.
  - url에 대한 규칙은 [공식 문서](https://docs.unity3d.com/kr/2021.3/Manual/upm-git.html)에서 확인할 수 있다.

![image-20230514081252624](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230514081252624.png)

```
//GitUrl + ?path= + package.json 위치
https://github.com/hns17/UpmTest.git?path=Assets/UpmTest
```

사. PackageManager를 통해 추가하기

- 작성한 패키지를 추가할 유니티 프로젝트를 연다.
  - 프로젝트에 동일한 패키지를 여러개 가질 수 없으므로 작업한 프로젝트가 아닌 다른 프로젝트에서 추가해야 함.

- 패키지 매니저를 열고 좌측 상단 + 버튼을 눌러 git url에서 패키지 추가 항목을 선택한다.
- 위에서 만든 url을 입력하고 추가한다.
  - https://github.com/hns17/UpmTest.git?path=Assets/UpmTest

- Result
  - 패키지매니저에 추가된 패키지 정보를 확인할 수 있다.
  - 프로젝트의 Packages 항목을 통해 패키지가 정상적으로 설치되었는지 확인할 수 있다.

![image-20230514083747718](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230514083747718.png)



> # Package에 Script 추가하기

- 스크립트를 작성 후 추가한다.

- 폴더 내에 asemdef 파일을 만들어 준다.

  - 패키지를 통해 Script 파일을 배포할 경우 assembly 영역 지정이 필요하다.

  - 유니티의 Create 메뉴를 통해 쉽게 생성할 수 있다.

  - Ref : [https://docs.unity3d.com/kr/2021.3/Manual/cus-asmdef.html](https://docs.unity3d.com/kr/2021.3/Manual/cus-asmdef.html)

![image-20230514084505302](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230514084505302.png)



> # Update CustomPackage

- 기능을 추가하거나 수정한 경우 package.json파일의 version 정보를 변경후 Git에 Push한다.

- 하위 버전을 사용중인 경우 PackageManager에서 Update 버튼을 통해 최신 버전으로 업데이트 가능하다.

  ```json
  {
  	...
  	"version": "1.0.1",
  	...
  }
  ```

![image-20230514085543405](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230514085543405.png)



> # Version 전환은?

- git url을 통해 추가된 custom package는 버전 전환 기능을 제공하지 않는다.

- Ref : [https://docs.unity3d.com/kr/2021.3/Manual/upm-ui-update.html](https://docs.unity3d.com/kr/2021.3/Manual/upm-ui-update.html)

![image-20230513234955200](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230513234955200.png)



> # 발생 할 수 있는 Issue

- Custom Package를 만들때 발생 가능한 몇 가지 Issue들



> ## Package Name Issue

- package name 은 대문자를 사용할 수 없다.

```
package.json
{
	"name": "com.hns17.Upmtest",
	...
}

[패키지 관리자 창] UPM 작업을 수행할 수 없습니다.: Unable to add package [https://github.com/hns17/UpmTest.git]:
  Manifest [D:\Project\Unity\UNITY_IL_TEST\Library\PackageCache\com.hns17.Upmtest@acf95f6ceb\package.json] is invalid:
    Package name 'com.hns17.Upmtest' is invalid. [NotFound].
UnityEditor.EditorApplication:Internal_CallUpdateFunctions ()
```



> ## Dependency Issue

- package.json의 dependency 항목은 git 종속성을 지원하지 않는다.
- Ref : [https://docs.unity3d.com/kr/2021.3/Manual/upm-git.html](https://docs.unity3d.com/kr/2021.3/Manual/upm-git.html)

![image-20230513232857802](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230513232857802.png)

```
[패키지 관리자 창] UPM 작업을 수행할 수 없습니다.: Unable to add package [https://github.com/hns17/UpmTest.git]:
  Package com.hns17.upmtest@https://github.com/hns17/UpmTest.git has invalid dependencies or related test packages:
    com.cysharp.unitask (dependency): Version 'https://github.com/Cysharp/UniTask.git?path=src/UniTask/Assets/Plugins/UniTask' is invalid. Expected a 'SemVer' compatible value. [NotFound].
UnityEditor.EditorApplication:Internal_CallUpdateFunctions ()
```



> ## MetaFile Issue

- Package 배포시 meta 파일도 포함하여야 한다.
- meta파일이 없는 경우 아래와 같은 오류가 발생한다.

![image-20230511233647015](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20230511233647015.png)