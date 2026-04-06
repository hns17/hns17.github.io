---
title: "Clobie - 캐릭터"
permalink: /clobie/art/characters/
layout: single
sidebar:
  title: "Clobie"
  nav: "_clobie"
---

캐릭터 중심의 그림을 모아보는 영역입니다.

{% assign items = site.clobie_art | where: "clobie_type", "characters" | sort: 'date' | reverse %}
{% if items.size > 0 %}
<div class="clobie-gallery">
  {% for item in items %}
  <a class="clobie-gallery__item" href="{{ item.url | relative_url }}">
    {% if item.image %}<img src="{{ item.image | relative_url }}" alt="{{ item.title }}">{% else %}<div class="clobie-gallery__placeholder">No Image</div>{% endif %}
    <div class="clobie-gallery__caption"><strong>{{ item.title }}</strong></div>
  </a>
  {% endfor %}
</div>
{% else %}
<div class="clobie-empty">아직 등록된 캐릭터 작업이 없습니다.</div>
{% endif %}
