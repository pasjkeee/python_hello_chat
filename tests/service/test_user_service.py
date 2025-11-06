import asyncio
import datetime
from typing import cast
from unittest.mock import create_autospec, AsyncMock
from uuid import uuid4

import pytest

from main.client.ai.open_ai import OpenAiCreateClientInfo
from main.model.api.user_model import CreateUserRs, UserRs
from main.model.entity.user import User
from main.model.open_ai.model import CreateClientInfoRs, Gender
from main.persistence.user_repository import UserRepository
from main.server.kafka.default_producer import DefaultProducerDepends
from main.service.user_service import UserService


def future_ok(value=None):
    f = asyncio.Future()
    f.set_result(value)
    return f


@pytest.mark.asyncio
async def test_create_user_success():
    # given
    user_id = str(uuid4())
    user = get_user_1(user_id)

    user_repository_mock = create_autospec(UserRepository, spec_set=True, instance=True)
    user_repository_mock.save = AsyncMock(return_value=user)

    open_ai_create_client_info_mock = create_autospec(OpenAiCreateClientInfo, spec_set=True, instance=True)
    open_ai_create_client_info_mock.create_client_info = AsyncMock(return_value=get_create_client_info_rs())

    producer_mock = create_autospec(DefaultProducerDepends, spec_set=True, instance=True)
    producer_mock.send_user_created_msg = AsyncMock(return_value=future_ok("OK"))

    service = UserService(user_repository=user_repository_mock,
                          open_ai_create_client_info=open_ai_create_client_info_mock, producer=producer_mock)

    # when
    login = "login"
    created_at = datetime.datetime.now()
    result = await service.create_user(login, created_at)

    # then
    assert result == CreateUserRs(id=user.id)

    open_ai_create_client_info_mock.create_client_info.assert_awaited_once_with(login)
    user_repository_mock.save.assert_awaited_once()

    producer_mock.send_user_created_msg.assert_awaited_once()

    args, kwargs = user_repository_mock.save.call_args
    user_capture = cast(User, kwargs["user"])

    assert user_capture.login == login
    assert user_capture.id is not None
    assert user_capture.name == "n"
    assert user_capture.surname == "s"
    assert user_capture.description == "d"
    assert user_capture.created_at is not None
    assert user_capture.gender == "MALE"
    assert user_capture.age == 10


@pytest.mark.asyncio
async def test_get_user_success():
    # given
    user_id = str(uuid4())
    user = get_user_1(user_id)
    rs = get_user_rs_1(user)

    user_repository_mock = create_autospec(UserRepository, spec_set=True, instance=True)
    user_repository_mock.find_one = AsyncMock(return_value=user)

    open_ai_create_client_info_mock = create_autospec(OpenAiCreateClientInfo, spec_set=True, instance=True)

    service = UserService(user_repository=user_repository_mock,
                          open_ai_create_client_info=open_ai_create_client_info_mock)

    # when
    result = await service.get_user(user_id)

    # then
    assert result == rs

    user_repository_mock.find_one.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_get_users_success():
    # given
    user_id = str(uuid4())
    user = get_user_1(user_id)
    rs = get_user_rs_1(user)

    user_repository_mock = create_autospec(UserRepository, spec_set=True, instance=True)
    user_repository_mock.find_all = AsyncMock(return_value=[user, user])

    open_ai_create_client_info_mock = create_autospec(OpenAiCreateClientInfo, spec_set=True, instance=True)

    service = UserService(user_repository=user_repository_mock,
                          open_ai_create_client_info=open_ai_create_client_info_mock)

    # when
    result = await service.get_users(registered_after=None)

    # then
    assert result == [rs, rs]

    user_repository_mock.find_all.assert_awaited_once()


def get_user_1(user_id: str) -> User:
    return User(id=user_id, login="login", name="name", surname="surname", description="d",
                created_at=datetime.datetime.now(), gender="MALE", age=10)


def get_user_rs_1(user: User) -> UserRs:
    return UserRs(id=user.id, login=user.login, name=user.name, surname=user.surname, description=user.description,
                  created_at=user.created_at, gender=user.gender, age=user.age)


def get_create_client_info_rs():
    return CreateClientInfoRs(age=10, gender=Gender.MALE, name="n", surname="s", description="d")
