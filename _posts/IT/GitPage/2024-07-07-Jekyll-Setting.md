---
title: GitPage 사용을 위해 Local에 Jekyll 환경 설정하기 
categories: IT/GitPage
tags: ["Jekyll"]


---



# Jekyll

- Jekyll은 정적 웹사이트 생성기(Static Site Generator)

  - 마크다운(Markdown)을 사용하여 웹 페이지를 작성할 수 있습니다.

  - 템플릿 엔진을 사용하여 HTML 페이지를 생성합니다.

  - 콘텐츠와 디자인을 분리하여 관리할 수 있습니다.

  - GitHub Pages와 연동하여 손쉽게 웹 사이트를 배포할 수 있습니다.

  - 블로그, 포트폴리오, 문서 사이트 등 다양한 용도로 활용할 수 있습니다.

  - 오픈소스 프로젝트이며, Ruby 언어로 개발되었습니다.



# GitPage와 Jekyll

- GitHub Pages는 Jekyll을 기반으로 하는 정적 사이트 생성기를 기본적으로 지원하기 때문에 많은 사람들이 GitHub Pages와 함께 Jekyll을 사용

- 로컬에 환경을 구축해놓으면 Posting 내용을 Repo에 push하기 전에 미리 확인이 가능하다.



# Setting

- 아래는 윈도우 환경에서 Jekyll 환경 구성을 요약합니다.

- 맥의 경우 기본적으로 루비는 설치되어 있으며, RubyGems 등을 이용해 설치하시면 됩니다.

  

#### 1. Ruby 설치

- Jekyll은 Ruby 언어로 개발되어 있기 때문에 우선 루비를 설치한다.

  - https://rubyinstaller.org/downloads/ 가서 적절한 버전을 받은 후 인스톨

  - install 창에 나오는 모든 항목을 체크하자

  - 진행 중 콘솔 창이 열리면 Msys2 base installation, 1 입력 후 엔터

  - 정상적으로 설치되었다면 이제 Ruby 명령어를 사용할 수 있다.

    - 콘솔 창에서 ruby -v를 입력하면 설치된 루비 버전 확인이 가능하다.

    ![image-20240707211257145](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240707211257145.png)

![image-20240707212034913](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240707212034913.png)

![image-20240707212840140](https://raw.githubusercontent.com/hns17/ImageContainer/main/img/image-20240707212840140.png)



#### 2. Jekyll 설치

- Ruby가 설치되었으면 패키지 서버에서 Jekyll을 설치한다.
  - gem install bundler 입력하여 bundler 설치
  - gem install jekyll 입력하여 Jekyll 설치



#### 3. Local host로 확인하기

- 이제 콘솔에서 github page 디렉토리로 이동 후 bundle install 을 입력하여 bundle을 설치합니다.
  - 만약 bundle install error가 뜨면 gemfile.lock 삭제 후 다시 설치
- bundle exec jekyll serve 를 입력하여 jekyll 페이지를 로컬에 생성합니다.



#### 4. 브라우저에서 확인

- 3까지 모든 작업이 마무리 되면 브라우저의 검색 창에 localhost:4000을 입력하여 정상적으로 페이지가 보이는지 확인