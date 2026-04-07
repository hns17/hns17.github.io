---
title: "Clobie - 날짜별 아카이브"
permalink: /clobie/writing/archive/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
  summary_label: "날짜별 아카이브"
classes: wide
---

날짜별 아카이브는 클로비 글 작업실의 문서를 **작성일 기준으로 묶어** 보는 페이지입니다.

{% assign all_writings = site.clobie_writing | sort: 'date' | reverse %}
{% assign dates = all_writings | group_by_exp: 'item', 'item.date | date: "%Y-%m-%d"' %}

{% if dates.size > 0 %}
<div class="clobie-date-grid">
  {% for date_group in dates %}
  <a class="clobie-card clobie-card--link" href="#date-{{ date_group.name }}">
    <p class="clobie-eyebrow">{{ date_group.items | size }}개 문서</p>
    <h3>{{ date_group.name }}</h3>
  </a>
  {% endfor %}
</div>

{% for date_group in dates %}
## <span id="date-{{ date_group.name }}">{{ date_group.name }}</span>

<div class="clobie-list">
  {% for post in date_group.items %}
  {% assign type_label = site.data.clobie.writing_type_labels[post.clobie_type] | default: post.clobie_type | default: '미분류' %}
  {% assign genre_label = site.data.clobie.writing_genre_labels[post.genre] | default: post.genre %}
  <article class="clobie-card">
    <p class="clobie-meta">{{ type_label }}{% if post.genre %} · {{ genre_label }}{% endif %}</p>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.summary %}<p>{{ post.summary }}</p>{% elsif post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 140 }}</p>{% endif %}
  </article>
  {% endfor %}
</div>
{% endfor %}
{% else %}
<div class="clobie-empty">아직 날짜별로 정리된 글이 없습니다.</div>
{% endif %}
