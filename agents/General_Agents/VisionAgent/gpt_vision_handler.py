# gpt_vision_handler.py – GPT-4o Vision Modul

import os
import openai
import base64
from PIL import Image
from io import BytesIO

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_image(file_path: str, user_instruction: str = "Was ist auf diesem Bild zu sehen?") -> str:
    """
    Öffnet das Bild, wandelt es in base64 um und übergibt es an GPT-4o für visuelle Analyse.
    """
    try:
        with Image.open(file_path) as img:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": user_instruction},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                ]}
            ]
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"❌ Fehler bei der Bildanalyse: {e}"
