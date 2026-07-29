---
title: "Graphics/Series"
permalink: /category/graphics/series/
layout: archive
archive_intro: "그래픽스에 관한 여러 장기 연재를 모아 둔 페이지입니다. 각 연재는 독립된 제목과 읽기 순서를 가집니다."
---

<div class="archive__lead" role="note" aria-label="페이지 소개">
  <p class="archive__lead-label">이 페이지 소개</p>
  <p class="archive__lead-text">{{ page.archive_intro }}</p>
  <p class="archive__lead-meta">현재 {{ site.data.graphics_series | size }}개의 연재가 있습니다.</p>
</div>

{% for series_info in site.data.graphics_series %}
  {% assign series_posts = site.categories[series_info.category] | sort: "series_order" | reverse %}
  {% if series_posts.size > 0 %}
    <section class="archive__series">
      <h2><a href="{{ series_info.url | relative_url }}">{{ series_info.title }}</a></h2>
      <p>{{ series_info.description }}</p>
      <p>총 {{ series_posts | size }}개의 글 · 최신 글부터 표시 · 제목 번호는 읽기 순서</p>

      {% for post in series_posts %}
        {% include archive-single.html type=page.entries_layout %}
      {% endfor %}
    </section>
  {% endif %}
{% endfor %}
