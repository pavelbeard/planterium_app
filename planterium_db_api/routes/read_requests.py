import logging
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.config import async_session
from app.data_access_layer import BotAdminDAL
from app.models import Customer, Plant

router = APIRouter()


@router.get("/api/get_admins")
async def get_admins():
    try:
        async with async_session() as s:
            async with s.begin():
                bot_admin_dal = BotAdminDAL(s)
                results = await bot_admin_dal.get_admins()
                return results
    except OSError:
        return JSONResponse(status_code=503, content={"postgres_status": "unavailable"})


@router.get("/api/get_customers")
async def get_customers():
    pass


@router.get("/api/get_plants")
async def get_plants():
    pass


# detail
@router.get("/api/get_customer/{customer_id}")
async def get_customer(customer_id: int):
    pass


@router.get("/api/get_order/{order_id}")
async def get_order(order_id: int):
    """
    Not implemented
    :param order_id:
    :return:
    """
    pass


@router.get("/api/get_plant/{plant_id}")
async def get_plant(plant_id: int):
    pass
