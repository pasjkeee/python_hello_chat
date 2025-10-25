import logging as log
from datetime import datetime
from typing import List, Optional, Annotated
from uuid import uuid4

from fastapi import Depends

from main.client.ai.open_ai import create_client_info
from main.model.api.user_model import CreateUserRs, UserRs
from main.model.entity.user import User
from main.persistence.user_repository import UserRepositoryDepends


def map_user_entity_to_user_rs(user: User) -> UserRs:
    return UserRs(id=user.id, login=user.login, age=user.age, gender=user.gender, name=user.name, surname=user.surname,
                  description=user.description, created_at=user.created_at)


class UserService:

    def __init__(self, user_repository: UserRepositoryDepends):
        self.user_repository = user_repository

    async def create_user(self, login: str, created_at: datetime):
        additional_client_info = await create_client_info(login)

        user = User(
            id=str(uuid4()),
            login=login,
            age=additional_client_info.age,
            gender=str(additional_client_info.gender.name),
            name=additional_client_info.name,
            surname=additional_client_info.surname,
            description=additional_client_info.description,
            created_at=created_at
        )

        user = await self.user_repository.save(user=user)
        log.info(f"Создан новый пользователь: {user}")

        return CreateUserRs(id=user.id)

    async def get_user(self, user_id: str):
        user = await self.user_repository.find_one(user_id)
        return map_user_entity_to_user_rs(user)

    async def get_users(self, registered_after: Optional[datetime]) -> List[UserRs]:
        users = await self.user_repository.find_all(registered_after)
        return [map_user_entity_to_user_rs(user) for user in users]


UserServiceDepends = Annotated[UserService, Depends()]
