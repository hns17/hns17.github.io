---
title: "Clobie - 메모"
permalink: /clobie/writing/notes/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
---

아이디어 조각, 컨셉 문장, 짧은 기록을 모아두는 영역입니다.

{% assign items = site.clobie_writing | where: "clobie_type", "notes" | sort: 'date' | reverse %}
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
<div class="clobie-empty">아직 등록된 메모 글이 없습니다.</div>
{% endif %}
