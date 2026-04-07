---
title: "Clobie - 그림"
permalink: /clobie/art/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
  summary_label: "그림 작업실"
classes: wide
---

그림 작업실은 디스코드 그림 채널의 이미지를 **갤러리 중심 아카이브**로 정리하는 공간입니다.

{% assign all_art = site.clobie_art | sort: 'date' | reverse %}
{% assign character_count = site.clobie_art | where: 'clobie_type', 'character' | size %}
{% assign creature_count = site.clobie_art | where: 'clobie_type', 'creature' | size %}
{% assign background_count = site.clobie_art | where: 'clobie_type', 'background' | size %}
{% assign mecha_count = site.clobie_art | where: 'clobie_type', 'mecha' | size %}

<div class="clobie-grid clobie-grid--3 clobie-section-gap">
  <div class="clobie-card">
    <p class="clobie-eyebrow">전체 이미지</p>
    <h3>{{ all_art | size }}개</h3>
    <p>현재 그림 작업실에 정리된 전체 이미지 수입니다.</p>
  </div>
  <div class="clobie-card">
    <p class="clobie-eyebrow">유형 분포</p>
    <h3>캐릭터 {{ character_count }} · 생물 {{ creature_count }} · 배경 {{ background_count }}{% if mecha_count > 0 %} · 메카 {{ mecha_count }}{% endif %}</h3>
    <p>기본 탐색 축은 그림 유형 기준입니다.</p>
  </div>
  <div class="clobie-card">
    <p class="clobie-eyebrow">보관 방식</p>
    <h3>Container + MD</h3>
    <p>원본 이미지는 clobie-image-container, 페이지 레포에는 메타 문서만 저장합니다.</p>
  </div>
</div>

## 유형별 보기

<div class="clobie-grid clobie-grid--3">
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/art/characters/' | relative_url }}">
    <p class="clobie-eyebrow">{{ character_count }}개 이미지</p>
    <h3>캐릭터</h3>
    <p>인물 중심 이미지와 캐릭터 컨셉을 모아봅니다.</p>
  </a>
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/art/creatures/' | relative_url }}">
    <p class="clobie-eyebrow">{{ creature_count }}개 이미지</p>
    <h3>생물</h3>
    <p>동물, 수호수, 몬스터 같은 비인간 존재를 모아봅니다.</p>
  </a>
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/art/backgrounds/' | relative_url }}">
    <p class="clobie-eyebrow">{{ background_count }}개 이미지</p>
    <h3>배경</h3>
    <p>풍경, 공간, 도시와 환경 중심 이미지를 모아봅니다.</p>
  </a>
</div>

## 최근 이미지

{% if all_art.size > 0 %}
<div class="clobie-gallery">
  {% for item in all_art limit: 9 %}
  <a class="clobie-gallery__item" href="{{ item.url | relative_url }}">
    {% if item.image_url %}
    <img src="{{ item.image_url }}" alt="{{ item.title }}">
    {% else %}
    <div class="clobie-gallery__placeholder">No Image</div>
    {% endif %}
    <div class="clobie-gallery__caption">
      <strong>{{ item.title }}</strong>
      <span>{{ item.clobie_type | default: '미분류' }}{% if item.mood %} · {{ item.mood }}{% endif %}</span>
    </div>
  </a>
  {% endfor %}
</div>
{% else %}
<div class="clobie-empty">
  아직 등록된 그림이 없습니다. 추후 디스코드 그림 채널의 작업물을 갤러리 중심으로 정리할 예정입니다.
</div>
{% endif %}

## 추천 메타데이터

- `클로비 타입`: character / creature / background / mecha / object / scene
- `장르`: fantasy / sf / mystery / horror / daily 등
- `감성`: warm / calm / mystical / dreamy / dark / epic 등
- `태그`: 탐색용 키워드
- `image_url`: clobie-image-container의 최종 PNG URL
- `prompt`, `source_tool`, `source_model`, `chatgpt_share_url`: 생성 기록용
