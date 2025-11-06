from functools import lru_cache
from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main.config.settings import get_settings


def __get__db_url():
    return URL.create(
        drivername=get_settings().db.driver,
        username=get_settings().db.username,
        password=get_settings().db.password.get_secret_value(),
        host=get_settings().db.host,
        port=get_settings().db.port,
        database=get_settings().db.database
    )


def __get_engine():
    return create_async_engine(
        __get__db_url(),
        echo=get_settings().db.debug,
        connect_args={"server_settings": {"search_path": get_settings().db.db_schema}}
    )


@lru_cache
def __get_session() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=__get_engine(),
        autoflush=False,
        expire_on_commit=False,  # Не перезагружать объекты после коммита
    )


async def __with_session() -> AsyncGenerator[AsyncSession, None]:
    session = __get_session()
    async with session() as session:
        try:
            yield session
        finally:
            # Соединение закроется из-за with
            pass


DbSessionDepends = Annotated[AsyncSession, Depends(__with_session)]
