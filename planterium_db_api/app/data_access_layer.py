from typing import List

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models


class BotAdminDAL:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_admin(self, user_id: int):
        new_admin = models.BotAdmin(user_id=user_id)
        self._db_session.add(new_admin)
        await self._db_session.flush()

    async def get_admins(self) -> List[models.BotAdmin]:
        query = select(models.BotAdmin).order_by(models.BotAdmin.user_id)
        results = await self._db_session.execute(query)
        return results.scalars().all()

    async def get_admin(self, user_id):
        query = select(models.BotAdmin).where(models.BotAdmin.user_id == user_id)
        result = await self._db_session.execute(query)
        return result.scalar()

    async def update_admin(self, user_id: int):
        query = update(models.BotAdmin).where(models.BotAdmin.user_id == user_id)
        update_query = query.values(user_id=user_id)
        update_query.execution_options(synchronize_session="fetch")
        await self._db_session.execute(update_query)

    async def delete_admin(self, user_id: int):
        query = delete(models.BotAdmin).where(models.BotAdmin.user_id == user_id)
        await self._db_session.execute(query)

