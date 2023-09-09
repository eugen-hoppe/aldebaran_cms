from pydantic import BaseModel

from settings import config

from markdown import markdown



class Options(BaseModel):
    development: bool = config.CMS.MODE.value == "development"
    md_404_path: str = config.CMS.status_path(status=404)

    def index_md(self):
        return f"{config.CMS.INDEX_FILENAME.value}.md"



class Document(BaseModel):
    title: str = config.CMS.WEBSITE_NAME.value
    path: str


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
    
    @staticmethod
    def from_markdown(md: MD) -> "HTML":
        html = HTML(
            title=md.title,
            path=md.path,
            body=markdown(md.content, extensions=["tables", "fenced_code"])
        )
        html.__markdown__ = md
        return html
