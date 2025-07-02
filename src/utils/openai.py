import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self, model_name):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    def generate_content(self, system_prompt, user_prompt):
        response = self.client.responses.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": {"type": "input_text", "text": user_prompt}}
            ],
            temperature=0.0,
        )

        return response.output_text
    
    def generate_content_with_file(self, system_prompt, user_prompt, file_type, file_name, data_url):

        if file_type == "application/pdf":
            user_content = [
                {"type": "input_text", "text": user_prompt},
                {
                    "type": "input_file",
                    "filename": file_name,
                    "file_data": data_url,
                },
            ]
        else:
            user_content = [
                {"type": "input_text", "text": user_prompt},
                {
                    "type": "input_image",
                    "image_url": data_url
                },
            ]

        response = self.client.responses.create(
            model=self.model_name,
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": user_content},
            ],
            temperature=0.0,
        )

        return response.output_text