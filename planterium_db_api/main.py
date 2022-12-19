import logging
import logging.handlers
import os
import uvicorn
from fastapi import FastAPI
from api import create_db_and_tables, exceptions, get_logger
from routes import check_requests, create_requests, read_requests

app = FastAPI()
# app.add_exception_handler(exceptions.NoDBConnectionException, )
app.include_router(check_requests.router)
app.include_router(create_requests.router)
app.include_router(read_requests.router)

headers = {"Content-Type": "application/json;charset=utf-8"}

HOST = os.getenv("DB_API_HOST", "localhost")
PORT = os.getenv("DB_API_PORT", 8001)
RELOAD = os.getenv("DB_API_ENABLE_RELOAD", True)


logger = get_logger(__name__)


@app.on_event("startup")
async def startup():
    try:
        await create_db_and_tables()
    except OSError:
        logger.error("OSError", exc_info=True)


if __name__ == '__main__':
    uvicorn.run(app="main:app", root_path=os.getcwd(), host=HOST, port=PORT, reload=RELOAD)
