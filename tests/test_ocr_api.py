import asyncio
from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from app.api.ocr import ocr_endpoint


def make_upload(
    filename: str = "handwriting.jpg",
    content_type: str = "image/jpeg",
    image_bytes: bytes = b"test image bytes",
) -> UploadFile:
    return UploadFile(
        file=BytesIO(image_bytes),
        filename=filename,
        headers=Headers({"content-type": content_type}),
    )


def test_returns_ocr_text_for_valid_image() -> None:
    image_bytes = b"jpeg bytes"
    extract_text = AsyncMock(return_value="手書きの文字")

    with patch("app.api.ocr.extract_text_from_image", extract_text):
        response = asyncio.run(ocr_endpoint(make_upload(image_bytes=image_bytes)))

    assert response.text == "手書きの文字"
    extract_text.assert_awaited_once_with(image_bytes, "image/jpeg")


@pytest.mark.parametrize(
    ("filename", "content_type"),
    [
        ("handwriting.gif", "image/gif"),
        ("handwriting.jpg", "application/octet-stream"),
        ("handwriting.jpeg", None),
    ],
)
def test_rejects_invalid_image_upload(
    filename: str, content_type: str | None
) -> None:
    headers = (
        Headers({"content-type": content_type}) if content_type is not None else Headers()
    )
    upload = UploadFile(
        file=BytesIO(b"not an accepted image"),
        filename=filename,
        headers=headers,
    )

    with (
        patch("app.api.ocr.extract_text_from_image", new_callable=AsyncMock) as extract,
        pytest.raises(HTTPException) as exc_info,
    ):
        asyncio.run(ocr_endpoint(upload))

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid image file format."
    extract.assert_not_awaited()


def test_converts_ocr_failure_to_internal_server_error() -> None:
    with (
        patch(
            "app.api.ocr.extract_text_from_image",
            new_callable=AsyncMock,
            side_effect=RuntimeError("provider unavailable"),
        ),
        pytest.raises(HTTPException) as exc_info,
    ):
        asyncio.run(ocr_endpoint(make_upload()))

    assert exc_info.value.status_code == 500
    assert (
        exc_info.value.detail
        == "OCR processing failed: provider unavailable"
    )
