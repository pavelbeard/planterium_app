import os

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# global startup #
# he-he, this is data from the test database! a present database works with environment variables

DB_USERNAME = os.getenv('POSTGRES_USER', 'test_db')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'test_db*123')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '9002')
DATABASE = os.getenv('POSTGRES_DB', 'test_planterium_db')

# db+driver://username:password@host:port/database
DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def inspect_db():
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )


Base = declarative_base()

######################################################
