---
title: "Clobie - 캐릭터"
permalink: /clobie/art/characters/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
classes: wide
---

캐릭터 중심의 그림을 모아보는 영역입니다.

{% assign all_art = site.clobie_art | sort: 'date' | reverse %}
{% assign character_items = site.clobie_art | where: 'clobie_type', 'character' %}
{% assign creature_items = site.clobie_art | where: 'clobie_type', 'creature' %}
{% assign scene_items = site.clobie_art | where: 'clobie_type', 'scene' %}
{% assign sf_items = site.clobie_art | where: 'clobie_type', 'sf' %}
{% assign items = character_items | sort: 'date' | reverse %}

<div class="clobie-type-nav clobie-section-gap">
  <a class="clobie-type-pill" href="{{ '/clobie/art/' | relative_url }}">
    <strong>전체</strong>
    <span>{{ all_art | size }}</span>
  </a>
  <a class="clobie-type-pill" href="{{ '/clobie/art/characters/' | relative_url }}">
    <strong>캐릭터</strong>
    <span>{{ character_items | size }}</span>
  </a>
  <a class="clobie-type-pill" href="{{ '/clobie/art/creatures/' | relative_url }}">
    <strong>생물</strong>
    <span>{{ creature_items | size }}</span>
  </a>
  <a class="clobie-type-pill" href="{{ '/clobie/art/scenes/' | relative_url }}">
    <strong>장면</strong>
    <span>{{ scene_items | size }}</span>
  </a>
  <a class="clobie-type-pill" href="{{ '/clobie/art/sf/' | relative_url }}">
    <strong>SF</strong>
    <span>{{ sf_items | size }}</span>
  </a>
</div>

{% if items.size > 0 %}
<div class="clobie-gallery clobie-list" data-page-size="24">
  {% for item in items %}
  <a class="clobie-gallery__item" href="{{ item.url | relative_url }}">
    {% if item.image_url %}<img src="{{ item.image_url }}" alt="{{ item.title }}">{% else %}<div class="clobie-gallery__placeholder">No Image</div>{% endif %}
    <div class="clobie-gallery__caption"><strong>{{ item.title }}</strong><span>{% if item.mood %}{{ item.mood }}{% endif %}</span></div>
  </a>
  {% endfor %}
</div>
{% else %}
<div class="clobie-empty">아직 등록된 캐릭터 작업이 없습니다.</div>
{% endif %}
