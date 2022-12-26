import logging

from fastapi import Depends, APIRouter
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.models import BotAdmin, Plant, Customer
from . import validation_models

from app.config import async_session
from app.data_access_layer import BotAdminDAL

router = APIRouter()


# insert into BotAdmin

@router.delete("/api/delete_admin")
async def delete_bot_admin(bot_admin: validation_models.BotAdmin):
    """Создает администратора бота"""
    try:
        new_admin = bot_admin
        async with async_session() as s:
            async with s.begin():
                bot_admin_dal = BotAdminDAL(s)
                return await bot_admin_dal.create_admin(new_admin.user_id)
    except OSError:
        return JSONResponse(status_code=503, content={"postgres_status": "unavailable."})
    except ValidationError:
        return JSONResponse(status_code=502, content={"request_status": "bad request."})


# insert into Customer

@router.post("/api/delete_customer")
async def delete_customer(request: Request):
    """
    Загружает в базу данных информацию о покупателе\n
    :param session:
    :param request: HTTP-запрос к API
    :return: None
    """
    pass


# insert into Plant

@router.post("/api/delete_plant")
async def delete_plant(request: Request):
    """
    Загружает в базу данных информацию о цветочках :)\n
    :param session:
    :param request: HTTP-запрос к API
    :return: None
    """
    pass
