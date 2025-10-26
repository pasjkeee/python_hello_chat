from datetime import datetime
from typing import List, Optional, Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from main.model.entity.user import User
from main.persistence.session import DbSessionDepends
from .exception import UserAlreadyExists, UserNotFound


class UserRepository:

    def __init__(self, session: DbSessionDepends):
        self.session = session

    async def save(self, user: User) -> User:
        """
        Создать нового пользователя

        Args:
            user (User): ORM-объект ``User``

        Returns:
            User: ORM-объект ``User``

        Raises:
            UserAlreadyExists: Пользователь с данным ``login`` уже существует.
        """
        try:
            async with self.session.begin():
                self.session.add(user)
                await self.session.flush()
        except IntegrityError:
            raise UserAlreadyExists()
        await self.session.refresh(user)
        return user

    async def find_one(self, user_id: str) -> User:
        """
        Получить пользователя по идентификатору ``user_id``

        Args:
            user_id (str): Уникальный идентификатор пользователя.

        Returns:
            User: ORM-объект ``User``

        Raises:
            UserNotFound: Если пользователь не найден.
        """
        async with self.session.begin():
            stmt = select(User).where(User.id == user_id)
            ex = await self.session.execute(stmt)
            user = ex.scalar_one_or_none()
            if user is None:
                raise UserNotFound(f"Не найден пользователь с id {user_id}")
            return user

    async def find_all(self, registered_after: Optional[datetime]) -> List[User]:
        """
        Получить список всех пользователей, отсортированных по дате регистрации.
        Если параметр ``registered_after`` задан, возвращаются только пользователи, у которых ``created_at``
        больше или равно указанной дате.
        Если параметр ``registered_after`` равен ``None``, возвращаются все пользователи.

        Args:
            registered_after (Optional[datetime]): Дата/время фильтрации.
            Если указано, будут выбраны пользователи, зарегистрированные начиная с этого момента.

        Returns:
            List[User]: Список ORM-объектов ``User``, отсортированных по возрастанию поля ``created_at``.
        """
        async with self.session.begin():
            if registered_after is None:
                stmt = select(User).order_by(User.created_at.asc())
            else:
                stmt = select(User).where(User.created_at >= registered_after).order_by(User.created_at.asc())
            ex = await self.session.execute(stmt)
            users = ex.scalars().all()
            return users


UserRepositoryDepends = Annotated[UserRepository, Depends()]
