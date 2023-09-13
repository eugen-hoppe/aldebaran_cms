from pydantic import BaseModel

from settings import config

from markdown import markdown

from devtools import debug, Debug # requirements.txt: devtools TODO


class Options(BaseModel):
    development: bool = config.CMS.MODE.value == "development"
    md_404_path: str = config.CMS.status_path(status=404)
    page: str | None = None

    def index_md(self) -> str:
        if isinstance(self.page, str):
            return f"{self.page}.md"
        return f"{config.CMS.INDEX_FILENAME.value}.md"
    
    @staticmethod
    def dev() -> Debug:
        return debug


class Document(BaseModel):
    title: str = config.CMS.WEBSITE_NAME.value
    path: str
    sections: dict[str, str] = {}

    def directory(self) -> str:
        return self.path.rsplit("/", 1)[0]


class MD(Document):
    document_type: str = "md"
    content: str


class HTML(Document):
    __markdown__: MD | None = None
    
    document_type: str = "html"
    template: str = "base.html"
    body: str

    def md(self) -> MD | None:
        return self.__markdown__
    
    def menu(self, md_index = 1) -> str:
        return [key for key in self.sections.values()][md_index - 1]
    
    @staticmethod
    def from_markdown(md: MD) -> "HTML":
        html = HTML(
            title=md.title,
            path=md.path,
            sections=md.sections,
            body=markdown(md.content, extensions=["tables", "fenced_code"])
        )
        html.__markdown__ = md
        return html
