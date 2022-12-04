import os.path

from sqlalchemy import (
    MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BLOB, ForeignKey,
    create_engine,
)
from sqlalchemy.sql import select


class Schema:
    __metadata = MetaData()
    __DATABASE_URL = 'sqlite:///../sqlite3.db?check_same_thread=False'

    def create_schema(self):
        self.customer = Table(
            'customer', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
            Column('first_name', String, nullable=False),
            Column('last_name', String, nullable=False),
            Column('email', String, nullable=False)
        )

        self.order = Table(
            'order', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
            Column('date_of_create', DateTime, nullable=False),
            Column('customer_id', None, ForeignKey('customer.id', ondelete='cascade'), nullable=False)
        )

        self.plant = Table(
            'plant', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
            Column('plant_image', BLOB, nullable=False),
            Column('plant_title', String, nullable=False),
            Column('plant_text', Text, nullable=False),
            Column('with_transplant', Boolean, nullable=False)
        )

        self.order_plant = Table(
            'order_plant', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
            Column('order_id', None, ForeignKey('order.id', ondelete='cascade'), nullable=False),
            Column('plant_id', None, ForeignKey('plant.id', ondelete='cascade'), nullable=False),
        )

        self.engine = create_engine(self.__DATABASE_URL, echo=True)
        self.__metadata.create_all(self.engine)
