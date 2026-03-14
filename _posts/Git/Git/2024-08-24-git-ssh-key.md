---
title: Git에 ssh key 등록하기
categories: Git/Git
tags: ["Git", "ssh"]


---

> 핵심 요약
> - Windows에서는 `ssh-keygen`으로 키를 만든 뒤 GitHub에 공개키를 등록하면 된다.
> - 마지막에 `ssh -T git@github.com`으로 연결 여부를 확인할 수 있다.
> - 계정이 여러 개라면 `~/.ssh/config`에서 Host alias를 나눠 관리하는 편이 안전하다.

이 글은 Windows 기준으로 GitHub용 SSH 키를 만드는 방법과, 여러 계정을 함께 쓸 때 설정을 분리하는 방법을 정리한다.

## 준비

- Git이 설치되어 있어야 한다.
- 명령 프롬프트나 PowerShell을 사용할 수 있어야 한다.
- GitHub 계정에 로그인할 수 있어야 한다.

## 1. Git 설치 확인

터미널을 열고 아래 명령어를 입력한다.

```bash
git --version
```

버전 정보가 나오면 정상적으로 설치된 상태다.

## 2. SSH 키 생성

![image-20240824122318921](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240824122318921.png)

아래 명령어를 실행한다.

```bash
ssh-keygen -t rsa -b 4096 -C "user email"
```

- `user email`에는 GitHub 계정에 사용하는 이메일을 넣는다.
- 파일 이름을 따로 입력하지 않으면 기본값인 `id_rsa`로 생성된다.
- 나머지 질문은 특별한 이유가 없으면 Enter로 진행해도 된다.

## 3. GitHub에 공개키 등록

먼저 생성된 공개키 파일을 열어 내용을 복사한다.

- 기본 경로 예시: `C:\Users\사용자이름\.ssh\id_rsa.pub`

그 다음 GitHub의 SSH key 등록 화면으로 이동해 새 키를 추가한다.

![image-20240824123230562](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240824123230562.png)

등록할 때는 아래 두 항목을 입력하면 된다.

- `Title`: 키를 구분할 수 있는 이름
- `Key`: 방금 복사한 공개키 내용

## 4. 연결 확인

등록이 끝났다면 다시 터미널로 돌아와 아래 명령어를 실행한다.

```bash
ssh -T git@github.com
```

정상적으로 연결되면 GitHub에서 인증 메시지를 출력한다.

![image-20240824124016458](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240824124016458.png)

## 여러 계정을 함께 쓰는 방법

### 1. 계정별로 키를 따로 만든다

- 각 계정마다 다른 파일 이름으로 SSH 키를 생성한다.
- 예를 들어 `id_rsa`, `id_rsa_hns17`처럼 구분해 두면 관리가 편하다.

### 2. `config` 파일을 만든다

`~/.ssh` 폴더 안에 `config` 파일을 만든다.

- 확장자는 없다.
- 파일 이름 그대로 `config`다.

### 3. Host alias를 작성한다

```sshconfig
# 첫 번째 GitHub 계정
Host first.git
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa

# 두 번째 GitHub 계정
Host second.git
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_hns17
```

이렇게 설정해 두면 저장소마다 다른 Host를 사용해 원하는 계정으로 인증할 수 있다.

### 4. 각 alias를 테스트한다

```bash
ssh -T first.git
ssh -T second.git
```

각 명령어가 서로 다른 계정으로 정상 인증되는지 확인하면 된다.

## 정리

- SSH 키 등록 자체는 `키 생성 -> 공개키 등록 -> 연결 확인` 세 단계로 끝난다.
- 여러 계정을 함께 쓰면 키를 분리하고 `config`에서 alias를 나누는 편이 충돌을 줄이기 쉽다.
- 나중에 push 권한 문제가 생기면 "현재 어떤 Host와 어떤 키를 쓰는지"부터 확인하면 된다.
