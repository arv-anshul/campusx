---
hide:
    - navigation
---

# CampusX - DSMP Resources

<figure style="min-width: 35%" markdown>
???+ example "Reference"

    :material-book-open-page-variant:{ .lg .warning } :material-equal: **Main Topic** of the Course.

    :material-book:{ .lg .primary } :material-equal: **Sub Topic** of the Main Topic.

    :memo:{ .lg } :material-equal: Sub Topic is **Assignment**.

    :material-video:{ .lg .secondary } :material-equal: Sub Topic is **Video**.
</figure>

{% set printed_topic_ids = [] %}

{% for topic in courseTopics %}
    {% for sub_topic in cleanedResources %}
        {% if topic.id == sub_topic.topicId %}

<!-- Video Resources -->
{% if sub_topic.type == "video" %}
    {% if sub_topic.description %}
        {% if topic.id not in printed_topic_ids %}
            {% set _ = printed_topic_ids.append(topic.id) %}

## :material-book-open-page-variant:{ title="Main Topic" .warning } {{ topic.title }}
        {% endif %}

### :material-{{ sub_topic.type }}:{ title="Sub Topic: {{ sub_topic.type | title }}" .secondary } {{ sub_topic.title }}

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

<!-- Assignment Resources -->
{% if sub_topic.type == "assignment" %}

<figure style="min-width: 35%" markdown>
<div class="grid cards" markdown>

- ### :memo:{ title="Sub Topic: {{ sub_topic.type | title }}" .info } {{ sub_topic.title }}

    [Assignment Link]({{ sub_topic.assignmentLink }}){ .md-button }

</div>
</figure>

{% endif %}

        {% endif %}
    {% endfor %}
{% endfor %}
