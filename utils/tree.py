import os
from typing import Any, Callable


def dir_walk(init_path: str) -> list[tuple[str, list[str], list[str]]]:
    return [(root, dirs, files) for root, dirs, files in os.walk(init_path)]


def dir_tree(
        entrypoint: str,
        file_extention: str,
        keys: tuple[str, str, str] = ("parents", "files", "paths"),
        cache: dict[str, dict[str, Any]] | None = None,
        cache_function: Callable | None = None,
        exclude_prefix_dirs: list[str] = ["."]
        ) -> dict[str, dict[str, list[str]]]:
    dir_db = {}
    dirs = dir_walk(entrypoint)
    for path, rel_dir_paths, file_list in dirs:
        path = path.removeprefix(entrypoint)
        file_paths = []
        for file_name in file_list:
            if file_name.endswith(file_extention):
                file_paths.append(file_name.removesuffix(file_extention))
        rel_parent_paths = path.split("/")[:-1][1:]
        abs_parent_paths: list[str] = []
        for i in range(1, len(rel_parent_paths) + 1):
            abs_parent_paths.append("/" + "/".join(rel_parent_paths[:i]))
        abs_dirs: list[str] = []
        for rel_dir_path in rel_dir_paths:
            exclude = False
            for prefix in exclude_prefix_dirs:
                if rel_dir_path.startswith(prefix):
                    exclude = True
            if exclude:
                continue
            abs_dirs.append(path + "/" + rel_dir_path)
        abs_dirs = sorted(abs_dirs, reverse=False)
        file_paths = sorted(file_paths, reverse=True)

        k1, k2, k3 = keys
        dir_db[path] = {k1: abs_parent_paths, k2: file_paths, k3: abs_dirs}

        if isinstance(cache, dict):
            if isinstance(cache_function, Callable):
                cache_function(dir_db, path, cache)
        
    return dir_db


def update_tree(tree: dict[str, dict[str, list[str]]], tree_cache: dict[str, str]):
    for path in tree_cache:
        tree[path]["root_pages"] = []
        tree[path]["root_crumbs"] = []
        for i in range(1, len(tree[path]["parents"])):
            parent_page = tree_cache[tree[path]["parents"][-i]]

            tree[path]["root_pages"].append(parent_page)
            tree[path]["root_crumbs"].append("/".join(tree[path]["parents"][:-i][1:]))
