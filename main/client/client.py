from functools import lru_cache

from openai import OpenAI

from main.config.settings import get_settings


@lru_cache
def get_open_ai_client():
    """
    Создание клиента open ai
    """
    return OpenAI(
        api_key=get_settings().openai.api_key.get_secret_value()
    )
