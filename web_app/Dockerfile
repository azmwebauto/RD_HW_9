FROM python:3.11

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry
RUN poetry install

COPY . .

RUN alembic upgrade heads