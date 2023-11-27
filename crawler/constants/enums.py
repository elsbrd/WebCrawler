from enum import Enum


class StatusCode(int, Enum):
    HTTP_200_OK = 200


class ContentType(str, Enum):
    TEXT_HTML = "text/html"
