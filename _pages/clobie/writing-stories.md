---
title: "Clobie - 스토리"
permalink: /clobie/writing/stories/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
classes: wide
---

짧은 이야기, 장면 스케치, 에피소드 중심의 글을 모아두는 영역입니다.

{% assign items = site.clobie_writing | where: 'clobie_type', 'stories' | sort: 'date' | reverse %}

<div class="clobie-grid clobie-grid--3">
  <div class="clobie-card">
    <p class="clobie-eyebrow">스토리 문서</p>
    <h3>{{ items | size }}개</h3>
    <p>클로비 작업실에 정리된 스토리 문서 수입니다.</p>
  </div>
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/writing/archive/' | relative_url }}">
    <p class="clobie-eyebrow">시간 흐름</p>
    <h3>날짜별 아카이브</h3>
    <p>언제 어떤 분위기의 이야기가 쓰였는지 흐름으로 볼 수 있습니다.</p>
  </a>
  <a class="clobie-card clobie-card--link" href="{{ '/clobie/writing/tags/' | relative_url }}">
    <p class="clobie-eyebrow">주제 보기</p>
    <h3>태그 허브</h3>
    <p>미스터리, 어반 판타지, 드라마 같은 주제축으로 모아볼 수 있습니다.</p>
  </a>
</div>

{% if items.size > 0 %}
<div class="clobie-list">
  {% for post in items %}
  {% assign genre_label = site.data.clobie.writing_genre_labels[post.genre] | default: post.genre %}
  <article class="clobie-card">
    <p class="clobie-meta">{{ post.date | date: "%Y-%m-%d" }}{% if post.genre %} · {{ genre_label }}{% endif %}</p>
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
<div class="clobie-empty">아직 등록된 스토리 글이 없습니다.</div>
{% endif %}
