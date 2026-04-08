---
title: "Clobie - 생물"
permalink: /clobie/art/creatures/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
classes: wide
---

동물, 수호수, 몬스터 같은 비인간 존재를 모아보는 영역입니다.

{% assign items = site.clobie_art | where: 'clobie_type', 'creature' | sort: 'date' | reverse %}
{% if items.size > 0 %}
<div class="clobie-gallery clobie-list" data-page-size="12">
  {% for item in items %}
  <a class="clobie-gallery__item" href="{{ item.url | relative_url }}">
    {% if item.image_url %}<img src="{{ item.image_url }}" alt="{{ item.title }}">{% else %}<div class="clobie-gallery__placeholder">No Image</div>{% endif %}
    <div class="clobie-gallery__caption"><strong>{{ item.title }}</strong><span>{% if item.mood %}{{ item.mood }}{% endif %}</span></div>
  </a>
  {% endfor %}
</div>
{% else %}
<div class="clobie-empty">아직 등록된 생물 작업이 없습니다.</div>
{% endif %}
