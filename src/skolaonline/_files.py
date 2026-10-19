from __future__ import annotations

import os
from dataclasses import dataclass
from email.message import Message

import httpx

from skolaonline._types import FileContent, FileInput

DEFAULT_FILENAME = "file"
"""File name used for uploads of raw bytes."""


@dataclass(frozen=True)
class DownloadedFile:
    """File downloaded from the API."""

    content: bytes
    """Raw content of the file."""

    filename: str | None = None
    """File name from the Content-Disposition header."""

    content_type: str | None = None
    """Media type from the Content-Type header, without parameters."""

    def save(self, path: str | os.PathLike[str]) -> None:
        """Write the content to a file.

        Args:
            path: Path of the file to write. An existing file is overwritten.
        """
        with open(path, "wb") as fh:
            fh.write(self.content)


def _filename_from_headers(headers: httpx.Headers) -> str | None:
    disposition = headers.get("content-disposition")
    if not disposition:
        return None
    message = Message()
    message["content-disposition"] = disposition
    return message.get_filename()


def downloaded_file(response: httpx.Response) -> DownloadedFile:
    """Create a downloaded file from a binary response."""
    content_type = response.headers.get("content-type")
    return DownloadedFile(
        content=response.content,
        filename=_filename_from_headers(response.headers),
        content_type=content_type.split(";")[0].strip() if content_type else None,
    )


def _default_filename(content: FileContent) -> str:
    name = getattr(content, "name", None)
    if isinstance(name, str) and name:
        return os.path.basename(name)
    return DEFAULT_FILENAME


def to_multipart(
    field: str, file: FileInput
) -> tuple[str, tuple[str, FileContent] | tuple[str, FileContent, str]]:
    """Convert a file input to an HTTPX multipart entry for a form field."""
    if isinstance(file, tuple):
        return field, file
    return field, (_default_filename(file), file)
