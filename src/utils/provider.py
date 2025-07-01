from utils.gemini import GeminiClient
from utils.openai import OpenAIClient
from utils.azure_openai import AzureOpenAIClient

model_names = {
    "OpenAI": {
        "gpt-4.1": "gpt-4.1",
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini"
    },
    "Azure": {
        "gpt-4.1-mini": "gpt-4.1-mini",
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini"
    },
    "Google": {
        "gemini-2.0-flash": "gemini-2.0-flash",
        "gemini-2.5-pro": "gemini-2.5-pro"
    },
    "Anthropic": {
        "claude-3-5-sonnet": "claude-3-5-sonnet-20240620",
        "claude-3-5-haiku": "claude-3-5-haiku-20240307",
        "claude-3-7-sonnet": "claude-3-7-sonnet-20250219"
    }
}

class LLMProvider:
    def __init__(self, client_name, model_name):
        self.client_name = client_name
        self.model_name = model_name

    def get_client(self):
        if self.client_name == "OpenAI":
            return OpenAIClient(model_name=self.model_name)
        elif self.client_name == "Azure":
            return AzureOpenAIClient(model_name=self.model_name)
        elif self.client_name == "Google":
            return GeminiClient(model_name=self.model_name)
        # elif self.client_name == "Anthropic":
        #     return AnthropicClient(model_name=self.model_name)