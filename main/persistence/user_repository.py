from datetime import datetime
from typing import List, Optional

from pydantic.v1.typing import is_none_type

from main.model.entity.user import User
from sqlalchemy import select, exists
from main.persistence.session import AsyncSessionLocal


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
    async def find_all(since: Optional[datetime]) -> List[User]:
        async with AsyncSessionLocal() as session:
            if since is None:
                stmt = select(User).order_by(User.created_at.asc())
            else:
                stmt = select(User).where(User.created_at >= since).order_by(User.created_at.asc())
            users = (await session.execute(stmt)).scalars().all()
            await session.commit()
            return users
