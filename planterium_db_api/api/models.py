from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, Text, Boolean, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base = declarative_base()
#
#
# class Customer(Base):
#     __tablename__ = 'customer'
#
#     id = Column(Integer(), primary_key=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     email = Column(String(50), nullable=False)
#
#     def __repr__(self):
#         return f"CustomerTest {self.id}"
#
#
# class Order(Base):
#     __tablename__ = 'order'
#
#     id = Column(Integer(), primary_key=True, autoincrement=True)
#     create_on = Column(datetime, nullable=False)
#     customer_id = Column(Integer(), ForeignKey('customer.id', ondelete='cascade'), nullable=False)
#
#     def __repr__(self):
#         return f"OrderTest {self.id}"
#
#
# class OrderPlant(Base):
#     __tablename__ = 'order_plant'
#     id = Column(Integer(), primary_key=True)
#     order_id = Column(Integer(), ForeignKey('order.id', ondelete='cascade'), nullable=False)
#     plant_id = Column(Integer(), ForeignKey('plant.id', ondelete='cascade'), nullable=False)
#
#     def __repr__(self):
#         return f"OrderPlantTest {self.id}"


class Plant(BaseModel):
    id: int
    plant_image: bytes
    plant_title: str
    plant_text: str
    with_transplant: bool

    # __tablename__ = 'plant'
    #
    # id = Column(Integer(), primary_key=True)

    # plant_image = Column(BLOB(), nullable=False)
    # plant_title = Column(String(50), nullable=False)
    # plant_text = Column(Text(256), nullable=False)
    # with_transplant = Column(Boolean(), nullable=False)
    #
    # def __repr__(self):
    #     return f"PlantTest {self.id}"
