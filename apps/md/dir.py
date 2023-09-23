from functools import lru_cache

from settings.constants import Template
from utils.tree import dir_tree, update_tree


def parent_traversal(
        dir_db: dict[str, dict[str, list[str]]],
        path: str,
        cache: dict[str, str]
        ) -> str | None:
    node = dir_db[path]
    if node["parents"]:
        if dir_db[node["parents"][-1]]["files"]:
            parent_node = dir_db[node["parents"][-1]]
            cache[path] = parent_node["files"][-1]


@lru_cache(maxsize=1)
def md_tree(slash_prefix: bool = False):
    tree_cache: dict[str, str] = {}
    tree = dir_tree(
        "static/web",
        file_extention=".md",
        cache=tree_cache,
        cache_function=parent_traversal,
        exclude_prefix_dirs=[".", Template.XTND.value]
    )
    update_tree(tree, tree_cache)
    if not slash_prefix:
        return tree
    aliased_tree = {}
    for path in tree:
        aliased_tree[path] = tree[path]
        if not path.startswith("/"):
            aliased_tree["/" + path] = tree[path]
    return aliased_tree
