import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, Boolean, Table
from sqlalchemy.orm import relationship
from .config import Base


class BotAdmin(Base):
    __tablename__ = 'bot_admin'
    user_id = Column(BigInteger, primary_key=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(user_id={self.user_id})"


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)

    order = relationship('Order', backref='customer')

    def __getitem__(self, item):
        return item

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id!r}, ' \
               f'first_name={self.first_name!r}, last_name={self.last_name!r})'


order_plant = Table(
    'order_plant', Base.metadata,
    Column("order_id", ForeignKey("order.id"), primary_key=True),
    Column("plant_id", ForeignKey("plant.id"), primary_key=True),
)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    date_of_create = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)

    plant = relationship('Plant', secondary=order_plant)

    def __getitem__(self, item):
        return item

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, date_of_create={self.date_of_create})'


class Plant(Base):
    __tablename__ = 'plant'

    id = Column(Integer, primary_key=True)
    plant_image = Column(String(254), nullable=False)
    plant_name = Column(String(50), nullable=False)
    plant_text = Column(Text)
    with_transplant = Column(Boolean, nullable=False)
    amount = Column(Integer, default=1, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, plant_image={self.plant_image}, ' \
               f'plant_name={self.plant_name}, plant_text={self.plant_text}, ' \
               f'with_transplant={self.with_transplant}, amount={self.amount})'
