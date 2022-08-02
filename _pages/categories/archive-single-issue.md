---
title: "Issue"
permalink: /archive-single-issue/
layout: archive
author_profile: true
sidebar:
 nav: "docs"
---



{% assign title = "Issue" %}

{% assign posts = site.categories[title ] %} 

{% for post in posts %} {% include archive-single.html type=page.entries_layout %}

{% endfor %}

