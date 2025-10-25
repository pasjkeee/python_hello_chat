from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from .db import DatabaseSettings
from .openai import OpenAiSettings

class Settings(BaseSettings):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    openai: OpenAiSettings = Field(default_factory=OpenAiSettings)

    model_config = SettingsConfigDict(
        env_file=".env", # только локально
        env_file_encoding="utf-8", # только локально
        extra='ignore',
        case_sensitive=False,
        env_nested_delimiter="__"
    )

settings = Settings()
