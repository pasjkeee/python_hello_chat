from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main.config.settings import settings

__db_url = URL.create(
    drivername=settings.db.driver,
    username=settings.db.username,
    password=settings.db.password.get_secret_value(),
    host=settings.db.host,
    port=settings.db.port,
    database=settings.db.database
)

__engine = create_async_engine(
    __db_url,
    echo=settings.db.debug,
    connect_args={"server_settings": {"search_path": settings.db.db_schema}}
)

__Session = async_sessionmaker(
    bind=__engine,
    autoflush=False,
    expire_on_commit=False,  # Не перезагружать объекты после коммита
)


async def __get_session() -> AsyncGenerator[AsyncSession, None]:
    async with __Session() as session:
        try:
            yield session
        finally:
            # Соединение закроется из-за with
            pass


DbSessionDepends = Annotated[AsyncSession, Depends(__get_session)]
