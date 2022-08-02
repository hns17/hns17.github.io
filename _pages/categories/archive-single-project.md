---
title: "Project"
permalink: /archive-single-project/
layout: archive
author_profile: true
sidebar:
 nav: "docs"
---



{% assign title = "Project" %}

{% assign posts = site.categories[title ] %} 

{% for post in posts %} {% include archive-single.html type=page.entries_layout %}

{% endfor %}

