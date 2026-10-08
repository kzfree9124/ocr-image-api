from io import BytesIO

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers

from app.utils.file_validator import validate_image_file


def make_upload(filename: str, content_type: str) -> UploadFile:
    return UploadFile(
        file=BytesIO(b"image"),
        filename=filename,
        headers=Headers({"content-type": content_type}),
    )


@pytest.mark.parametrize(
    ("filename", "content_type"),
    [
        ("photo.jpg", "image/jpeg"),
        ("photo.jpeg", "image/jpeg"),
        ("photo.png", "image/png"),
        ("PHOTO.JPG", "image/jpeg"),
    ],
)
def test_accepts_supported_image_files(filename: str, content_type: str) -> None:
    assert validate_image_file(make_upload(filename, content_type)) is True


@pytest.mark.parametrize(
    ("filename", "content_type"),
    [
        ("photo.gif", "image/gif"),
        ("photo.jpg", "image/png"),
        ("photo.jpeg", "image/png"),
        ("photo.png", "image/jpeg"),
        ("photo.png", "application/octet-stream"),
        ("photo", "image/jpeg"),
    ],
)
def test_rejects_unsupported_extension_or_content_type(
    filename: str, content_type: str
) -> None:
    assert validate_image_file(make_upload(filename, content_type)) is False
