---
title: "Git/Git"
permalink: /category/git/git/
layout: archive
---



{% assign title = page.title %}

{% assign posts = site.categories[title] %} 

{% for post in posts %}

  {% include archive-single.html type=page.entries_layout %}

{% endfor %}

