FROM python:3.12.11-alpine

RUN adduser --system --no-create-home webuser

RUN mkdir -p /home/webuser/app
WORKDIR /home/webuser/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt "psycopg[binary]==3.2.10"

COPY . .

RUN chown -R webuser /home/webuser
USER webuser
