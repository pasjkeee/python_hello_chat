from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query

from main.model.api.user_model import CreateUserRs, CreateUserRq, UserRs, GetAllUsersParams
from typing import List, Optional

import logging as log
from main.service.user_service import UserService

user_router = APIRouter()


@user_router.post("/create", response_model=CreateUserRs)
async def create_user(rq: CreateUserRq) -> CreateUserRs:
    log.info(f"Поступил запрос на создание пользователя с rqId {rq.rqId}")
    log.debug(f"Поступил запрос на создание пользователя {rq}")
    return await UserService.create_user(rq.login)


@user_router.get("/all", response_model=List[UserRs])
async def get_users(params: GetAllUsersParams = Depends()) -> List[UserRs]:
    log.info("Поступил запрос на получение всех пользователей")
    log.debug(f"Поступил запрос на получение всех пользователей с параметрами: {params}")
    return await UserService.get_users(params.registered_after)


@user_router.get("/{user_id}", response_model=UserRs)
async def get_user(user_id: str) -> UserRs:
    log.info(f"Поступил запрос на получение пользователя с id {user_id}")
    try:
        return await UserService.get_user(user_id)
    except RuntimeError as err:
        raise HTTPException(status_code=404, detail=f"Ошибка при поиске пользователя с id {user_id}: {err}")
