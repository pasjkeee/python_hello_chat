from openai import BaseModel
from pydantic import Field


class UserCreatedMsg(BaseModel):
    rq_id: str = Field(...)
    user_id: str = Field(...)
