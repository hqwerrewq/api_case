FROM python:3.12-slim as base


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        curl \
        build-essential \
        libffi-dev \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*


RUN curl -sSL https://install.python-poetry.org | python3 && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry


ENV PYTHONPATH=/app/src
WORKDIR /app


COPY pyproject.toml poetry.lock ./


RUN poetry --version


RUN poetry install --no-interaction --no-ansi --with dev

COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
