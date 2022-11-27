import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)

    def __getitem__(self, item):
        return item

    def __repr__(self):
        return f'User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})'


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    date_of_create = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)

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

    # order = relationship('Order', back_populates='order')

    def __repr__(self):
        return f'Order(id={self.id!r}, date_of_create={self.date_of_create!r})'
