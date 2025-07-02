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
    
    def generate_content_with_file(self, system_prompt, user_prompt, file_type, file_name, data_url):
        _, base64_data = data_url.split(',', 1)

        contents = [user_prompt]
        if file_type == "application/pdf":
            contents.append(
                types.Part.from_bytes(
                    data=base64.b64decode(base64_data),
                    mime_type=file_type
                )
            )
        else:
            image_bytes = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_bytes))
            contents.append(image)

        response = self.client.models.generate_content(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.0,
            ),
            contents=contents,
        )

        return response.text