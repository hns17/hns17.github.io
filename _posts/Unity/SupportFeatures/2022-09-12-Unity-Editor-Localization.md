---
title: "Unity Editor Localization"
categories: [Unity/SupportFeatures]
tags: ["Unity", "Editor Localization", "Localization", "Editor", "L10n", "*.po"]
---



# Editor Localization

- Custom Editor의 텍스트를 Unity Language 설정에 맞춰 변경 할 수 있다.
- 유니티 2019 버전과 이후 버전에서 사용하는 API가 다르므로 가능하면 2020 이후 버전을 사용
- 해당 문서는 2021.3 버전 기준으로 작성



## 1. Unity Editor Language

- Unity 설치 시 언어 모듈을 포함하여 설치하면 Menu-Preferences 항목에서 언어 변경이 가능하다.

  ![image-20220912105332302](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912105332302.png)

- 언어 모듈은 허브를 통하여 추가 가능

![image-20220912105424428](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912105424428.png)



## 2. po 파일 만들기

- Editor Text를 현지화 하기 위해서는 po 파일을 작성해야 한다.

- po 파일은 Editor Localization 기능을 사용하기 위해 Unity Editor에서 인식하는 자산이며, 현지화에 따른 파일 이름은 아래와 같다.

  ![image-20220912110717758](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912110717758.png)

- po파일 작성은 별도의 Editor를 사용해 작성할 수 있지만, 형식이 복잡하지 않아 Notepad를 이용해도 쉽게 작성이 가능하다.

  - po format

    ```
    //Header info
    msgid ""
    msgstr ""
    "Language: ko\n"
    
    //아래부터 Localization StringTable
    msgid "Hello Localization"
    msgstr "안녕 현지화 테스트 중이야!"
    
    msgid "Write Test Code"
    msgstr "테스트 코드 작성"
    
    msgid "Finish"
    msgstr "마무리"
    ```

  

## 3. Assembly Definition 생성

- po 파일은 유니티 MainEditor 뿐만 아니라, 패키지 및 기타 커스텀 에디터에서도 사용되기 때문에 해당 파일의 사용 범위를 지정해야 한다.

- 범위 지정을 위해 AssemblyDefinition 파일을 생성해야 한다. 

  - AssemblyDefinition은 Unity QuickMenu를 통해 생성

  - Editor 용이므로 범위는 Editor로 지정

    ![image-20220912111845349](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912111845349.png)



## 4. Set Editor Localization Attribute

- Unity에서 제공하는 Editor Localization API를 사용하기 위해서 아래의 Attribute 설정이 필요

- cs file 생성 후 Localization Attribute를 작성

  - cs 파일 이름은 관계없어 보인다.

    ```csharp
    [assembly: UnityEditor.Localization]
    ```

    

## 5. Editor Localization API

- 작성된 po 파일의 텍스트를 가져오기 위해 Unity에서 API를 제공한다.

  - Unity 2019 : Localization

  - Unity 2020~ : L10n(Localization의 약자)

  - 공식문서 : [https://docs.unity3d.com/ScriptReference/L10n.html](https://docs.unity3d.com/ScriptReference/L10n.html)

    ![image-20220912130043742](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912130043742.png)



## 6. Localization API를 사용해 Custom Editor 만들기

- 현재까지 작성한 파일이 존재하는 폴더 아래에 대상이 되는 Custom Editor를 생성한다.

  ![image-20220912131943600](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912131943600.png)

- Editor  Localization API를 이용해 스크립트를 작성

  - L10n.Tr("key")

    ![image-20220912132522638](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912132522638.png)

- Unity Editor의 언어 설정에 따라 현지화가 적용된 모습

  - 왼쪽은 에디터 언어가 영어인 경우, 오른쪽은 한글은 경우

  ![image-20220912132959140](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20220912132959140.png)



## 7. 정리 및 나머지

- Unity는 Unity Editor의 언어 설정에 따른 Custom Editor Localization 기능을 제공한다.
- 다만 개인적으로 알아두고 사용하지는 않을  것으로 보임
  - AssemblyDefiniton 및 po 파일 작성 등 번거로움
  - 애초에 에디터 기능 대부분을 영어로 작성하며, 대규모 프로젝트의 상품화가 아니면 필요성을 느끼지 못함
  - Unity 2019와 2020 이후 버전의 API가 달라 Unity 버전을 신경써서 만들어야함
  - 필요한 경우 Unity Engine 언어설정이 아닌 Custom Editor 자체에 언어설정 값을 두고 사용할 것 같음
    - 다른 Package나 Editor 간 통일된 기능의 작성을 생각한다면 Unity Package의 Localization 기능을 사용하면 되지 않을까...
  - 가장 큰 이유는 해당 기능에 대한 제대로된 문서가 없음
    - Unity에서도 단순 편의성을 위한 기능 정도로 생각하는 느낌?
  - 유니티 엔진상의 이슈
    - 언어 변경시 엔진의 언어가 정상적으로 변경되지 않는 경우가 있으며 이 경우 CustomEditor도 변경되지 않음
    - Editor를 재실행하면 해결됨



# Ref

- [https://forum.unity.com/threads/package-ui-localization-is-available-in-2020-2.957173/]("https://forum.unity.com/threads/package-ui-localization-is-available-in-2020-2.957173/")
- [https://caitsithware.com/wordpress/archives/2227#Localization]("https://caitsithware.com/wordpress/archives/2227#Localization")
- [https://docs.unity3d.com/ScriptReference/L10n.Tr.html]("https://docs.unity3d.com/ScriptReference/L10n.Tr.html")
- [https://qiita.com/sator_imaging/items/81c9066caa9e21feda8c]("https://qiita.com/sator_imaging/items/81c9066caa9e21feda8c")
