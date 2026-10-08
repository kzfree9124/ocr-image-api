from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ocr_schema import OCRResponse
from app.services.ocr_service import extract_text_from_image
from app.utils.file_validator import validate_image_file

router = APIRouter()

@router.post("/ocr", response_model=OCRResponse)
async def ocr_endpoint(file: UploadFile = File(...)):
    """
    OCR API エンドポイント
    - 画像ファイルを受け取り
    - GPT-4o Vision で文字を抽出し
    - 抽出結果を返す
    """
    
    content_type = file.content_type
    if content_type is None or not validate_image_file(file):
        raise HTTPException(status_code=400, detail="Invalid image file format.")

    image_bytes = await file.read()
    
    try:
        text = await extract_text_from_image(image_bytes, content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
    
    return OCRResponse(text=text)