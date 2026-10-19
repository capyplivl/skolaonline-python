from __future__ import annotations

from dataclasses import dataclass

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class FileUploadResult(SkolaOnlineModel):
    """Result of uploading a single file."""

    file_id: str | None = None
    """Unique identifier of the uploaded file."""

    file_name: str | None = None
    """Name of the uploaded file."""

    successful_upload: bool | None = None
    """Whether the file was uploaded successfully."""


@dataclass(kw_only=True)
class FilesUploadResponse(SkolaOnlineModel):
    """Result of uploading files."""

    upload_results: list[FileUploadResult]
    """Upload results with the identifiers of the files."""
