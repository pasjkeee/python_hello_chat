from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.params import Query

from main.model.api.user_model import CreateUserRs, CreateUserRq, UserRs
from typing import List, Optional

import logging as log
from main.service.user_service import UserService

user_router = APIRouter()


@user_router.post("/create", response_model=CreateUserRs)
async def create_user(rq: CreateUserRq) -> CreateUserRs:
    log.info(f"Поступил запрос на создание пользователя с rqId {rq.rqId}")
    return await UserService.create_user(rq.login)


@user_router.get("/all", response_model=List[UserRs])
async def get_users(
        since: Optional[datetime] = Query(None, description="Начиная с времени регистрации пользователя")
) -> List[UserRs]:
    log.info("Поступил запрос на получение всех пользователей")
    return await UserService.get_users(since)


@user_router.get("/{user_id}", response_model=UserRs)
async def get_user(user_id: str) -> UserRs:
    log.info(f"Поступил запрос на получение пользователя с id {user_id}")
    log.debug(f"Поступил запрос на получение пользователя {user_id}")
    try:
        return await UserService.get_user(user_id)
    except RuntimeError as err:
        raise HTTPException(status_code=404, detail=f"Ошибка при поиске пользователя с id {user_id}: {err}")
