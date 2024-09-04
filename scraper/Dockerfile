FROM python:3.11

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry
RUN poetry install

COPY . .

CMD poetry run python -m app.main