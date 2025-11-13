"""
Download course's resources like `.pdf`, `.ipynb`, `.docx`, `.pptx`, `.xlsx` and `.py` files.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from string import punctuation
from typing import Any

import httpx

from src import _io
from src.downloader import infer_downloader

from . import constant as C
from .course_parser import ResourceType

ResourceDict = dict[str, dict[str, list[tuple[str, bytes]]]]


def _infer_path_from_title(title: str) -> Path:
    _punc = re.sub(r"[-_]", "", str(punctuation))
    title = re.sub(rf"[{_punc}]", "", title)
    title = re.sub(r"\s+", " ", title)
    return Path(title)


def _dl_video_resource(
    resource: dict[str, Any], client: httpx.Client
) -> list[tuple[str, bytes]]:
    resources = []
    for url in resource["links"]:
        try:
            dl = infer_downloader(url)
        except TypeError:
            continue
        resources.append(dl.download(client))
    return resources


def _dl_assignment_resource(
    resource: dict[str, Any], client: httpx.Client
) -> tuple[str, bytes]:
    dl = infer_downloader(resource["assignmentLink"])
    return dl.download(client)


def download_resources(
    resource: dict[str, Any], client: httpx.Client
) -> ResourceDict | None:
    if resource["type"] == ResourceType.video and resource.get("links"):
        temp = _dl_video_resource(resource, client)
    elif resource["type"] == ResourceType.assignment and resource.get("assignmentLink"):
        temp = [_dl_assignment_resource(resource, client)]
    else:
        return None
    if temp:
        return {resource["topicId"]: {resource["title"]: temp}}


def topic_title_from_topic_id(topic_id: str) -> str:
    data = json.loads(_io.open_file(C.COURSE_TOPICS_PATH))
    for topic in data:
        if topic["id"] == topic_id:
            return topic["title"]
    else:
        raise ValueError(f"{topic_id = } not found")


def _infer_existed_file_path(fp: Path, /) -> Path:
    """Checks whether the file path exists if yes then append `"_1"` and returns."""
    return fp.with_name(fp.name + "_1") if fp.exists() else fp


def store_resources(dl_resources: ResourceDict) -> None:
    for topic_id, resource in dl_resources.items():
        topic_dir = C.DSMP_RESOURCES_PATH / _infer_path_from_title(
            topic_title_from_topic_id(topic_id)
        )
        for parent_title, contents in resource.items():
            parent_dir = topic_dir / _infer_path_from_title(parent_title)
            parent_dir.mkdir(exist_ok=True, parents=True)
            for filename, content in contents:
                print("Storing at:", parent_dir / filename)
                _infer_existed_file_path(parent_dir / filename).write_bytes(content)


def filter_stored_resources(
    resources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    stored_resources = {p.name for p in C.DSMP_RESOURCES_PATH.rglob("*") if p.is_dir()}
    filtered_resources = [
        resource
        for resource in resources
        if any(resource.get(i) for i in ("links", "assignmentLink"))
        and _infer_path_from_title(resource["title"]).name not in stored_resources
    ]
    return filtered_resources


def main(resources: list[dict[str, Any]]):
    dl_resources = []
    try:
        with httpx.Client(follow_redirects=True) as client:
            for resource in resources:
                try:
                    dl_resources.append(download_resources(resource, client) or {})
                except TypeError:
                    continue
    except Exception:
        raise
    finally:
        [store_resources(i) for i in dl_resources]
        print("🥳 DONE!")


if __name__ == "__main__":
    all_resources = json.loads(_io.open_file(C.CLEANED_RESOURCES_PATH))
    filtered_resources = filter_stored_resources(all_resources)
    main(all_resources)
