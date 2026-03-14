---
title: SourceTree에 VS Code merge tool 연결하기
categories: Git/Git
tags: ["Git", "SourceTree", "vs-code", "diff-tool", "merge-tool"]

---

> 핵심 요약
> - 이 글은 `SourceTree에 VS Code merge tool 연결하기` 작업 절차를 정리한다.
> - 설정 순서와 확인 방법을 단계별로 정리한다.
> - 실행 중 막히기 쉬운 지점도 함께 확인할 수 있게 정리한다.

- 소스트리의 diff, merge tool은 사용하기 불편하고 편리한 외부 병합 툴들은 유료
- 무료 툴 중에서 가장 괜찮아 보이는 vs code merge tool을 연결해서 사용

![image-20240728105208484](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728105208484.png)

## 1. VS Code 설치

- [VS Code]("https://code.visualstudio.com/") 를 다운로드 후 설치

## 2. VS Code 설정

- merge tool 활성화

  - 설치한 VS Code를 실행한 후 File - Preferences - Setting 목록에서 Git:Merge Editor 체크박스 체크

    ![image-20240728102549192](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728102549192.png)

### ️ Mac인 경우 터미널 코드 활성화가 필요

- vs code 상단의 프롬프트 입력란에 >shell commmand 입력 후 code 설치
  - ref : https://code.visualstudio.com/docs/setup/mac

![image-20240728014034537](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728014034537.png)

### Mac Permission Error

![image-20240728014726361](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728014726361.png)

- Mac에서 위와 같은 문제가 발생할 경우 터미널을 통해 bin 접근 후 code 삭제 후 다시 설치

```
cd /usr/local/bin
sudo rm -rf code
```

## 3. SourceTree와 연결하기

#### (1). Window

![image-20240728103940632](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728103940632.png)

- 도구 - 옵션 창 - 비교 탭으로 이동

- 외부 비교 / 병합 항목의 도구를 커스텀으로 변경 후 명령어와 변수를 입력

  - 명령어 : VS Code 설치 위치 입력

    - diff, merge 동일

      ```
      C:\Users\xxxx\AppData\Local\Programs\Microsoft VS Code\Code.exe
      ```

  - 변수

    - diff tool

      ```
      -n -w -d $LOCAL $REMOTE
      ```

    - merge tool

      ```
      -n -w $MERGED
      ```

#### (2) Mac

- SourceTree - 설정 창 - 비교 탭으로 이동

- 외부 비교 / 병합 항목의 도구를 커스텀으로 변경 후 명령어와 변수를 입력

  - 명령어 : 아래 내용 입력

    - diff, merge 동일

      ```
      /usr/local/bin/code
      ```

  - 변수

    - diff tool

      ```
      -n -w -d $LOCAL $REMOTE
      ```

    - merge tool

      ```
      -n -w $MERGED
      ```

## 확인하기

#### 가. 외부 병합툴 시작하기

- conflict가 발생한 항목에서 오른쪽 마우스 버튼을 클릭 후 충돌해결 - 외부 병합 툴 시작 선택

![image-20240728104704242](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728104704242.png)

#### 나. 정상적으로 설정 되었으면 아래와 같이 vs code가 실행된다.

- resolve in merge editor 버튼을 클릭해 merge tool로 전환

![image-20240728104955289](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728104955289.png)

#### 다. vs code merge tool로 전환된 모습

- check box를 이용해 필요한 내용을 선택적으로 컨트롤 할 수 있다.
- 작업을 완료하고 save 후 창을 닫으면 source tree 상에서 conflict가 해결된 것을 확인할 수 있다.
  - 백업으로 생성된 .orig 파일은 제거해도 됨

![image-20240728105208484](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728105208484.png)

## Check box가 나오지 않는 경우 표시하기

- VS Code merge tool에서 체크박스가 표시되지 않는 경우

#### 가. Setting 창에서 아래 표시된 버튼을 클릭하여 Json으로 전환

![image-20240728110315280](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728110315280.png)

#### 나. 아래 내용 추가 후 확인

![image-20240728110716798](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240728110716798.png)

```
    "mergeEditor.showCheckboxes": true,
    "mergeEditor.showCodeLenses": false,
```
