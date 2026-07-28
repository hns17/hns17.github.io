---
author_profile: true
layout: single
title: 근황
sidebar:
  nav: "_posts"
---

<section>
  {% for post in site.posts %}
    {% if post.categories contains "Projects/WorkLog" or post.categories contains "Daily/Life" %}
      {{ post.content }}
      {% break %}
    {% endif %}
  {% endfor %}
</section>
