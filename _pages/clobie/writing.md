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

글 작업실은 디스코드 글 채널과 원본 md 문서에서 올라온 창작물을 **유형 중심 아카이브**로 다시 묶는 공간입니다.

{% assign all_writings = site.clobie_writing | sort: 'date' | reverse %}
{% assign setting_count = site.clobie_writing | where: 'clobie_type', 'settings' | size %}
{% assign story_count = site.clobie_writing | where: 'clobie_type', 'stories' | size %}
{% assign note_count = site.clobie_writing | where: 'clobie_type', 'notes' | size %}
{% assign series_count = site.clobie_writing | map: 'series' | uniq | compact | size %}

<div class="clobie-grid clobie-grid--3">
  <div class="clobie-card">
    <p class="clobie-eyebrow">전체 문서</p>
    <h3>{{ all_writings | size }}개</h3>
    <p>현재 클로비 글 작업실에 정리된 전체 글 수입니다.</p>
  </div>
  <div class="clobie-card">
    <p class="clobie-eyebrow">유형 분포</p>
    <h3>설정 {{ setting_count }} · 스토리 {{ story_count }}{% if note_count > 0 %} · 메모 {{ note_count }}{% endif %}</h3>
    <p>기본 탐색 축은 유형 기준입니다.</p>
  </div>
  <div class="clobie-card">
    <p class="clobie-eyebrow">시리즈</p>
    <h3>{{ series_count }}개</h3>
    <p>같은 세계관과 연작 단위로 묶인 시리즈 수입니다.</p>
  </div>
</div>

## 유형별 보기

<div class="clobie-grid clobie-grid--3">
  {% for item in site.data.clobie.writing_types %}
  {% assign count = site.clobie_writing | where: 'clobie_type', item.key | size %}
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/writing/' | append: item.key | append: '/' | relative_url }}">
    <p class="clobie-eyebrow">{{ count }}개 문서</p>
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>
  </a>
  {% endfor %}
</div>

## 탐색 허브

<div class="clobie-grid clobie-grid--2">
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/writing/tags/' | relative_url }}">
    <p class="clobie-eyebrow">분류 기준</p>
    <h3>태그별 보기</h3>
    <p>태그 단위로 자주 반복되는 주제와 분위기를 모아볼 수 있습니다.</p>
  </a>
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/writing/series/' | relative_url }}">
    <p class="clobie-eyebrow">연작 기준</p>
    <h3>시리즈별 보기</h3>
    <p>같은 세계관과 연속된 컨셉을 시리즈 단위로 살펴봅니다.</p>
  </a>
</div>

## 최근 글

{% if all_writings.size > 0 %}
<div class="clobie-list">
  {% for post in all_writings limit: 12 %}
  {% assign type_label = site.data.clobie.writing_type_labels[post.clobie_type] | default: post.clobie_type | default: '미분류' %}
  {% assign genre_label = site.data.clobie.writing_genre_labels[post.genre] | default: post.genre %}
  <article class="clobie-card">
    <p class="clobie-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ type_label }}{% if post.genre %} · {{ genre_label }}{% endif %}</p>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.tags and post.tags.size > 0 %}
    <div class="clobie-tag-row">
      {% for tag in post.tags limit: 5 %}
      {% assign tag_label = site.data.clobie.writing_tag_labels[tag] | default: tag %}
      <span class="clobie-tag">{{ tag_label }}</span>
      {% endfor %}
    </div>
    {% endif %}
    {% if post.summary %}<p>{{ post.summary }}</p>{% elsif post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 140 }}</p>{% endif %}
  </article>
  {% endfor %}
</div>
{% else %}
<div class="clobie-empty">
  아직 등록된 글이 없습니다. 추후 디스코드 글 채널의 작업물을 설정 / 스토리 / 메모로 분류해 이곳에 연결할 예정입니다.
</div>
{% endif %}

## 추천 메타데이터

- `클로비 타입`: 설정 / 스토리 / 메모
- `장르`: 판타지 / SF / 미스터리 / 공포 / 일상 / 감성 / 드라마 등
- `시리즈`: 같은 세계관/연작 식별자
- `태그`: 탐색용 키워드
- `source_channel`, `source_message_id`: 디스코드 원본 추적용
- `source_path`: 원본 md 문서 경로 (중복 이관 방지용)
