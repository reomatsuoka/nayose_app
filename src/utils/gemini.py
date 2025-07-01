import os
import base64
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, model_name):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model_name

    def generate_content(self, system_prompt, user_prompt):
        response = self.client.models.generate_content(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            ),
            contents=user_prompt,
            temperature=0.0,
        )

        return response.text
    
    def generate_content_with_image(self, system_prompt, user_prompt, image_url):
        _, base64_data = image_url.split(',', 1)
        image_bytes = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_bytes))
        
        response = self.client.models.generate_content(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.0,
            ),
            contents=[
                user_prompt,
                image
            ],
        )

        return response.text