from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse
from api.models import get_async_session, BotAdmin

router = APIRouter()


@router.post("/api/check_admin")
async def check_admin(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Проверяет id пользователя, что он администратор
    :param session: Сессия с базой данных
    :param request: HTTP-запрос к API
    :return:
    """
    data = await request.json()
    user = int(data.get('user_id'))
    query = select(BotAdmin).where(BotAdmin.user_id == user)

    admin = [a for a in await session.execute(query)]

    status_code, value = (200, 1) if len(admin) > 0 else (403, 0)
    return JSONResponse(status_code=status_code, content={"check_admin_status": value})
