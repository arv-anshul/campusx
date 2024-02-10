---
hide:
    - navigation
---

# CampusX - DSMP Resources

<style>
#campusx-dsmp-resources {
    display: none;
}
</style>

<figure style="min-width: 40%" markdown>
??? example "Reference"
    | Icon                | Description                   |
    | :-----------------: | :---------------------------- |
    | :bookmark:{ .lg } | **Main Topic** of the Course. |
    |   :memo:{ .lg }   | Sub Topic is **Assignment**.  |
    |  :camera:{ .lg }  | Sub Topic is **Video**.       |
</figure>

{% set printed_topic_ids = [] %}

{% for topic in courseTopics %}
    {% for sub_topic in cleanedResources %}
        {% if topic.id == sub_topic.topicId %}

{% if sub_topic.type == "video" %}
    {% if sub_topic.description %}
        {% if topic.id not in printed_topic_ids %}
            {% set _ = printed_topic_ids.append(topic.id) %}

## :bookmark:{ title="Main Topic" } **{{ topic.title }}**
        {% endif %}

### :camera:{ title="Sub Topic: Video" } {{ sub_topic.title }}

<details style="border-color: #448aff33;">
    <summary>Description</summary>
    <div style="font-family: monospace;">
    {{ sub_topic.description }}
    </div>
</details>

            {% for link, netloc in sub_topic.links.items() %}
- [{{ netloc }}]({{ link }}){ title="{{ link }}" }
            {% endfor %}

    {% endif %}
{% endif %}

{% if sub_topic.type == "assignment" %}

<figure style="min-width: 35%" markdown>
<div class="grid cards" markdown>

- ### :memo:{ title="Sub Topic: Assignment" } {{ sub_topic.title }}

    [Assignment Link]({{ sub_topic.assignmentLink }}){ .md-button }

</div>
</figure>

{% endif %}

        {% endif %}
    {% endfor %}
{% endfor %}
