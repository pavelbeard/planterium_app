import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse
from api.models import get_async_session, BotAdmin, Plant, Customer

router = APIRouter()


# insert into BotAdmin

@router.post("/api/add_bot_admin")
async def create_bot_admin(request: Request, session: AsyncSession = Depends(get_async_session)):
    """Создает администратора бота"""
    data = await request.json()
    user = int(data.get('user_id'))
    new_admin = BotAdmin(user_id=user)

    session.add(new_admin)
    await session.commit()

    return JSONResponse(status_code=200, content={"adding_status": "done"})


# insert into Customer

@router.post("/api/post_customer")
async def post_customer(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Загружает в базу данных информацию о покупателе\n
    :param session:
    :param request: HTTP-запрос к API
    :return: None
    """
    data = await request.json()

    with get_async_session() as session:
        new_customer = Customer(**data)
        session.add(new_customer)
        session.commit()

    logging.info(f"/api/post_customer works normally. status_code=200")

    return JSONResponse(status_code=200, content={"adding_customer_status": "done"})


# insert into Plant

@router.post("/api/post_plant")
async def post_plant(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Загружает в базу данных информацию о цветочках :)\n
    :param session:
    :param request: HTTP-запрос к API
    :return: None
    """
    data = await request.json()

    new_plants = [Plant(**d) for d in data]
    session.add_all(new_plants)
    await session.commit()

    logging.info(f"/api/post_plant works normally. status_code=200")

    return JSONResponse(status_code=200, content={"adding_plant_status": "done"})
