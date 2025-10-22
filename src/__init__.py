from fastapi import FastAPI
from src.router.user_router import user_router

app = FastAPI()

app.include_router(user_router, prefix="/user")