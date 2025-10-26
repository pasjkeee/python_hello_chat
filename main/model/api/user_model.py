import re
from datetime import datetime, timezone
from typing import Optional

from fastapi.params import Query
from pydantic import BaseModel, field_validator, computed_field, Field

UUID_PATTERN = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


class CreateUserRq(BaseModel):
    rq_id: str = Field(..., examples=["a05ecbfa-4c30-493c-8f6f-2eefe086e9f7"])
    login: str = Field(..., examples=["johndoe"])

    @field_validator("rq_id")
    @classmethod
    def is_uuid_string(cls, v: str) -> str:
        if not bool(UUID_PATTERN.match(v)):
            raise ValueError("rq_id must be uuid valid string")
        return v

    @field_validator("login")
    @classmethod
    def login_lower(cls, v: str) -> str:
        return v.lower()

    @computed_field
    @property
    def created_at(self) -> datetime:
        return datetime.now(timezone.utc)


class CreateUserRs(BaseModel):
    id: str = Field(..., examples=["c04233ada-5d41-493c-8f6f-211fe086e9f1"])

    @classmethod
    @field_validator("id")
    def is_uuid_string(cls, v: str) -> str:
        if not bool(UUID_PATTERN.match(v)):
            raise ValueError("user id must be uuid valid string")
        return v


class UserRs(BaseModel):
    id: str = Field(..., examples=["a05ecbfa-4c30-493c-8f6f-2eefe086e9f7"])
    login: str = Field(..., examples=["pas2"])
    age: int = Field(..., examples=[29])
    gender: str = Field(..., examples=["MALE"])
    name: str = Field(..., examples=["Michael"])
    surname: str = Field(..., examples=["Johnson"])
    description: str = Field(..., examples=["c04233ada-5d41-493c-8f6f-211fe086e9f1"])
    created_at: datetime = Field(..., examples=["2025-10-25T21:21:02.172918Z"])


class GetAllUsersParams:
    def __init__(self, registered_after: Optional[datetime] = Query(None,
                                                                    description="Начиная с времени регистрации пользователя",
                                                                    alias='registeredAfter')):
        self.registered_after = registered_after
