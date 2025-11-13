from pathlib import Path

COURSE_URL = "https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a/take"
BASE_RESOURCE_URL = "https://learnwith.campusx.in/s/courses/653f50d1e4b0d2eae855480a"
BASE_HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "referer": COURSE_URL,
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_7) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/111.5.0.0 Safari/507.02"
    ),
}

COURSE_HTML_PATH = Path("dsmp2.arv.html")  # Added `.arv` to ignore for *git*
DSMP2_DATA_PATH = Path("data/dsmp2")
COURSE_TOPICS_PATH = DSMP2_DATA_PATH / "courseTopics.json"
COURSE_SUB_TOPICS_PATH = DSMP2_DATA_PATH / "courseSubTopics.json"
SUB_TOPIC_RESOURCES_PATH = DSMP2_DATA_PATH / "subTopicResources.json"
CLEANED_RESOURCES_PATH = SUB_TOPIC_RESOURCES_PATH.with_name("cleanedResources.json")

RESOURCES_PATH = Path("resources")
DSMP_RESOURCES_PATH = RESOURCES_PATH / "DSMP"
