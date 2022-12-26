from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.models import BotAdmin
from . import validation_models

router = APIRouter()


@router.post("/api/check_admin")
async def check_admin(bot_admin: validation_models.BotAdmin):
    """
    Проверяет id пользователя, что он администратор
    :param request: HTTP-запрос к API
    :return:
    """
    pass
