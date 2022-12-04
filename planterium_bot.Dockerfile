FROM python:3.11.0-alpine3.16

ENV API_KEY_PLANTERIUM_BOT=5741189229:AAF9nka1wLsCKLOO81ETXfu1WGG_wyg3NgU

WORKDIR /www/

COPY planterium_bot/reqs.txt .
COPY planterium_bot/app .

RUN apk --no-cache add gcc musl-dev
RUN pip install -r reqs.txt;

EXPOSE 8000/tcp

CMD ["python3.11", "main.py"]