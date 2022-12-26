from typing import Callable
from fastapi.routing import APIRoute, APIRouter
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

router = APIRouter()


class NoDBConnectionException(OSError):
    def __init__(self, message: str):
        self.message = message


# TODO: Обернуть sessionmaker в обработку исключений базы данных

class NoDatabaseConnection(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except OSError:
                return JSONResponse(status_code=503, content={"postgresql_status": "postgresql service not available!"})

        return custom_route_handler
