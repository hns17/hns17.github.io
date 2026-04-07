---
title: "Clobie - 설정"
permalink: /clobie/writing/settings/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
---

세계관, 시스템, 조직, 캐릭터 프로필 같은 구조적 자료를 모아두는 영역입니다.

{% assign items = site.clobie_writing | where: "clobie_type", "settings" | sort: 'date' | reverse %}
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
<div class="clobie-empty">아직 등록된 설정 글이 없습니다.</div>
{% endif %}
