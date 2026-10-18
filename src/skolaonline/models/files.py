from __future__ import annotations

from dataclasses import dataclass

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class FileUploadResult(SkolaOnlineModel):
    file_id: str | None = None
    file_name: str | None = None
    successful_upload: bool | None = None


@dataclass(kw_only=True)
class FilesUploadResponse(SkolaOnlineModel):
    upload_results: list[FileUploadResult]
