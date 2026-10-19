from __future__ import annotations

from datetime import date, datetime
from typing import IO, TypeAlias

FileContent: TypeAlias = bytes | IO[bytes]
"""Content of an uploaded file: raw bytes or a binary file object."""
FileInput: TypeAlias = (
    FileContent | tuple[str, FileContent] | tuple[str, FileContent, str]
)
"""File to upload: content, (filename, content) or (filename, content, media type)."""
DateLike: TypeAlias = date | datetime
"""Date or date and time accepted by date parameters."""
