import os


def in_actual_(
        directory: str,
        exclude: list[str] = [],
        only_files: bool = False
        ) -> list[str]:
    dirs_ = []
    for name in os.listdir(directory):
        if name.startswith("."):
            continue
        if name in exclude:
            continue
        dirs_.append(os.path.join(directory, name))
    if only_files:
        return [dir_ for dir_ in dirs_ if os.path.isfile(dir_)]
    return [dir_ for dir_ in dirs_ if os.path.isdir(dir_)]
