import os
from pprint import pprint
from typing import Any, Callable


def dir_walk(init_path: str) -> list[tuple[str, list[str], list[str]]]:
    return [(root, dirs, files) for root, dirs, files in os.walk(init_path)]


def dir_tree(
        entrypoint: str,
        keys: tuple[str, str, str] = ("parents", "files", "paths"),
        cache: dict[str, dict[str, Any]] | None = None,
        cache_function: Callable | None = None
        ) -> dict[str, dict[str, list[str]]]:
    dir_db = {}
    dirs = dir_walk(entrypoint)
    for path, rel_dir_paths, file_list in dirs:
        path = path.removeprefix(entrypoint)
        rel_parent_paths = path.split("/")[:-1][1:]
        abs_parent_paths: list[str] = []
        for i in range(1, len(rel_parent_paths) + 1):
            abs_parent_paths.append("/" + "/".join(rel_parent_paths[:i]))
        abs_dirs: list[str] = []
        for rel_dir_path in rel_dir_paths:
            abs_dirs.append(path + "/" + rel_dir_path)
        file_list = sorted(file_list, reverse=True)

        k1, k2, k3 = keys
        dir_db[path] = {k1: abs_parent_paths, k2: file_list, k3: abs_dirs}

        if isinstance(cache, dict):
            if isinstance(cache_function, Callable):
                cache_function(dir_db, path, cache)
        
    return dir_db


def parent_title(dir_db: dict[str, dict[str, list[str]]], path: str, cache: dict[str, str]) -> str | None:
    node = dir_db[path]
    if node["parents"]:
        if dir_db[node["parents"][-1]]["files"]:
            parent_node = dir_db[node["parents"][-1]]
            cache[path] = parent_node["files"][-1]


def update_tree(tree: dict[str, dict[str, list[str]]], tree_cache: dict[str, str]):
    for path in tree_cache:
        tree[path]["root_pages"] = []
        tree[path]["root_crumbs"] = []
        for i in range(1, len(tree[path]["parents"])):
            parent_page = tree_cache[tree[path]["parents"][-i]]

            tree[path]["root_pages"].append(parent_page)
            tree[path]["root_crumbs"].append("/".join(tree[path]["parents"][:-i][1:]))

