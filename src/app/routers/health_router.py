from fastapi import APIRouter
from fastapi.requests import Request

router = APIRouter(tags=['health_check'])


@router.get("/ping/")
async def health_check():
    """Простая проверка работоспособности веб-приложения"""
    return {"message": "pong"}
