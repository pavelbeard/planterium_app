FROM python:3.11.1-alpine3.16 as builder

WORKDIR /builder

COPY planterium_bot_assemble_files/reqs.txt .
RUN mkdir -p /builder/wheels;  \
    apk add gcc musl-dev; \
    pip3.11 wheel \
    --no-cache-dir \
    --no-deps \
    --wheel-dir /builder/wheels -r reqs.txt

FROM python:3.11.0-alpine3.16

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /builder/wheels /wheels
RUN pip install --no-cache /wheels/*; rm -rf /wheels

WORKDIR /www/app

COPY app .

CMD ["python3.11", "main.py"]