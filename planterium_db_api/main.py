import json
import logging
import logging.handlers
import os.path
from typing import Any

from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse, JSONResponse
from api.models import (
    Base, create_db_and_tables, get_async_session, BotAdmin,
    Customer, Order, Plant)

api = FastAPI()
headers = {"Content-Type": "application/json;charset=utf-8"}


def success_response(key: str, value: Any):
    return JSONResponse(
        status_code=200,
        headers=headers,
        content={key: value}
    )


@api.on_event("startup")
async def startup():
    log_dir = os.path.join(os.getcwd(), 'log')
    log_file = os.path.join(log_dir, 'planterium_api.log')

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logger_format = "[%(asctime)s] - [%(levelname)s] - [%(filename)s].[%(module)s]" \
                    "{%(funcName)s:%(lineno)d: %(message)s }"

    logging.getLogger(__name__)
    logging.basicConfig(filename=log_file, filemode='a', format=logger_format,
                        level=logging.INFO)
    logging.handlers.RotatingFileHandler(filename=log_file, mode='a', maxBytes=1024 ** 2, backupCount=10)

    await create_db_and_tables()


@api.get("/")
async def main():
    return {"1": "1"}


@api.get("/api/get_customer/{customer_id}")
async def get_customer(customer_id: int):
    session = get_async_session()
    query = select(Customer).where(Customer.id == customer_id)
    customer = await session.scalar(query)

    logging.info(f"/api/get_customer/{customer_id} works normally. status_code=200")

    return customer


@api.get("/api/get_order/{order_id}")
async def get_order(order_id: int):
    """
    Not implemented
    :param order_id:
    :return:
    """
    pass


@api.get("/api/get_plant/{plant_id}")
async def get_plant(plant_id: int):
    session = get_async_session()
    query = select(Plant).where(Plant.id == plant_id)
    plant = await session.scalar(query)

    logging.info(f"/api/get_plant/{plant} works normally. status_code=200")

    return plant


@api.post("/api/post_plant")
async def post_plant(request: Request):
    """
    Загружает в базу данных информацию о цветочках :)\n
    :param request: HTTP-запрос к API
    :return: None
    """
    data = await request.json()

    with get_async_session() as session:
        new_plant = Plant(**data)
        session.add(new_plant)
        session.commit()

    logging.info(f"/api/post_plant works normally. status_code=200")

    return success_response("load_plant", "done")


@api.post("/api/post_customer")
async def post_customer(request: Request):
    """
    Загружает в базу данных информацию о покупателе\n
    :param request: HTTP-запрос к API
    :return: None
    """
    data = await request.json()

    with get_async_session() as session:
        new_customer = Customer(**data)
        session.add(new_customer)
        session.commit()

    logging.info(f"/api/post_customer works normally. status_code=200")

    return success_response("load", "done")


@api.post("/api/check_admin")
async def check_admin(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Проверяет id пользователя, что он администратор
    :param session: Сессия с базой данных
    :param request: HTTP-запрос к API
    :return:
    """
    data = await request.json()
    user = int(data.get('user_id'))
    query = select(BotAdmin).where(BotAdmin.user_id == user)
    admin = [a for a in await session.execute(query)]

    return success_response("check_admin", 1) if len(admin) > 0 else JSONResponse(
        status_code=403, headers=headers, content={"check_admin": 0}
    )

