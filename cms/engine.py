from typing import Annotated

from fastapi import APIRouter, Depends

from cms.dependencies import options
from cms.models import HTML, MD, Options
from settings import config

api = APIRouter(
    responses={404: {"description": "Not found"}},
)


@api.get("/md", response_model=MD)
async def read_md(
        md_path: str,
        opt: Annotated[Options, Depends(options)]
        ) -> MD:
    """#Reads a markdown file returns it as a MD model."""
    def __md_content(md_file_path: str):
        with open(md_file_path, "r") as markdown_file:
            return markdown_file.read()
    try:
        content = __md_content(f"{md_path}/{opt.index_md()}")
    except FileNotFoundError:
        content = __md_content(md_file_path = opt.md_404_path)
    return MD(path=md_path, content=content)


@api.get("/{path:path}", response_model=HTML)
async def content(
        location: list[str],
        opt: Annotated[Options, Depends(options)]
        ) -> HTML:
    """#Locates and reads a markdown file and returns it as a HTML model."""
    md = await read_md(
        md_path=f"{config.CMS.ROOT.value}{'/'.join(location)}", opt=opt
    )
    return HTML.from_markdown(md)
