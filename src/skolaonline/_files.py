from __future__ import annotations

import os
from dataclasses import dataclass
from email.message import Message

import httpx

from skolaonline._types import FileContent, FileInput

DEFAULT_FILENAME = "file"


@dataclass(frozen=True)
class DownloadedFile:
    content: bytes
    filename: str | None = None
    content_type: str | None = None

    def save(self, path: str | os.PathLike[str]) -> None:
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
    if isinstance(file, tuple):
        return field, file
    return field, (_default_filename(file), file)
