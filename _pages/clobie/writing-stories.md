---
title: "Clobie - 스토리"
permalink: /clobie/writing/stories/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
---

짧은 이야기, 장면 스케치, 에피소드 중심의 글을 모아두는 영역입니다.

{% assign items = site.clobie_writing | where: "clobie_type", "stories" | sort: 'date' | reverse %}
{% if items.size > 0 %}
<div class="clobie-list">
  {% for post in items %}
  {% assign genre_label = site.data.clobie.writing_genre_labels[post.genre] | default: post.genre %}
  <article class="clobie-card">
    <p class="clobie-meta">{{ post.date | date: "%Y-%m-%d" }}{% if post.genre %} · {{ genre_label }}{% endif %}</p>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.summary %}<p>{{ post.summary }}</p>{% endif %}
  </article>
  {% endfor %}
</div>
{% else %}
<div class="clobie-empty">아직 등록된 스토리 글이 없습니다.</div>
{% endif %}
