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

<div class="clobie-grid clobie-grid--3">
  {% for item in site.data.clobie.art_types %}
  {% assign count = site.clobie_art | where: "clobie_type", item.key | size %}
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/art/' | append: item.key | append: '/' | relative_url }}">
    <p class="clobie-eyebrow">{{ count }} items</p>
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>
  </a>
  {% endfor %}
</div>

## 갤러리 미리보기

{% assign recent_art = site.clobie_art | sort: 'date' | reverse %}
{% if recent_art.size > 0 %}
<div class="clobie-gallery">
  {% for item in recent_art limit: 9 %}
  <a class="clobie-gallery__item" href="{{ item.url | relative_url }}">
    {% if item.image %}
    <img src="{{ item.image | relative_url }}" alt="{{ item.title }}">
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
  아직 등록된 그림이 없습니다. 추후 디스코드 그림 채널의 작업물을 썸네일과 태그 중심으로 정리할 예정입니다.
</div>
{% endif %}

## 추천 메타데이터

- `클로비 타입`: 캐릭터 / 배경·풍경 / 콘셉트·러프
- `감성`: 따뜻함 / 몽환 / 어두움 / 사이버펑크 / 판타지 등
- `시리즈`: 같은 시리즈/세계관 식별자
- `대표 이미지`: 대표 이미지 경로
- `프롬프트`, `source_channel`, `source_message_id`: 원본 기록용
- `source_path`: 원본 md 문서 경로 (중복 이관 방지용)
