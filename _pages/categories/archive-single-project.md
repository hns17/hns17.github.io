---
title: "Project"
permalink: /archive-single-project/
layout: archive
---



{% assign title = "Project" %}

{% assign posts = site.categories[title ] %} 

{% for post in posts %} {% include archive-single.html type=page.entries_layout %}

{% endfor %}

