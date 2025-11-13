import logging
import os
import time
from pathlib import Path

import httpx

from . import constant as C
from . import course_parser as cp

# Logging configs
LOG_FILE_PATH = Path("course_parser.log")
LOG_FILE_PATH.touch(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]:%(levelname)s    - %(message)s",
    handlers=[
        logging.StreamHandler() if os.getenv("STREAM_LOG") else logging.NullHandler(),
        logging.FileHandler(LOG_FILE_PATH),
    ],
)
logger = logging.getLogger("course_parser")


def get_resources_to_fetch() -> list[cp.CourseSubTopic]:
    # Parse website's html and extract course's topics
    # course_topic_tag = cp.CourseTopic.search(Path("campusx.arv.html"))
    # topics = list(cp.CourseTopic.parse(course_topic_tag))
    # sub_topics = [i for topic in topics for i in cp.CourseSubTopic.parse(topic)]

    # Read stored json file for sub_topics
    sub_topics = list(cp.CourseSubTopic.from_json(C.COURSE_SUB_TOPICS_PATH))
    logger.info("❗ Length of SubTopics: %d", len(sub_topics))
    return cp.filter_resources(sub_topics, cp.load_resources())


def fetch_resources(
    resources_to_fetch: list[cp.CourseSubTopic],
    resource_type: cp.ResourceType,
    *,
    n_resources: int = 30,
) -> list[cp.CourseVideoResource]:
    fetched_resources = []
    counter = 1

    for sub_topic in reversed(resources_to_fetch):
        if sub_topic.type != resource_type:
            logger.debug(
                "👎 subtopic id=%s is not a %s resource.",
                sub_topic.id,
                resource_type,
            )
            continue
        if counter % 10 == 0:
            t_ = 5
            logger.warning("😴 sleeping for %d seconds...", t_)
            time.sleep(t_)

        logger.info(
            "😃 %d. Storing data of sub_topic title='%s'", counter, sub_topic.title
        )
        try:
            with httpx.Client(
                base_url=C.BASE_RESOURCE_URL,
                headers=C.BASE_HEADERS,
                cookies=cp.get_cookies(),
            ) as client:
                fetched_resources.append(
                    cp._RESOURCE_TYPE_MAPPING[resource_type].fetch(client, sub_topic)
                )
            # After fetching 50 video resources it stops.
            if counter == n_resources:
                raise httpx.HTTPError("Intensional Error")
        except (httpx.HTTPError, ValueError) as e:
            logger.error("❌ Error Occurred: %s: %s", type(e).__name__, e)
            logger.exception(e)
            logger.critical("🪣 Total results fetched: %d", len(fetched_resources))
            return fetched_resources
        else:
            time.sleep(1)
            counter += 1

    return fetched_resources


def main():
    resources_to_fetch = get_resources_to_fetch()
    logger.info("❗ Resources to fetch: %d", len(resources_to_fetch))
    fetched_resources = fetch_resources(
        resources_to_fetch,
        cp.ResourceType.video,
        n_resources=30,
    )
    # Store the data into a JSON file
    cp.dump_resources(fetched_resources)
    logger.info("🐸 Data has been stored into file.")


if __name__ == "__main__":
    main()
