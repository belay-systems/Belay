from pathlib import Path


def ensure(path: Path):

    path.mkdir(parents=True, exist_ok=True)


def touch(path: Path):

    path.touch(exist_ok=True)
