---
author_profile: true
layout : single
title : IndexPage
---



<section>

{% assign filter_category = "Daily" %}

{% if filter_category == "" %}

​	{{ site.posts[0].content }}

{% else %}

​	{% for post in site.posts %}

​		{% assign categories = post.categories | split: "/" %}

​		{% assign str_cnt = categories[0] | size %}

​		{% assign head_category = categories[0] | slice: 2, str_cnt %}

​			{% if head_category == filter_category %}

​				{% assign content = post.content %}

​				{{ content }}

​			{% break %}

​		{% endif %}

​	{% endfor %}

{% endif %}

