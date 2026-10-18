from __future__ import annotations

import io
from pathlib import Path

import httpx
import respx

from skolaonline import AsyncSkolaOnline, DownloadedFile, SkolaOnline
from tests._helpers import BASE_URL


@respx.mock
def test_download_returns_content_and_metadata() -> None:
    respx.get(f"{BASE_URL}/api/v1/messages/m1/attachments/a1").mock(
        return_value=httpx.Response(
            200,
            content=b"%PDF-1.7",
            headers={
                "Content-Type": "application/pdf; charset=binary",
                "Content-Disposition": (
                    "attachment; filename*=UTF-8''r%C3%A9sum%C3%A9.pdf"
                ),
            },
        )
    )
    file = SkolaOnline(access_token="t").messages.download_attachment("m1", "a1")
    assert file == DownloadedFile(
        content=b"%PDF-1.7", filename="résumé.pdf", content_type="application/pdf"
    )


@respx.mock
def test_download_without_metadata() -> None:
    respx.get(f"{BASE_URL}/api/v1/files/f1/download").mock(
        return_value=httpx.Response(200, content=b"raw")
    )
    file = SkolaOnline(access_token="t").files.download("f1")
    assert file.content == b"raw"
    assert file.filename is None


@respx.mock
def test_homework_attachment_download_sends_student(tmp_path: Path) -> None:
    route = respx.get(
        f"{BASE_URL}/api/v1/student/homeworks/assignment/attachments/a1"
    ).mock(
        return_value=httpx.Response(
            200,
            content=b"text",
            headers={"Content-Disposition": 'attachment; filename="task.txt"'},
        )
    )
    file = SkolaOnline(access_token="t").homeworks.download_assignment_attachment(
        "a1", student_id="s1"
    )
    assert route.calls.last.request.url.params["StudentId"] == "s1"
    target = tmp_path / (file.filename or "out")
    file.save(target)
    assert target.read_bytes() == b"text"


@respx.mock
def test_upload_multiple_files() -> None:
    route = respx.post(f"{BASE_URL}/api/v1/files/upload").mock(
        return_value=httpx.Response(200, json={"uploadResults": []})
    )
    handle = io.BytesIO(b"second")
    handle.name = "/tmp/second.txt"
    result = SkolaOnline(access_token="t").files.upload(
        [("first.txt", b"first", "text/plain"), handle, b"third"]
    )
    assert result.upload_results == []
    body = route.calls.last.request.content
    assert body.count(b'name="Files"') == 3
    assert b'filename="first.txt"' in body
    assert b'filename="second.txt"' in body
    assert b'filename="file"' in body
    assert b"Content-Type: text/plain" in body


@respx.mock
def test_upload_message_attachment_with_parameters() -> None:
    route = respx.post(f"{BASE_URL}/api/v1/messages/m1/attachments").mock(
        return_value=httpx.Response(200, json={"id": "att"})
    )
    result = SkolaOnline(access_token="t").messages.upload_attachment(
        "m1", ("photo.jpg", b"jpeg"), name="photo.jpg", display_name="Photo"
    )
    assert result == {"id": "att"}
    request = route.calls.last.request
    assert dict(request.url.params) == {"Name": "photo.jpg", "NameUser": "Photo"}
    assert b'name="Data"; filename="photo.jpg"' in request.content


@respx.mock
async def test_async_upload_and_download() -> None:
    upload = respx.post(
        f"{BASE_URL}/api/v1/student/homeworks/h1/elaboration/attachments"
    ).mock(return_value=httpx.Response(200))
    respx.get(f"{BASE_URL}/api/v1/files/f1/download").mock(
        return_value=httpx.Response(200, content=b"bytes")
    )
    async with AsyncSkolaOnline(access_token="t") as client:
        await client.homeworks.upload_elaboration_attachment(
            "h1", ("work.txt", b"done"), submit=True
        )
        file = await client.files.download("f1")
    assert upload.calls.last.request.url.params["Submit"] == "true"
    assert file.content == b"bytes"
