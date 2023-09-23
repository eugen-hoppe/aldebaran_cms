from functools import lru_cache

from fastapi.responses import FileResponse


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
