---
title: "Clobie - 글"
permalink: /clobie/writing/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
  summary_label: "글 작업실"
classes: wide
---

글 작업실은 디스코드 글 채널에서 올라오는 창작물을 **유형 중심 아카이브**로 다시 묶는 공간입니다.

<div class="clobie-grid clobie-grid--3">
  {% for item in site.data.clobie.writing_types %}
  {% assign count = site.clobie_writing | where: "clobie_type", item.key | size %}
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/writing/' | append: item.key | append: '/' | relative_url }}">
    <p class="clobie-eyebrow">{{ count }} items</p>
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>
  </a>
  {% endfor %}
</div>

## 최근 글

{% assign recent_writings = site.clobie_writing | sort: 'date' | reverse %}
{% if recent_writings.size > 0 %}
<div class="clobie-list">
  {% for post in recent_writings limit: 6 %}
  <article class="clobie-card">
    <p class="clobie-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ post.clobie_type | default: '미분류' }}{% if post.genre %} · {{ post.genre }}{% endif %}</p>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.summary %}<p>{{ post.summary }}</p>{% elsif post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 120 }}</p>{% endif %}
  </article>
  {% endfor %}
</div>
{% else %}
<div class="clobie-empty">
  아직 등록된 글이 없습니다. 추후 디스코드 글 채널의 작업물을 설정 / 스토리 / 메모로 분류해 이곳에 연결할 예정입니다.
</div>
{% endif %}

## 추천 메타데이터

- `clobie_type`: settings / stories / notes
- `genre`: fantasy / sf / mystery / horror / daily / emotional 등
- `series`: 같은 세계관/연작 식별자
- `tags`: 탐색용 키워드
- `source_channel`, `source_message_id`: 디스코드 원본 추적용
