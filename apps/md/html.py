import re
from functools import lru_cache

from markdown import markdown

from settings import options


HTMX_SNIPPET = (
    '.md" class="ahx" hx-target="closest body" hx-swap="innerHTML" hx-push-url="true"'
)


@lru_cache(maxsize=2096)
def from_md(path: str, htmx_on: bool = False) -> str:
    static_web_path = f"{options.Static.web_path}/{path}".removesuffix("/")
    try:
        with open(f"{static_web_path}.md", "r") as markdown_file:
            content = markdown_file.read()
    except FileNotFoundError:
        content = ""
    content= re.sub(r'\]\(([^/]+/)', r'](/\1', content)
    content = re.sub(r'\[.*?__([^]]+)', r'[\1', content)
    html = markdown(
        content,
        extensions=["fenced_code", "codehilite", "tables", "nl2br"]
    )
    if htmx_on:
        html = html.replace("href=", "hx-get=").replace('.md"', HTMX_SNIPPET)
    return html
