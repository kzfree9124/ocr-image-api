import base64

from openai import OpenAI

client = OpenAI()

# GPT-4o Visionを使って画像からテキストを抽出する関数
async def extract_text_from_image(image_bytes: bytes, content_type: str) -> str:
    image_data = base64.b64encode(image_bytes).decode("ascii")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{content_type};base64,{image_data}"
                        },
                    },
                    {"type": "text", "text": "画像内の文字を抽出して返してください。"}
                ]
            }
        ]
    )
    
    text = response.choices[0].message.content
    return text