---
hide:
  - navigation
---

# DSMP by CampusX

<style>
article > h1 { display: none; }
</style>

<div class="grid" markdown>

[:material-sync:{ .lg .middle .bounce } Reverse Topic Order](#){ .md-button .md-button--primary style="text-align: center; display: block;" onclick="reverseContainers()" }

[:material-database:{ .lg .middle } View Downloaded Resources](https://github.com/arv-anshul/campusx/tree/main/resources/DSMP "Resources downloaded as files on GitHub"){ .md-button .md-button--primary style="text-align: center; display: block;" target="_blank" }

</div>

<article id="resourceContainer" markdown>
{% set printed_topic_ids = [] %}

{% for topic in dsmp2.courseTopics|reverse %}
    {% for sub_topic in dsmp2.cleanedResources %}
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
- [{{ netloc }}]({{ link }}){ target="_blank" title="{{ link }}" }
            {% endfor %}

    {% endif %}
{% endif %}

{% if sub_topic.type == "assignment" %}

<figure style="min-width: 35%" markdown>
<div class="grid cards" markdown>

- ### [:memo:](https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a/take#{{ sub_topic.id }}){ .middle target="_blank" title="Go to Website" } {{ sub_topic.title }}

    [Assignment Link]({{ sub_topic.assignmentLink }}){ target="_blank" .md-button }

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
