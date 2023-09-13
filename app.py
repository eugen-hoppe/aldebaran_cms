from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from cms.dependencies import options
from cms.engine import api, content
from cms.models import Options
from settings import config
from utils import tree

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
    if path.endswith("/index"):  # TODO: remove this
        return RedirectResponse(f"{path[:-6]}")
    if path.endswith(".md"):
        return RedirectResponse(f"{path[:-3]}")
    html = await content(opt=opt, location=config.CMS.web(path=path))
    
    # Build site structure as data tree
    # =================================
    cache_ = {}
    registry = tree.dir_tree(
        entrypoint=config.CMS.web(),
        cache=cache_,
        cache_function=tree.parent_title
    )
    tree.update_tree(registry, cache_)

    # Build menu
    # ==========
    menu_items: list[tuple(str, str, str)] = [
        ("/", registry[""]["files"][-1], "root")
    ]
    actual_path = html.directory().removeprefix(config.CMS.web())
    actual_node: dict[str, list[str]] = registry[actual_path]
    for parent in actual_node["parents"]:
        parent_title = registry[parent]["files"][-1]
        menu_items.append((parent, parent_title, "previous"))
    
    if actual_path != "":
        menu_items.append((actual_path, actual_node["files"][-1], "actual"))

    for child in actual_node["paths"]:
        files = registry[child]["files"]
        md_files = [file for file in files if file.endswith(".md")]
        if len(md_files) > 0:
            menu_items.append((child, md_files[-1], "next"))
    crumbs: list[tuple[str, str]] = []
    menus: list[tuple[str, str]] = []
    for menu_item in menu_items:
        path: str = menu_item[0]
        file: str =  menu_item[1]
        nav_type: str = menu_item[2]
        nav_name = file.removesuffix(".md")
        if "_" in nav_name:
            name_parts = nav_name.split("_")
            if name_parts[0].startswith("x"):
                nav_name = " ".join(name_parts[1:])
            else:
                nav_name = " ".join(name_parts)
        ht = "h5"
        if nav_type == "root":
            if actual_path == "":
                ht = "h4"
                crumbs.append((path, f"<{ht}>[ " + nav_name + f" ] / </{ht}>"))
            else:
                rname = f"<{ht}>| " + nav_name.lower().replace(" ", "_") + f" |</{ht}>"
                crumbs.append((path, rname))
        if nav_type == "previous":
            crumbs.append((path, "#" + nav_name.lower()))
        elif nav_type == "actual":
            menus.append((path, "<b>@" + nav_name.lower() + "</b>"))
        elif nav_type == "next":
            menus.append((path, "[ " + nav_name + " ]"))

    payload = {
        "request": request,
        "title": config.CMS.WEBSITE_NAME.value,
        "body": html.body,
        "crumbs": crumbs,
        "menu": menus
    }
    return templates.TemplateResponse("base.html", payload)
