---
title: git에 ssh key 등록하기
categories: Git/Git
tags: ["Git", "ssh"]


---



# Git ssh key 등록하기

- 윈도우에서 git ssh key 생성 후 git에 등록하기



## 1. git 설치확인 하기

- cmd 열고 git 입력하여 git이 정상적으로 설치되어 있는지 확인



## 2. ssh key 생성하기

![image-20240824122318921](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240824122318921.png)

(1) cmd에서 아래 내용 입력

- user email : 사용자 email

```
ssh-keygen -t rsa -b 4096 -C "user email"
```



(2) 생성될 파일 이름

- 입력하지 않는 경우 id_rsa로 생성

나머지는 전부 enter를 입력



## 3. 생성된 ssh key git에 등록

(1) 위에서 생성한 ssh public key 파일을 열어서 내용을 복사

- 파일의 기본 경로는 c:/users/@username/.ssh/@filename.pub

<br>

(2) git setting page 접속 후 ssh key 생성

![image-20240824123230562](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240824123230562.png)

- New SSH Key 버튼을 누른 후 나온 page에서 아래 내용을 작성 후 등록
  - Title : 원하는 타이틀
  - Key : 위에서 복사한 key 값을 붙여넣기



## 4.  확인하기

- cmd로 돌아와서 아래 내용을 입력

  ```
  ssh -T git@github.com
  ```

- 아래 메시지가 출력되는지 확인

  ![image-20240824124016458](C:\Users\Hns1n7\AppData\Roaming\Typora\typora-user-images\image-20240824124016458.png)



## ✨ 여러 계정의 ssh key 등록하기

(1) 위와 동일한 방법으로 각각의 git 계정에 대한 ssh key 생성 후 등록

- key 생성시 파일 이름을 지정해 각각 생성



(2) config 파일을 생성

-  ssh key가 생성된 폴더에 config 파일을 생성
  - 작성할 config 파일은 별도의 확장자가 없으며 파일명이 config



(3) 아래 내용을 작성

- Host @name
- IdentityFile @ssh_key_file_path

```
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



(4) 확인하기

- 아래 내용을 입력 후 출력되는 메시지를 각각 확인

  ```
  ssh -T first.git
  ssh -T second.git
  ```

  