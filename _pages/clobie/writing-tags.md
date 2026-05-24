---
title: "Clobie - 태그별 보기"
permalink: /clobie/writing/tags/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
classes: wide
---

태그별 보기는 자주 반복되는 주제와 분위기를 기준으로 글을 모아보는 페이지입니다.

{% assign tag_pool = '' | split: '' %}
{% assign writings = site.clobie_writing | where_exp: 'item', 'item.clobie_type != "notes"' | sort: 'date' | reverse %}
{% for post in writings %}
  {% if post.tags %}
    {% assign tag_pool = tag_pool | concat: post.tags %}
  {% endif %}
{% endfor %}
{% assign uniq_tags = tag_pool | uniq | sort %}

{% if uniq_tags.size > 0 %}
<div class="clobie-tag-cloud">
  {% for tag in uniq_tags %}
    {% assign tag_label = site.data.clobie.writing_tag_labels[tag] | default: tag %}
    {% assign tag_count = 0 %}
    {% for post in writings %}
      {% if post.tags contains tag %}
        {% assign tag_count = tag_count | plus: 1 %}
      {% endif %}
    {% endfor %}
    <a class="clobie-card clobie-card--link" href="#tag-{{ tag | slugify }}">
      <p class="clobie-eyebrow">{{ tag_count }}개 문서</p>
      <h3>{{ tag_label }}</h3>
    </a>
  {% endfor %}
</div>

{% for tag in uniq_tags %}
  {% assign tag_label = site.data.clobie.writing_tag_labels[tag] | default: tag %}
  <h2 id="tag-{{ tag | slugify }}">{{ tag_label }}</h2>
  <div class="clobie-list" data-page-size="5">
    {% for post in writings %}
      {% if post.tags contains tag %}
      {% assign type_label = site.data.clobie.writing_type_labels[post.clobie_type] | default: post.clobie_type %}
      <article class="clobie-card">
        <p class="clobie-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ type_label }}</p>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        {% if post.summary %}<p>{{ post.summary }}</p>{% elsif post.excerpt %}<p>{{ post.excerpt | strip_html | truncate: 140 }}</p>{% endif %}
      </article>
      {% endif %}
    {% endfor %}
  </div>
{% endfor %}
{% else %}
<div class="clobie-empty">아직 정리된 태그가 없습니다.</div>
{% endif %}
