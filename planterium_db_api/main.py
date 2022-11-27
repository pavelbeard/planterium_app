import json
import logging
import logging.handlers
import os.path

from fastapi import FastAPI, Request, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse, JSONResponse

from api.models import Base, Customer, Order, Plant

### global startup ###
api = FastAPI()
# he-he, this is data from the test database! a present database works with environment variables
engine = create_engine("postgresql+psycopg2://pavelbeard:\"Rt3%YiOO\"@localhost:8001/test_db", echo=True)
Base.metadata.create_all(engine)
#####################


@api.on_event("startup")
async def startup():
    log_dir = os.path.join(os.getcwd(), 'log')
    log_file = os.path.join(log_dir, 'planterium_api.log')

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    format = "[%(asctime)s] - [%(levelname)s] - [%(filename)s].[%(module)s]" \
             "{%(funcName)s:%(lineno)d: %(message)s }"

    logging.getLogger(__name__)
    logging.basicConfig(filename=log_file, filemode='a', format=format,
                        level=logging.INFO)
    logging.handlers.RotatingFileHandler(filename=log_file, mode='a', maxBytes=1024 ** 2, backupCount=10)


@api.get("/")
async def main():
    return {"1": "1"}


@api.get("/api/get_customer/{customer_id}")
async def get_customer(customer_id: int):
    session = Session(engine)
    query = select(Customer).where(Customer.id == customer_id)
    customer = session.scalar(query)

    logging.info(f"/api/get_customer/{customer_id} works normally")

    return customer


@api.get("/api/get_order/{order_id}")
async def get_order(order_id: int):
    """
    Not implemented
    :param order_id:
    :return:
    """
    pass


@api.post("/api/post_plant")
async def post_plant(request: Request):
    """
    Загружает в базу данных информацию о цветочках :)\n
    :param request: HTTP-запрос к API
    :return: None
    """
    data = await request.json()

    with Session(engine) as session:
        new_plant = Plant(**data)
        session.add(new_plant)
        session.commit()

    logging.info(f"/api/post_plant works normally. status_code=200")

    return {"load_plant": "done"}


@api.post("/api/post_customer")
async def post_customer(request: Request):
    """
    Загружает в базу данных информацию о покупателе\n
    :param request: HTTP-запрос к API
    :return: None
    """
    data = await request.json()

    with Session(engine) as session:
        new_customer = Customer(**data)
        session.add(new_customer)
        session.commit()

    logging.info(f"/api/post_customer works normally")

    return {"load": "done"}
