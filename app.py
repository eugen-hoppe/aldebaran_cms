from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from cms.dependencies import options
from cms.engine import api, content
from cms.models import Options
from settings import config
from utils import dirs

cms = FastAPI()

if config.CMS.MODE.value == "development":
    cms.include_router(api, prefix="/api/v1")



cms.mount("/static", StaticFiles(directory="cms/static"), name="static")
templates = Jinja2Templates(directory="cms/templates")


@cms.get("/{path:path}/")
async def redirect(path: str):
    return RedirectResponse(f"/{path}")


@cms.get("/favicon.ico")
async def favicon():
    return FileResponse("cms/static/favicon.ico")



@cms.get("/{path:path}", response_class=HTMLResponse)
async def html(request: Request, opt: Annotated[Options, Depends(options)]):
    path = request.url.path
    if path.endswith("/index"):  # obsidian compatibility
        return RedirectResponse(f"{path[:-6]}")
    if path.endswith("/index.md"):  # obsidian compatibility
        return RedirectResponse(f"{path[:-9]}")
    location = path.split("/")
    html = await content(
        opt=opt,
        location=location,
    )
    location[0] = "content"
    menu_path = "/".join(location).removesuffix("/")
    menu = dirs.entrypoints(
        menu_path, exclude=["admin"],
        entrypoint="index.md", 
        remove_prefix="content"
    )
    payload = {
        "request": request,
        "title": config.CMS.WEBSITE_NAME.value,
        "body": html.body,
        "menu": [(link, link.split("/")[-1]) for link in menu if link]
    }
    return templates.TemplateResponse("base.html", payload)


