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
{% assign character_items = site.clobie_art | where: 'clobie_type', 'character' %}
{% assign creature_items = site.clobie_art | where: 'clobie_type', 'creature' %}
{% assign scene_items = site.clobie_art | where: 'clobie_type', 'scene' %}
{% assign sf_items = site.clobie_art | where: 'clobie_type', 'sf' %}

<div class="clobie-grid clobie-grid--2 clobie-section-gap">
  <div class="clobie-card">
    <p class="clobie-eyebrow">전체 이미지</p>
    <h3>{{ all_art | size }}개</h3>
    <p>현재 그림 작업실에 정리된 전체 이미지 수입니다.</p>
  </div>
</div>

## 유형별 보기

<div class="clobie-type-nav clobie-section-gap">
  <a class="clobie-type-pill" href="{{ '/clobie/art/characters/' | relative_url }}">
    <strong>캐릭터</strong>
    <span>{{ character_items | size }}</span>
  </a>
  <a class="clobie-type-pill" href="{{ '/clobie/art/creatures/' | relative_url }}">
    <strong>생물</strong>
    <span>{{ creature_items | size }}</span>
  </a>
  <a class="clobie-type-pill" href="{{ '/clobie/art/scenes/' | relative_url }}">
    <strong>장면</strong>
    <span>{{ scene_items | size }}</span>
  </a>
  <a class="clobie-type-pill" href="{{ '/clobie/art/sf/' | relative_url }}">
    <strong>SF</strong>
    <span>{{ sf_items | size }}</span>
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

- `클로비 타입`: character / creature / scene / sf
- `장르`: fantasy / sf / mystery / horror / daily 등
- `감성`: warm / calm / mystical / dreamy / dark / epic 등
- `태그`: 탐색용 키워드
- `image_url`: clobie-image-container의 최종 PNG URL
- `prompt`, `source_tool`, `source_model`, `chatgpt_share_url`: 생성 기록용
