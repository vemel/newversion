from pathlib import Path


def print_path(path: Path) -> str:
    """
    Stringify path as relative to cwd if possible.
    """
    if path.is_absolute():
        try:
            path = path.relative_to(Path.cwd())
        except ValueError:
            return path.as_posix()
    if len(path.parts) == 0:
        return path.absolute().as_posix()
    if len(path.parts) == 1:
        return f"./{path.as_posix()}"

    return path.as_posix()
