from enum import Enum


class CMS(str, Enum):
    WEBSITE_NAME: str = "Aldebaran CMS"
    ROOT: str = "content"
    INDEX_FILENAME: str = "index"
    MODE: str = "development"

    @staticmethod
    def admin_path():
        return f"{CMS.ROOT.value}/admin"
    
    @staticmethod
    def status_path(status: int = 404):
        return f"{CMS.admin_path()}/status/{status}.md"
    
    @staticmethod
    def web(path: str = ""):
        return f"{CMS.ROOT.value}/web" + path
