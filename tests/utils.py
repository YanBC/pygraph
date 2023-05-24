import os


def current_dir(file: str) -> str:
    full_path = os.path.abspath(file)
    dirname = os.path.dirname(full_path)
    return dirname
