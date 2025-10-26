import logging as log
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from main.model.api.user_model import CreateUserRs, CreateUserRq, UserRs, GetAllUsersParams
from main.service.user_service import UserServiceDepends

user_router = APIRouter()


@user_router.post(
    "/create",
    response_model=CreateUserRs,
    summary="Создать пользователя",
    description="Создает пользователя и возвращает user id."
)
async def create_user(user_service: UserServiceDepends, rq: CreateUserRq) -> CreateUserRs:
    log.info(f"Поступил запрос на создание пользователя с rq_id {rq.rq_id}")
    log.debug(f"Поступил запрос на создание пользователя {rq}")
    try:
        return await user_service.create_user(rq.login, rq.created_at)
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Ошибка при создании пользователя для rq_id {rq.rq_id}: {err}")


@user_router.get(
    "/all",
    response_model=List[UserRs],
    summary="Получить список всех пользователей",
    description="""
    Возвращает список всех пользователей зарегестрированных после registeredAfter.
    Если registeredAfter не заполнено, то возвращает список всех пользователей
    """
)
async def get_users(user_service: UserServiceDepends, params: GetAllUsersParams = Depends()) -> List[UserRs]:
    log.info("Поступил запрос на получение всех пользователей")
    log.debug(f"Поступил запрос на получение всех пользователей с параметрами: {params}")
    return await user_service.get_users(params.registered_after)


@user_router.get(
    "/{user_id}",
    response_model=UserRs,
    summary="Получить пользователя по user id",
    description="Возвращает пользователя с user id."
)
async def get_user(user_service: UserServiceDepends, user_id: str) -> UserRs:
    log.info(f"Поступил запрос на получение пользователя с id {user_id}")
    try:
        return await user_service.get_user(user_id)
    except RuntimeError as err:
        raise HTTPException(status_code=404, detail=f"Ошибка при поиске пользователя с id {user_id}: {err}")
