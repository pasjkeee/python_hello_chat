from datetime import datetime

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
