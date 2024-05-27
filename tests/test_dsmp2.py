from collections import Counter
from pathlib import Path

import pytest

from src.dsmp2 import course_parser as cp

DSMP2_TEST_HTML_PATH = Path("tests/data/campusx.html")


@pytest.fixture
def course_topics() -> list[cp.CourseTopic]:
    return list(cp.CourseTopic.parse(cp.CourseTopic.search(DSMP2_TEST_HTML_PATH)))


def test_course_topic_parser(course_topics: list[cp.CourseTopic]):
    assert len(course_topics) == 5, "Not parsing all the topics from TEST_HTML."


@pytest.mark.parametrize(
    ["course_topic_index", "title", "id"],
    [
        (0, "Week 1 - Basics of Python Programming", "t7z3or0ssw"),
        (1, "Week 2 - Python Data Types", "m2p4l0896y"),
        (2, "Week 3 - Object Oriented Programming(OOP)", "7xpqy4bgny"),
        (3, "Week 4 - Advanced Python", "5f44kexem4"),
        (4, "Python Fundamentals Additional Content", "cdn7xaxd4jf"),
    ],
)
def test_course_topic_content(
    course_topics: list[cp.CourseTopic],
    course_topic_index: int,
    title: str,
    id: str,
):
    topic = course_topics[course_topic_index]
    assert topic.title == title
    assert topic.id == id


@pytest.mark.parametrize(
    [
        "course_topic_index",
        "sub_topic_count",
    ],
    [
        (0, 12),
        (1, 12),
        (2, 12),
        (3, 15),
        (4, 7),
    ],
)
def test_course_sub_topics_count(
    course_topics: list[cp.CourseTopic],
    course_topic_index: int,
    sub_topic_count: int,
):
    sub_topics = list(cp.CourseSubTopic.parse(course_topics[course_topic_index]))

    assert (
        len(sub_topics) == sub_topic_count
    ), f"Expecting {sub_topic_count} sub-topics in TEST_HTML."


@pytest.mark.parametrize(
    [
        "course_topic_index",
        "unique_types_count",
    ],
    [
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
    ],
)
def test_course_sub_topics_unique_types_count(
    course_topics: list[cp.CourseTopic],
    course_topic_index: int,
    unique_types_count: int,
):
    sub_topics = list(cp.CourseSubTopic.parse(course_topics[course_topic_index]))

    unique_types = {sub_topic.type for sub_topic in sub_topics}
    assert (
        len(unique_types) == unique_types_count
    ), f"Expecting {unique_types_count} unique resource types in the sub-topics"


@pytest.mark.parametrize(
    [
        "course_topic_index",
        "resource_type_counts",
    ],
    [
        (0, {cp.ResourceType.video: 9, cp.ResourceType.assignment: 3}),
        (1, {cp.ResourceType.video: 9, cp.ResourceType.assignment: 3}),
        (2, {cp.ResourceType.video: 9, cp.ResourceType.assignment: 3}),
        (3, {cp.ResourceType.video: 12, cp.ResourceType.assignment: 3}),
        (4, {cp.ResourceType.link: 6, cp.ResourceType.article: 1}),
    ],
)
def test_course_sub_topic_counts(
    course_topics: list[cp.CourseTopic],
    course_topic_index: int,
    resource_type_counts: dict[cp.ResourceType, int],
):
    sub_topics = list(cp.CourseSubTopic.parse(course_topics[course_topic_index]))

    sub_topics_counter = Counter(sub_topic.type for sub_topic in sub_topics)
    assert (
        sub_topics_counter == resource_type_counts
    ), f"Unexpected count of resource types: {sub_topics_counter}"


@pytest.mark.parametrize(
    [
        "course_topic_index",
        "sub_topic_index",
        "sub_topic_id",
        "sub_topic_type",
    ],
    [
        (1, 2, "637effeae4b02c7bb21ffaf4", cp.ResourceType.video),
        (3, 4, "6387fb32e4b0bd2df3b1d7b6", cp.ResourceType.assignment),
        (4, 1, "639fd31ee4b089d90ae5fdd5", cp.ResourceType.article),
        (4, 5, "639fd3c5e4b061a4bd099672", cp.ResourceType.link),
    ],
)
def test_course_sub_topics_content(
    course_topics: list[cp.CourseTopic],
    course_topic_index: int,
    sub_topic_index: int,
    sub_topic_id: str,
    sub_topic_type: cp.ResourceType,
):
    sub_topics = list(cp.CourseSubTopic.parse(course_topics[course_topic_index]))
    sub_topic = sub_topics[sub_topic_index]

    assert sub_topic.id == sub_topic_id
    assert sub_topic.type == sub_topic_type
