import logging
import logging.handlers
import os
import uvicorn
from fastapi import FastAPI
from app import exceptions, get_logger, engine, Base, create_async_engine
from routes import check_requests, create_requests, read_requests, delete_requests

app = FastAPI()
# app.add_exception_handler(exceptions.NoDBConnectionException, )
app.include_router(check_requests.router)
app.include_router(create_requests.router)
app.include_router(read_requests.router)
app.include_router(delete_requests.router)

headers = {"Content-Type": "application/json;charset=utf-8"}

HOST = os.getenv("DB_API_HOST", "localhost")
PORT = os.getenv("DB_API_PORT", 8001)
RELOAD = os.getenv("DB_API_ENABLE_RELOAD", True)

logger = get_logger(__name__)


@app.get("/api/main")
async def main():
    return {"1": "1"}


if __name__ == '__main__':
    uvicorn.run(app="main:app", root_path=os.getcwd(), host=HOST, port=PORT, reload=RELOAD)
