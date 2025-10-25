import logging as log
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from main.model.api.user_model import CreateUserRs, CreateUserRq, UserRs, GetAllUsersParams
from main.service.user_service import UserServiceDepends

user_router = APIRouter()


@user_router.post("/create", response_model=CreateUserRs)
async def create_user(user_service: UserServiceDepends, rq: CreateUserRq) -> CreateUserRs:
    log.info(f"Поступил запрос на создание пользователя с rqId {rq.rqId}")
    log.debug(f"Поступил запрос на создание пользователя {rq}")
    return await user_service.create_user(rq.login)


@user_router.get("/all", response_model=List[UserRs])
async def get_users(user_service: UserServiceDepends, params: GetAllUsersParams = Depends()) -> List[UserRs]:
    log.info("Поступил запрос на получение всех пользователей")
    log.debug(f"Поступил запрос на получение всех пользователей с параметрами: {params}")
    return await user_service.get_users(params.registered_after)


@user_router.get("/{user_id}", response_model=UserRs)
async def get_user(user_service: UserServiceDepends, user_id: str) -> UserRs:
    log.info(f"Поступил запрос на получение пользователя с id {user_id}")
    try:
        return await user_service.get_user(user_id)
    except RuntimeError as err:
        raise HTTPException(status_code=404, detail=f"Ошибка при поиске пользователя с id {user_id}: {err}")
