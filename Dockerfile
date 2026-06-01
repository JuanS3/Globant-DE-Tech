FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir uvicorn fastapi sqlalchemy pydantic pydantic-settings slowapi pandas fastavro python-multipart aiosqlite asyncpg psycopg2-binary

COPY app/ ./app/
COPY main.py ./

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
