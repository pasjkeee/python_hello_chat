from pydantic import Field, BaseModel, SecretStr


class DatabaseSettings(BaseModel):
    driver: str = Field('postgresql+asyncpg')
    username: str = Field(...)
    password: SecretStr = Field(...)
    host: str = Field('localhost')
    port: int = Field(5432, ge=1, le=65535)
    database: str = Field('postgres')
    db_schema: str = Field('public')
    debug: bool = Field(True)
