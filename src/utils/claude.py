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
    
    def generate_content_with_file(self, system_prompt, user_prompt, file_type, file_name, data_url):
        _, base64_data = data_url.split(',', 1)

        if file_type == "application/pdf":
            source_type = "document"
        else:
            source_type = "image"

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
                            "type": source_type,
                            "source": {
                                "type": "base64",
                                "media_type": file_type,
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