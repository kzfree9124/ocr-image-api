import asyncio
import base64
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app.services.ocr_service import extract_text_from_image


@pytest.mark.parametrize("content_type", ["image/jpeg", "image/png"])
def test_sends_base64_data_url_and_returns_extracted_text(
    content_type: str,
) -> None:
    image_bytes = b"test image bytes"
    expected_text = "Recognized handwriting"
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(message=SimpleNamespace(content=expected_text))
        ]
    )

    with patch(
        "app.services.ocr_service.client.chat.completions.create",
        return_value=response,
    ) as create:
        result = asyncio.run(extract_text_from_image(image_bytes, content_type))

    assert result == expected_text
    create.assert_called_once()
    request = create.call_args.kwargs
    assert request["model"] == "gpt-4o-mini"
    content = request["messages"][0]["content"]
    image_url = content[0]["image_url"]["url"]
    prefix, encoded_image = image_url.split(",", maxsplit=1)
    assert prefix == f"data:{content_type};base64"
    assert base64.b64decode(encoded_image) == image_bytes
    assert content[1]["type"] == "text"
    assert "文字を抽出" in content[1]["text"]


def test_propagates_openai_client_errors() -> None:
    with (
        patch(
            "app.services.ocr_service.client.chat.completions.create",
            side_effect=RuntimeError("provider unavailable"),
        ),
        pytest.raises(RuntimeError, match="provider unavailable"),
    ):
        asyncio.run(extract_text_from_image(b"image", "image/jpeg"))
