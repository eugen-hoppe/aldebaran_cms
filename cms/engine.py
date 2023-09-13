from typing import Annotated

from fastapi import APIRouter, Depends

from cms.dependencies import options
from cms.models import HTML, MD, Options
from settings import config
from utils import dirs

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
        content = __md_content(f"{md_path}")
    except FileNotFoundError:
        content = __md_content(md_file_path = opt.md_404_path)
    return MD(path=md_path, content=content)


@api.get("/{path:path}", response_model=HTML)
async def content(
        location: list[str],
        opt: Annotated[Options, Depends(options)]
        ) -> HTML:
    """#Locates and reads a markdown file and returns it as a HTML model."""
    directory = location
    file_dirs = dirs.in_actual_(directory, only_files=True)
    if not file_dirs:
        file_dirs = [opt.md_404_path]
    md_list: list[MD] = []
    for md_file in file_dirs:
        if md_file.endswith(".md"):
            md = await read_md(md_path=md_file, opt=opt)
            md_list.append(md)
    md_list.sort(key=lambda x: x.title)
    return HTML.from_markdown(md_list[0])
