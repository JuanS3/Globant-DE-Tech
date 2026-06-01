# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

WORKDIR /app

# Build dependencies required to compile native extensions (e.g. asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install uv and create a virtual environment
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv venv /app/.venv && \
    uv pip install --no-cache --python /app/.venv/bin/python -r pyproject.toml

# ------------------------------------------------------------------
# Runtime stage
# ------------------------------------------------------------------
FROM python:3.12-slim

WORKDIR /app

# Runtime library for PostgreSQL (much smaller than -dev package)
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Application code
COPY app/ ./app/
COPY main.py ./

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
