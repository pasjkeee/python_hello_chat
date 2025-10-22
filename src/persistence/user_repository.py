from typing import List

from pydantic.v1.typing import is_none_type

from src.model.entity.user import User
from sqlalchemy import select, exists
from src.persistence import AsyncSessionLocal


class UserRepository:

    @staticmethod
    async def save(user: User) -> User:
        async with AsyncSessionLocal() as session:
            stmt = select(exists().where(User.login == user.login))
            result = (await session.execute(stmt)).scalar()
            if result:
                raise RuntimeError()

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def find_one(user_id: str) -> User:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.id == user_id)
            user = (await session.execute(stmt)).scalar_one_or_none()
            if is_none_type(user):
                raise RuntimeError(f"Не найден пользователь с id {user_id}")
            await session.commit()
            return user

    @staticmethod
    async def find_all() -> List[User]:
        async with AsyncSessionLocal() as session:
            stmt = select(User)
            users = (await session.execute(stmt)).scalars().all()
            await session.commit()
            return users
