from functools import lru_cache
from pathlib import Path


@lru_cache(8)
def open_file(path: Path | str) -> bytes:
    return Path(path).read_bytes()
