from __future__ import annotations

from collections.abc import Sequence

from skolaonline._files import DownloadedFile, downloaded_file, to_multipart
from skolaonline._types import FileInput
from skolaonline.models import (
    FilesUploadResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_model,
)


class Files(SyncAPIResource):
    """Endpoints for the temporary file storage."""

    def download(self, file_id: str) -> DownloadedFile:
        """Download a file from the temporary storage.

        Args:
            file_id: ID of the file.

        Returns:
            Downloaded file with its name and content type.
        """
        response = self._request(
            "GET", f"/api/v1/files/{encode_path(file_id)}/download"
        )
        return downloaded_file(response)

    def upload(self, files: Sequence[FileInput]) -> FilesUploadResponse:
        """Upload files to the temporary storage.

        Args:
            files: Files to upload.

        Returns:
            Result of uploading files.
        """
        response = self._request(
            "POST",
            "/api/v1/files/upload",
            files=[to_multipart("Files", file) for file in files],
        )
        return parse_model(response, FilesUploadResponse)


class AsyncFiles(AsyncAPIResource):
    """Asynchronous endpoints for the temporary file storage."""

    async def download(self, file_id: str) -> DownloadedFile:
        """Download a file from the temporary storage.

        Args:
            file_id: ID of the file.

        Returns:
            Downloaded file with its name and content type.
        """
        response = await self._request(
            "GET", f"/api/v1/files/{encode_path(file_id)}/download"
        )
        return downloaded_file(response)

    async def upload(self, files: Sequence[FileInput]) -> FilesUploadResponse:
        """Upload files to the temporary storage.

        Args:
            files: Files to upload.

        Returns:
            Result of uploading files.
        """
        response = await self._request(
            "POST",
            "/api/v1/files/upload",
            files=[to_multipart("Files", file) for file in files],
        )
        return parse_model(response, FilesUploadResponse)
