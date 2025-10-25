from datetime import datetime
from typing import List, Optional, Annotated

from fastapi import Depends
from pydantic.v1.typing import is_none_type
from sqlalchemy import select, exists

from main.model.entity.user import User
from main.persistence.session import DbSessionDepends


class UserRepository:

    def __init__(self, session: DbSessionDepends):
        self.session = session

    async def save(self, user: User) -> User:
        self.session.begin()
        stmt = select(exists().where(User.login == user.login))
        ex = await self.session.execute(stmt)
        if ex.scalar():
            raise RuntimeError()

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def find_one(self, user_id: str) -> User:
        self.session.begin()
        stmt = select(User).where(User.id == user_id)
        ex = await self.session.execute(stmt)
        user = ex.scalar_one_or_none()
        if is_none_type(user):
            raise RuntimeError(f"Не найден пользователь с id {user_id}")
        await self.session.commit()
        return user

    async def find_all(self, registered_after: Optional[datetime]) -> List[User]:
        self.session.begin()
        if registered_after is None:
            stmt = select(User).order_by(User.created_at.asc())
        else:
            stmt = select(User).where(User.created_at >= registered_after).order_by(User.created_at.asc())
        ex = await self.session.execute(stmt)
        users = ex.scalars().all()
        await self.session.commit()
        return users


UserRepositoryDepends = Annotated[UserRepository, Depends()]
