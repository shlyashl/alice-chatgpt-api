FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN apt-get update  \
    && apt-get install -y --no-install-recommends

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
