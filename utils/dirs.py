import os


def in_actual(
        directory: str,
        exclude: list[str] = []
        ) -> list[str]:
    dirs_ = []
    for name in os.listdir(directory):
        if name.startswith("."):
            continue
        if name in exclude:
            continue

        dirs_.append(os.path.join(directory, name))
    return [dir_ for dir_ in dirs_ if os.path.isdir(dir_)]


def get_all(directory: str, exclude: list[str] = []) -> list[str]:
    directories = in_actual(directory, exclude)
    for directory in directories:
        directories.extend(
            get_all(directory, exclude)
        )
    return directories


def entrypoints(
        directory: str,
        entrypoint: str,
        exclude: list[str] = [],
        recursive: bool = False,
        remove_prefix: str | None = None,
        ) -> dict[str, str]:
    if recursive:
        directories = get_all(directory, exclude)
    else:
        directories = in_actual(directory, exclude)
    output = {}
    for directory in directories:
        if remove_prefix:
            directory = directory.replace(remove_prefix, "")
        output[directory] = directory + "/" + entrypoint
    return output


if __name__ == "__main__":
    print(entrypoints("content", "index.md", exclude=["admin"], recursive=True))
