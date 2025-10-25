from pydantic import Field, BaseModel, SecretStr


class OpenAiSettings(BaseModel):
    api_key: SecretStr = Field(...)
