import logging
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import get_async_session, Customer, Plant

router = APIRouter()


@router.get("/api/get_customers")
async def get_customers(session: AsyncSession = Depends(get_async_session)):
    query = select(Customer)
    customers = await session.execute(query)

    return customers


@router.get("/api/get_plants")
async def get_plants(session: AsyncSession = Depends(get_async_session)):
    query = select(Plant)
    plants = await session.execute(query)

    return plants


# detail
@router.get("/api/get_customer/{customer_id}")
async def get_customer(customer_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Customer).where(Customer.id == customer_id)
    customer = await session.execute(query)

    logging.info(f"/api/get_customer/{customer_id} works normally. status_code=200")

    return customer


@router.get("/api/get_order/{order_id}")
async def get_order(order_id: int):
    """
    Not implemented
    :param order_id:
    :return:
    """
    pass


@router.get("/api/get_plant/{plant_id}")
async def get_plant(plant_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Plant).where(Plant.id == plant_id)
    plant = await session.scalar(query)

    logging.info(f"/api/get_plant/{plant} works normally. status_code=200")

    return plant
