from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from main.client.ai.open_ai import create_client_info
from main.model.api.user_model import CreateUserRs, UserRs
from main.model.entity.user import User
from main.persistence.user_repository import UserRepository

import logging as log


def map_user_entity_to_user_rs(user: User) -> UserRs:
    return UserRs(id=user.id, login=user.login, age=user.age, gender=user.gender, name=user.name, surname=user.surname,
                  description=user.description, created_at=user.created_at)


class UserService:

    @staticmethod
    async def create_user(login: str):
        additional_client_info = await create_client_info(login)

        user = User(
            id=str(uuid4()),
            login=login,
            age=additional_client_info.age,
            gender=str(additional_client_info.gender.name),
            name=additional_client_info.name,
            surname=additional_client_info.surname,
            description=additional_client_info.description,
            created_at=datetime.now()
        )

        user = await UserRepository.save(user=user)
        log.info(f"Создан новый пользователь: {user}")

        return CreateUserRs(id=user.id)

    @staticmethod
    async def get_user(user_id: str):
        user = await UserRepository.find_one(user_id)
        return map_user_entity_to_user_rs(user)

    @staticmethod
    async def get_users(registered_after: Optional[datetime]) -> List[UserRs]:
        users = await UserRepository.find_all(registered_after)
        return [map_user_entity_to_user_rs(user) for user in users]
