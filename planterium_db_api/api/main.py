import os
import databases

from fastapi import FastAPI
from sqlalchemy import (
    MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, ForeignKey,
    create_engine
)
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.sql import select
# from sqlalchemy_imageattach.entity import Image, image_attachment

# create schema
DATABASE_URL = 'sqlite:///database.db'
# DATABASE_URL = 'postgresql+psycopg2://test_admin:Rt3$YiOO@localhost:49153/test_db'

metadata = MetaData()
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)
# ############ #

# customer
customer = Table(
    'customer', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False)
)
# ############ #

# order
order = Table(
    'order', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('date_of_create', DateTime, nullable=False),
    Column('customer_id', None, ForeignKey('customer.id', ondelete='cascade'), nullable=False)
)
# ############ #

# plant
plant = Table(
    'plant', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('plant_image', BLOB, nullable=False),
    Column('plant_title', String, nullable=False),
    Column('plant_text', Text, nullable=False),
    Column('with_transplant', Boolean, nullable=False)
)
# ############ #

# order_plant
order_plant = Table(
    'order_plant', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('order_id', None, ForeignKey('order.id', ondelete='cascade'), nullable=False),
    Column('plant_id', None, ForeignKey('plant.id', ondelete='cascade'), nullable=False),
)
# ############ #

metadata.create_all(engine)

# ############ #

api = FastAPI()


@api.on_event('startup')
async def startup():
    await database.connect()

@api.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@api.get('/')
async def main():
    return {'hello': 'world'}


@api.get('/get_plants/{plant_id}')
async def get_plant(plant_id: int):
    query = select(plant.c.plant_image).where(plant.c.id == plant_id)


    return await database.fetch_one(query)

    # re =
    # result = {k: v for k, v in zip(plant.c, tmp)}

    # return Response([x for x in x for x in x][0], media_type='image/jpg')

@api.get('/get_plants/data/{plant_id}')
async def get_plant(plant_id: int):
    query = select(
        plant.c.id, plant.c.plant_title, plant.c.plant_text,
        plant.c.with_transplant
    ).where(plant.c.id == plant_id)
    return await database.fetch_one(query)


# fill database method
@api.get('/fill_db')
async def fill_database():
    path = os.path.join('D:\\', 'sobes_projects', 'planterium_db_api', 't')
    pics = os.listdir(path)

    for pic, num in zip(pics, range(len(pics))):
        with open(os.path.join(path, pic), 'rb', encoding='utf-8') as p:
            image = p.read()

        plant_query = plant.insert()
        await database.execute(
            plant_query,
            {'plant_image': image, 'plant_title': f'Test_pic {num}',
             'plant_text': f'Test text {num}', 'with_transplant': False}
        )

    return {'done': 'done!'}
