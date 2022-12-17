import datetime
import os
from typing import AsyncGenerator

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# from sqlalchemy.testing.pickleable import User

Base = declarative_base()

# global startup #
# he-he, this is data from the test database! a present database works with environment variables

DB_USERNAME = os.getenv('POSTGRES_USER', 'pavelbeard')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Rt3*YiOO')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '9002')
DATABASE = os.getenv('POSTGRES_DB', 'test_db')


engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}",
    echo=True
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

##################


# class PlatformUser(SQLAlchemyBaseUserTableUUID, Base):
#     pass


class BotAdmin(Base):
    __tablename__ = 'bot_admin'
    user_id = Column(BigInteger, primary_key=True, nullable=False)


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)

    order = relationship('Order', backref='customer')

    def __getitem__(self, item):
        return item

    def __repr__(self):
        return f'User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})'


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    date_of_create = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)

    plant = relationship('Plant', backref='order')

    def __getitem__(self, item):
        return item

    def __repr__(self):
        return f'Order(id={self.id!r}, date_of_create={self.date_of_create!r})'


class Plant(Base):
    __tablename__ = 'plant'

    id = Column(Integer, primary_key=True)
    plant_image = Column(String(254), nullable=False)
    plant_name = Column(String(50), nullable=False)
    plant_text = Column(Text)
    with_transplant = Column(Boolean, nullable=False)
    amount = Column(Integer, default=1, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'Plant({self.id=}, {self.plant_image=}, {self.plant_name=},' \
               f'{self.plant_text=}, {self.with_transplant=}, {self.amount=})'


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, PlatformUser)
