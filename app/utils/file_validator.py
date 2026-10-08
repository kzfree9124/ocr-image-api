from fastapi import UploadFile

CONTENT_TYPE_BY_EXTENSION = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}

# 画像ファイルの拡張子とMIMEタイプをチェック
def validate_image_file(file: UploadFile) -> bool:
    filename = file.filename.lower()
    extension = filename.split(".")[-1]
    return CONTENT_TYPE_BY_EXTENSION.get(extension) == file.content_type