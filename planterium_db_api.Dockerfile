FROM python:3.11.0-alpine3.16

WORKDIR /api

COPY planterium_db_api/reqs.txt /api/reqs.txt

RUN pip install --no-cache-dir --upgrade -r reqs.txt;

EXPOSE 8003/tcp

CMD ["uvicorn", "main:api", "--reload", "--host", "0.0.0.0", "--port", "8003"]