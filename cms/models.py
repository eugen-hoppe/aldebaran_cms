from pydantic import BaseModel

from settings import config


class Options(BaseModel):
    development: bool = True

    def index_md(self):
        if self.development:
            return f"{config.CMS.INDEX_FILENAME_TEST.value}.md"
        return f"{config.CMS.INDEX_FILENAME_DEFAULT.value}.md"
