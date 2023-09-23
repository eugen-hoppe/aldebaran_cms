from functools import lru_cache

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.md.dir import md_tree
from apps.md.html import from_md
from models import Data
from settings.constants import Template
from settings.status import API_RESPONSES


app = FastAPI(responses=API_RESPONSES)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def cached_static(
        path_dot_ext: str,
        folders: list[str] | None = None,
        cache_items: int = 16
        ) -> FileResponse | None:
    @lru_cache(maxsize=cache_items)
    def __get_static(path: str) -> FileResponse | None:
        folder_exists = False
        if folders is None:
            return FileResponse("static/web/" + path_dot_ext)
        for folder_name in folders:
            if path.startswith(folder_name):
                folder_exists = True
                break
        if not folder_exists:
            return None
        return FileResponse("static/" + path)
    return __get_static(path_dot_ext)


@app.get("{path:path}.{extension}", response_class=FileResponse | RedirectResponse)
async def dot(path: str, extension: str):
    if extension not in ("png", "jpg", "ico", "md", "css", "js", "manifest"):
        raise HTTPException(status_code=400, detail="Unsupported media type")
    static_meta = cached_static(path + "." + extension, folders=["/icon", "/css", "/js"])
    if extension == "md":
        path = path.removesuffix(".md").split("/")
        path = "/".join(path[:-1]) + "#" + path[-1].removesuffix(".md")
        if path.startswith("#"):
            path = "/" + path
        return RedirectResponse(path)
    if static_meta:
        return static_meta
    return cached_static(path + "." + extension, cache_items=248)


@app.get("/{path:path}/", response_class=HTMLResponse)
async def slash(path: str):
    return RedirectResponse("/" + path)


@app.get("{path:path}", response_class=HTMLResponse)
async def html(request: Request, path: str):
    data = Data(request=request)
    tree = md_tree(slash_prefix=True)
    node = tree[path]
    nav_1: list[tuple[str, str]] = []
    for parent_path in node["parents"]:
        nav_1.append((parent_path, tree[parent_path]["files"][-1].split("__")[-1]))
    nav_2: list[tuple[str, str]] = []
    for menu_path in node["paths"]:
        nav_2.append((menu_path, tree[menu_path]["files"][-1].split("__")[-1]))
    if nav_1:
        nav_1 = [(nav_1[-1][0], "")] + nav_1


    content: list[tuple[str, str]] = []
    for file_name in node["files"]:
        div_id = file_name
        md_path = path + "/" + div_id
        content.append((div_id, from_md(md_path)))


    page_title = from_md(path + f"{Template.XTND.value}/page_title")
    if page_title == "":
        page_title = tree[path]["files"][-1].split("__")[-1]
    else:
        page_title = page_title.removeprefix("<p>").removesuffix("</p>")
    if path != "/":
        nav_1 += [(path, page_title)]
    data.payload = {
        "title": page_title,
        "page_is_root": path == "/",
        "nav_1": nav_1,
        "nav_2": nav_2,
        "content": content[::-1],
        "footer": from_md(f"{Template.XTND.value}/footer")
    }
    context = data.context(request)
    return templates.TemplateResponse(data.template(), context)
