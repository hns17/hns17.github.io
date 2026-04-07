---
title: "Clobie - 시리즈별 보기"
permalink: /clobie/writing/series/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
classes: wide
---

시리즈별 보기는 같은 세계관과 연작 단위를 기준으로 글을 모아보는 페이지입니다.

{% assign series_pool = site.clobie_writing | map: 'series' | uniq | sort %}

{% if series_pool.size > 0 %}
<div class="clobie-tag-cloud">
  {% for series in series_pool %}
    {% unless series == nil or series == '' %}
    {% assign series_count = 0 %}
    {% for post in site.clobie_writing %}
      {% if post.series == series %}
        {% assign series_count = series_count | plus: 1 %}
      {% endif %}
    {% endfor %}
    <a class="clobie-card clobie-card--link" href="#series-{{ series | slugify }}">
      <p class="clobie-eyebrow">{{ series_count }}개 문서</p>
      <h3>{{ series }}</h3>
    </a>
    {% endunless %}
  {% endfor %}
</div>

{% for series in series_pool %}
  {% unless series == nil or series == '' %}
  <h2 id="series-{{ series | slugify }}">{{ series }}</h2>
  <div class="clobie-list">
    {% for post in site.clobie_writing %}
      {% if post.series == series %}
      {% assign type_label = site.data.clobie.writing_type_labels[post.clobie_type] | default: post.clobie_type %}
      {% assign genre_label = site.data.clobie.writing_genre_labels[post.genre] | default: post.genre %}
      <article class="clobie-card">
        <p class="clobie-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ type_label }}{% if post.genre %} · {{ genre_label }}{% endif %}</p>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        {% if post.summary %}<p>{{ post.summary }}</p>{% elsif post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 140 }}</p>{% endif %}
      </article>
      {% endif %}
    {% endfor %}
  </div>
  {% endunless %}
{% endfor %}
{% else %}
<div class="clobie-empty">아직 정리된 시리즈가 없습니다.</div>
{% endif %}
