from fastapi import APIRouter, HTTPException
from src.model.api.user_model import CreateUserRs, CreateUserRq, UserRs
from typing import List

import logging as log
from src.service.user_service import UserService

user_router = APIRouter(
    tags=["user"]
)

@user_router.post("/create", response_model = CreateUserRs)
async def create_user(rq: CreateUserRq) -> CreateUserRs:
    log.info(f"Поступил запрос на создание пользователя с rqId {rq.rqId}")
    return await UserService.create_user(rq.login)

@user_router.get("/all", response_model = List[UserRs])
async def get_users() -> List[UserRs]:
    log.info("Поступил запрос на получение всех пользователей")
    return await UserService.get_users()

@user_router.get("/{user_id}", response_model = UserRs)
async def get_user(user_id: str) -> UserRs:
    log.info(f"Поступил запрос на получение пользователя с id {user_id}")
    log.debug(f"Поступил запрос на получение пользователя {user_id}")
    try:
        return await UserService.get_user(user_id)
    except RuntimeError as err:
        raise HTTPException(status_code=404, detail=f"Ошибка при поиске пользователя с id {user_id}: {err}")
