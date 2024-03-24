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

<p align="center" style="margin: 0;" markdown>
[:material-sync:{ .lg .middle } Reverse Elements](#){ .md-button style="border-radius: 2rem;" onclick="reverseContainers()" }
</p>

<article id="resourceContainer" markdown>
{% set printed_topic_ids = [] %}

{% for topic in courseTopics|reverse %}
    {% for sub_topic in cleanedResources %}
        {% if topic.id == sub_topic.topicId %}

{% if sub_topic.type == "video" %}
    {% if sub_topic.description %}
        {% if topic.id not in printed_topic_ids %}
            {% set _ = printed_topic_ids.append(topic.id) %}
<section class="hi" markdown>

## [:bookmark:](https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a/take#{{ topic.id }}){ .middle target="_blank" title="Go to Website" } **{{ topic.title }}**
        {% endif %}

### [:camera:](https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a/take#{{ sub_topic.id }}){ .middle target="_blank" title="Go to Website" } {{ sub_topic.title }}

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

- ### [:memo:](https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a/take#{{ sub_topic.id }}){ .middle target="_blank" title="Go to Website" } {{ sub_topic.title }}

    [Assignment Link]({{ sub_topic.assignmentLink }}){ .md-button }

</div>
</figure>

{% endif %}

        {% endif %}
    {% endfor %}
</section>
{% endfor %}
</article>

<script>
    function reverseContainers() {
        var container1 = document.getElementById('resourceContainer');
        var container2 = document.querySelector(
            'div.md-sidebar.md-sidebar--secondary > div > div > nav > ul'
        );
        reverseChildren(container1);
        reverseChildren(container2);
    }

    function reverseChildren(container) {
        var children = Array.from(container.children);
        children.reverse();
        container.innerHTML = '';
        children.forEach(function(child) {
            container.appendChild(child);
        });
    }
</script>
