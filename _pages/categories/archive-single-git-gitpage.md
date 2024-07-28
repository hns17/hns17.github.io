---
title: "Git/GitPage"
permalink: /category/git/gitpage/
layout: archive
---



{% assign title = page.title %}

{% assign posts = site.categories[title] %} 

{% for post in posts %}

  {% include archive-single.html type=page.entries_layout %}

{% endfor %}

