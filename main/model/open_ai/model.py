from enum import Enum

from pydantic import BaseModel

"""
    Пол
"""


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    UNKNOWN = 3


"""
    Запрос в ai на создание личности клиента
"""


class CreateClientInfoRs(BaseModel):
    age: int
    gender: Gender
    name: str
    surname: str
    description: str
