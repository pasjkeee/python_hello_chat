from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .db import DatabaseSettings
from .kafka import KafkaSettings
from .openai import OpenAiSettings


class Settings(BaseSettings):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    openai: OpenAiSettings = Field(default_factory=OpenAiSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)

    model_config = SettingsConfigDict(
        env_file=".env",  # только локально
        env_file_encoding="utf-8",  # только локально
        extra='ignore',
        case_sensitive=False,
        env_nested_delimiter="__"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
