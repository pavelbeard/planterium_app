from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata_obj = MetaData()

users = Table(
    'users',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column
)