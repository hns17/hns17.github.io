---
title: "News"
permalink: /archive-single-news/
layout: archive
---



{% assign title = "News" %}

{% assign posts = site.categories[title ] %} 

{% for post in posts %} {% include archive-single.html type=page.entries_layout %}

{% endfor %}

