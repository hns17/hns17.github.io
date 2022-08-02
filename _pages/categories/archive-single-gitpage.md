---
title: "GitPage"
permalink: /archive-single-gitpage/
layout: archive
author_profile: true
sidebar:
 nav: "docs"
---



{% assign title = "GitPage" %}

{% assign posts = site.categories[title ] %} 

{% for post in posts %} {% include archive-single.html type=page.entries_layout %}

{% endfor %}

