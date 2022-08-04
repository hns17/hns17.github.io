---
title: IndexPage를 Custom 하기
categories: IT/GitPage
tags: ["GitPage"]
---





# 목적

- 사용중인 GitPage의 Main화면을 Custom한다.

- 가장 최근에 작성한 포스트를 표시

- 원하는 카테고리의 포스트만 표시




# 작성

```ruby
<section>
    //가져오려는 Post의 필터
    {% assign filter_category = "Daily" %}
	//필터가 비어있는 경우 전체 포스트 중 가장 마지막에 작성된 포스트 출력
	{% if filter_category == "" %}
		{{ site.posts[0].content }}
	{% else %}
		//Loop Post
		{% for post in site.posts %}
        	//Post의 카테고리 중 첫번째 값을 가져온다.
			{% assign categories = post.categories | split: "/" %}
			{% assign str_cnt = categories[0] | size %}
			{% assign head_category = categories[0] | slice: 2, str_cnt %}

			//해당 포스트 정보를 출력
			{% if head_category == filter_category %}
				{{ post.content }}
				{% break %}
			{% endif %}
		{% endfor %}
	{% endif %}
```



# Ref

- https://github.com/hns17/hns17.github.io/blob/main/index.md