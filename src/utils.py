"""
🗂️ Sort the stored Course's data so that it can be present neatly.
It only works when you have the website's HTML.
"""
import json
import re
from dataclasses import asdict
from urllib.parse import urlparse

from src import course_parser as cp


def export_course_topics() -> None:
    """Parse all Course Topics and dump them as JSON."""
    course_topic_tag = cp.CourseTopic.search(cp.COURSE_HTML_PATH)
    topics = cp.CourseTopic.parse(course_topic_tag)
    with cp.COURSE_TOPICS_PATH.open("w") as f:
        json.dump([{"id": i.id, "title": i.title} for i in topics], f, indent=2)


def export_course_sub_topics() -> None:
    """Parse all Course Sub-Topics and dump them as JSON."""
    course_topic_tag = cp.CourseTopic.search(cp.COURSE_HTML_PATH)
    topics = cp.CourseTopic.parse(course_topic_tag)
    sub_topics = [asdict(j) for i in topics for j in cp.CourseSubTopic.parse(i)]
    with cp.COURSE_SUB_TOPICS_PATH.open("w") as f:
        json.dump(sub_topics, f, indent=2)


def sort_sub_topics_resources():
    """
    Sorts the existing `data/subTopicResources.json` file according to
    `data/courseSubTopics.json`.
    """
    sub_topics = json.loads(cp.COURSE_SUB_TOPICS_PATH.read_bytes())
    resources = json.loads(cp.SUB_TOPIC_RESOURCES_PATH.read_bytes())

    id_to_position = {item["id"]: index for index, item in enumerate(sub_topics)}
    sorted_data_file2 = sorted(
        resources,
        key=lambda item: id_to_position.get(item.get("id"), float("inf")),
    )

    with cp.SUB_TOPIC_RESOURCES_PATH.open("w") as file2:
        json.dump(sorted_data_file2, file2, indent=2)


def clean_videos_resources() -> None:
    resources: list[dict] = json.loads(cp.SUB_TOPIC_RESOURCES_PATH.read_bytes())

    def parse_description(description: str) -> dict[str, str]:
        __s = re.sub(r"[\"<]", " ", description)
        links = re.findall(r"https?://\S+", __s)
        return {link: urlparse(link).netloc for link in links}

    cleaned_resources = []
    for resource in resources:
        if resource["type"] != "video":
            continue
        resource["links"] = parse_description(resource["description"])
        cleaned_resources.append(resource)

    with cp.CLEANED_RESOURCES_PATH.open("w") as f:
        json.dump(cleaned_resources, f, indent=2)


if __name__ == "__main__":
    if not cp.COURSE_HTML_PATH.exists():
        raise RuntimeError("You must have the Course's website HTML.")
    export_course_topics()
    export_course_sub_topics()
    sort_sub_topics_resources()
    clean_videos_resources()
