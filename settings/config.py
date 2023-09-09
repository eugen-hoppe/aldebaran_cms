from enum import Enum


class CMS(str, Enum):
    WEBSITE_NAME: str = "Aldebaran CMS"
    ROOT: str = "content"
    INDEX_FILENAME_DEFAULT: str = "index"
    INDEX_FILENAME_TEST: str = "index_test"
