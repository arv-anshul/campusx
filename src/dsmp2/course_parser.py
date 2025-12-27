from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from enum import StrEnum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Self

from bs4 import BeautifulSoup, Tag

from . import constant as C

if TYPE_CHECKING:
    import httpx


class ResourceType(StrEnum):
    article = auto()
    assessment = auto()
    assignment = auto()
    link = auto()
    livetest = auto()
    pdf = auto()
    video = auto()


def fetch_sub_topic_resource(
    client: httpx.Client,
    sub_topic_id: str,
    resource_type: ResourceType,
) -> bytes:
    """Fetches the resource data for the given subtopic ID and resource type.

    Args:
        client: HTTPX client instance with cookies set.
        sub_topic_id: ID of the subtopic to fetch.
        resource_type: Type of resource to fetch.

    Returns:
        The data as bytes for the requested resource.

    Raises:
        ValueError: If client does not have cookies set.
        HTTPError: If the API request fails.
    """
    if not client.cookies:
        raise ValueError("Client does not have cookies.")
    res = client.get(f"/{resource_type.name}s/{sub_topic_id}/get")
    res.raise_for_status()
    return res.content


def get_cookies():
    """Construct cookies from ENVs."""
    c_ujwt = os.getenv("C_UJWT")
    session_id = os.getenv("SESSION_ID")

    error_msg = "Define '%s' as environment variable."
    if c_ujwt is None:
        raise ValueError(error_msg % "C_UJWT")
    if session_id is None:
        raise ValueError(error_msg % "SESSION_ID")

    return {
        "c_ujwt": c_ujwt,
        "SESSIONID": session_id,
    }


@dataclass(kw_only=True)
class CourseTopic:
    title: str
    id: str
    source: Tag = field(repr=False)

    @staticmethod
    def search(html_path: Path) -> Tag:
        """
        Parses CourseTopic instances from a BeautifulSoup tag.

        Yields CourseTopic instances parsed from the provided BeautifulSoup tag source.
        """
        soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
        course_items_tag = soup.select_one("div.courseItems")
        if course_items_tag:
            return course_items_tag
        raise ValueError("'div.courseItems' css selector not present in source.")

    @classmethod
    def parse(cls, source: Tag) -> Iterable[Self]:
        """
        Parses CourseTopic instances from a BeautifulSoup tag.

        Yields CourseTopic instances parsed from the provided BeautifulSoup tag source.
        """
        yield from (
            cls(
                title=str(tag["data-title"]),
                id=str(tag["data-id"]),
                source=tag,
            )
            for tag in source.find_all("div", {"data-type": "label"})
        )


@dataclass(kw_only=True)
class CourseSubTopic:
    id: str
    topicId: str
    title: str
    type: ResourceType

    def __eq__(self, __value: Any) -> bool:
        if not isinstance(__value, CourseSubTopic):
            return False
        return self.id == __value.id

    @classmethod
    def parse(cls, topic: CourseTopic) -> Iterable[Self]:
        """
        Parses CourseSubTopic instances from a CourseTopic BeautifulSoup tag.

        Yields CourseSubTopic instances parsed from the provided CourseTopic
        BeautifulSoup tag source.
        """
        yield from (
            cls(
                id=str(tag["data-id"]),
                topicId=topic.id,
                title=str(tag["data-title"]),
                type=tag["data-type"],
            )
            for tag in topic.source.find_all("div", {"data-type": True})
        )

    @classmethod
    def parse_many(
        cls,
        topics: Iterable[CourseTopic],
    ) -> Iterable[tuple[CourseTopic, Iterable[Self]]]:
        for topic in topics:
            yield topic, cls.parse(topic)

    @classmethod
    def find(
        cls,
        course_topics: Iterable[CourseTopic],
        *,
        id: str | None = None,
        title: str | None = None,
    ) -> Iterable[Self]:
        """
        Parses a single CourseSubTopic from the given CourseTopics.

        This allows fetching a specific CourseSubTopic by title or id from the
        list of CourseTopics, by searching through their associated subtopics.

        Args:
            course_topics: Iterable of CourseTopic instances to search through.
            title: Optional title of subtopic to find.
            id: Optional id of subtopic to find.

        Returns:
            Iterable of matching CourseSubTopic instances.

        Raises:
            ValueError: If both title and id are None.
            ValueError: If no matching subtopic is found.
        """
        if id is None and title is None:
            raise ValueError("Both 'id' and 'title' must not be None.")

        for topic in course_topics:
            if topic.id == id or topic.title == title:
                yield from cls.parse(topic)
                break
        else:
            raise ValueError(f"No subtopic found matching id={id} or title={title}")

    @classmethod
    def from_json(cls, path: str | Path) -> Iterable[Self]:
        json_as_dict = json.loads(Path(path).read_bytes())
        yield from (cls(**i) for i in json_as_dict)


@dataclass(kw_only=True)
class CourseVideoResource(CourseSubTopic):
    totalTime: str
    description: str = field(repr=False)
    isDescriptionHtml: bool = field(repr=False)

    @classmethod
    def fetch(cls, client: httpx.Client, sub_topic: CourseSubTopic) -> Self:
        if sub_topic.type != "video":
            raise ValueError(f"sub_topic is not a video resource, got {sub_topic.type}")

        response = fetch_sub_topic_resource(
            client=client,
            sub_topic_id=sub_topic.id,
            resource_type=ResourceType.video,
        )
        try:
            data = json.loads(response)
            data = data["spayee:resource"]
        except json.JSONDecodeError as e:
            raise ValueError("Response could not be parsed as JSON.") from e
        except KeyError as e:
            raise ValueError("Bad response or missing required fields.") from e
        try:
            return cls(
                **asdict(sub_topic),
                description=data["spayee:description"],
                totalTime=data["spayee:totalTime"],
                isDescriptionHtml=data["spayee:isDescriptionHtml"],
            )
        except KeyError as e:
            print(f"❌ KeyError: {e}")
            return cls.null(sub_topic)

    @classmethod
    def null(cls, sub_topic: CourseSubTopic) -> Self:
        return cls(
            **asdict(sub_topic),
            description="",
            totalTime="0",
            isDescriptionHtml=False,
        )


@dataclass(kw_only=True)
class CourseAssignmentResource(CourseSubTopic):
    assignmentLink: str = field(repr=False)

    @classmethod
    def fetch(cls, client: httpx.Client, sub_topic: CourseSubTopic) -> Self:
        if sub_topic.type != "assignment":
            raise ValueError(
                f"sub_topic is not an assignment resource, got {sub_topic.type}"
            )

        response = fetch_sub_topic_resource(
            client=client,
            sub_topic_id=sub_topic.id,
            resource_type=ResourceType.assignment,
        )

        def parse_assignment_link(source: str | bytes) -> str:
            soup = BeautifulSoup(source, "html.parser")
            link_tag = soup.select_one("#instructions a")
            if link_tag:
                return link_tag.get_attribute_list("href", "")[0]
            raise ValueError("assignmentLink tag not found in source")

        return cls(
            **asdict(sub_topic),
            assignmentLink=parse_assignment_link(response),
        )


_RESOURCE_TYPE_MAPPING: dict[ResourceType, type] = {
    ResourceType.video: CourseVideoResource,
    ResourceType.assignment: CourseAssignmentResource,
}


def load_resources() -> list[CourseSubTopic]:
    inferred_resources = []
    resources = json.loads(C.SUB_TOPIC_RESOURCES_PATH.read_bytes())
    for i in resources:
        _class = _RESOURCE_TYPE_MAPPING.get(getattr(ResourceType, i["type"]))
        if _class:
            inferred_resources.append(_class(**i))
    return inferred_resources


def filter_resources(
    sub_topics: Iterable[CourseSubTopic],
    resources: Iterable[CourseSubTopic],
) -> list[CourseSubTopic]:
    return [sub_topic for sub_topic in sub_topics if sub_topic not in resources]


def dump_resources(resources: Iterable[CourseSubTopic]) -> None:
    _resources: list[dict] = [asdict(i) for i in resources]
    if C.SUB_TOPIC_RESOURCES_PATH.exists():
        _resources = json.loads(C.SUB_TOPIC_RESOURCES_PATH.read_bytes()) + _resources
        _resources = [dict(i) for i in {frozenset(r.items()) for r in _resources}]
    with C.SUB_TOPIC_RESOURCES_PATH.open("w") as f:
        json.dump(_resources, f, indent=2)
