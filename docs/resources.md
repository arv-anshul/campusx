---
hide:
    - navigation
---

# CampusX - DSMP Resources

<figure style="min-width: 35%" markdown>
!!! example "Reference"

    :material-book-open-page-variant:{ .lg .warning } :material-equal: **Main Topic** of the Course.

    :material-book:{ .lg .primary } :material-equal: **Sub Topic** of the Main Topic.
</figure>

{% set printed_topic_ids = [] %}

{% for topic in courseTopics %}
    {% for sub_topic in cleanedResources %}
        {% if topic.id == sub_topic.topicId %}
            {% if sub_topic.description %}
            {% if topic.id not in printed_topic_ids %}
                {% set _ = printed_topic_ids.append(topic.id) %}

## :material-book-open-page-variant:{ title="Main Topic" .warning } {{ topic.title }}
            {% endif %}

### :material-book:{ title="Sub Topic" .primary } {{ sub_topic.title }}

<details style="border-color: #448aff33;">
    <summary>Description</summary>
    <div style="font-family: monospace;">
    {{ sub_topic.description }}
    </div>
</details>

            {% for netloc, link in sub_topic.links.items() %}
- [{{ netloc }}]({{ link }})
            {% endfor %}

            {% endif %}
        {% endif %}
    {% endfor %}
{% endfor %}
