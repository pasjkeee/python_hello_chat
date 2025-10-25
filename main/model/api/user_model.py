from datetime import datetime
from typing import Optional

from fastapi.params import Query
from pydantic import BaseModel


class CreateUserRq(BaseModel):
    rqId: str
    login: str


class CreateUserRs(BaseModel):
    id: str


class UserRs(BaseModel):
    id: str
    login: str
    age: int
    gender: str
    name: str
    surname: str
    description: str
    created_at: datetime


class GetAllUsersParams:
    def __init__(self, registered_after: Optional[datetime] = Query(None,
                                                                    description="Начиная с времени регистрации пользователя",
                                                                    alias='registeredAfter')):
        self.registered_after = registered_after
