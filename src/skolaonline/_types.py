from __future__ import annotations

from datetime import date, datetime
from typing import IO, TypeAlias

FileContent: TypeAlias = bytes | IO[bytes]
FileInput: TypeAlias = (
    FileContent | tuple[str, FileContent] | tuple[str, FileContent, str]
)
DateLike: TypeAlias = date | datetime
