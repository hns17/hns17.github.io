---
title: "GitPage"
permalink: /archive-single-gitpage/
layout: archive
---



{% assign title = "GitPage" %}

{% assign posts = site.categories[title ] %} 

{% for post in posts %} {% include archive-single.html type=page.entries_layout %}

{% endfor %}

