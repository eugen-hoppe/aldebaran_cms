from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from cms.engine import content
from cms.dependencies import options
from cms.models import Options
from settings import config


cms = FastAPI()


cms.mount("/static", StaticFiles(directory="cms/static"), name="static")


templates = Jinja2Templates(directory="cms/templates")


@cms.get("/favicon.ico")
async def favicon():
    return FileResponse("cms/static/favicon.ico")


@cms.get("/", response_class=HTMLResponse)
async def html(
        request: Request,
        opt: Annotated[Options, Depends(options)]):
    path = request.url.path
    if request.url.path == "/":
        path = config.CMS.ROOT.value

    template = "base.html"

    html_body = await content(opt=opt, path=path)
    payload = {
        "request": request,
        "title": config.CMS.WEBSITE_NAME.value,
        "body": html_body,
    }

    return templates.TemplateResponse(template, payload)
