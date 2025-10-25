from openai import OpenAI
from src.config.settings import settings

open_ai_client = OpenAI(
    api_key=settings.openai.api_key.get_secret_value()
)
