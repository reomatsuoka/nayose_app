import os
import anthropic

class ClaudeClient:
    def __init__(self, model_name):
        self.client = anthropic.Anthropic()
        self.model_name = model_name

    def generate_content(self, system_prompt, user_prompt):
        response = self.client.messages.create(
            model=self.model_name,
            temperature=0,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
        )

        return response.content[0].text
    
    def generate_content_with_image(self, system_prompt, user_prompt, image_url):
        header, base64_data = image_url.split(',', 1)
        media_type = header.split(';')[0].split(':')[1]
        response = self.client.messages.create(
            model=self.model_name,
            system=system_prompt,
            max_tokens=1000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ],
                }
            ],
        )

        return response.content[0].text