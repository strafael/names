import re
import unicodedata
from typing import Generator

PATTERN = re.compile(r"[^\w\s]")


def pipeline(filename: str) -> Generator[str, None, None]:
    with open(filename) as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            if line[0] == "#":
                continue
            line = PATTERN.sub("", line)
            line = remove_accents(line)
            line = line.lower()
            yield line


def remove_accents(text) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode()
    return text
