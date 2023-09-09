from typing import Annotated

import markdown
from fastapi import APIRouter, Depends

from cms.dependencies import options
from cms.models import Options
from settings import config

api = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)


@api.get("/{path:path}", response_model=str)
async def content(
        opt: Annotated[Options, Depends(options)],
        path: str = config.CMS.ROOT.value):

    with open(f"{path}/{opt.index_md()}", "r") as f:
        content = f.read()

    html_body = markdown.markdown(content)

    return html_body
