---
title: "빛에서 픽셀까지"
permalink: /category/graphics/series/light-to-pixel/
layout: archive
category_key: "Graphics/Series/Light-To-Pixel"
redirect_from:
  - /graphics/series/light-to-pixel/
archive_intro: "사물을 인식하는 과정에서 출발해 빛과 색, 셰이딩과 그림자, 렌더링 파이프라인과 현대 렌더링 방식까지 원인과 결과로 연결하는 장기 연재입니다."
---

{% assign series_posts = site.categories[page.category_key] | sort: "series_order" %}

<div class="archive__lead" role="note" aria-label="연재 소개">
  <p class="archive__lead-label">연재 소개</p>
  <p class="archive__lead-text">{{ page.archive_intro }}</p>
  <p class="archive__lead-meta">총 {{ series_posts | size }}개의 글 · 001부터 순서대로 읽기</p>
</div>

{% for post in series_posts %}
  {% include archive-single.html type=page.entries_layout %}
{% endfor %}
