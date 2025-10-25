from fastapi import FastAPI

from main.router.user_router import user_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
