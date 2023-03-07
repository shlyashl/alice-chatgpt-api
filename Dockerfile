FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
