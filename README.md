# Globant DE Tech API

A REST API service for the Globant Data Engineering technical challenge. This project provides endpoints for migrating CSV data to a PostgreSQL database, batch inserting records, creating AVRO backups, restoring from backups, and generating hiring metrics.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Technical Decisions](#technical-decisions)

## Requirements

- Python >= 3.12
- PostgreSQL 16 (for production)
- Docker and Docker Compose (optional)

## Installation

Clone the repository and install dependencies with `uv`:

```bash
git clone <repository-url>
cd Globant-DE-Tech
uv sync
```

## Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_DRIVER` | `postgresql` | Database driver (`sqlite` or `postgresql`) |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_USER` | `postgres` | PostgreSQL user |
| `DB_PASSWORD` | `postgres` | PostgreSQL password |
| `DB_NAME` | `globant_de` | PostgreSQL database name |
| `SQLITE_PATH` | `./data/globant_de.db` | SQLite file path (when using SQLite) |
| `DEBUG` | `false` | Enable debug mode |

## Running the Application

### Local Development

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`.

Interactive documentation (Swagger UI) is available at `http://localhost:8000/docs`.

### Docker Compose

```bash
docker-compose up --build
```

This starts both the PostgreSQL database and the application.

## API Endpoints

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Check application health |
| `GET` | `/` | Redirect to `/docs` |

### Listing Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/departments/` | List all departments |
| `GET` | `/api/v1/jobs/` | List all jobs |
| `GET` | `/api/v1/employees/` | List all employees |

### Migration

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/migration/{table_name}` | Upload a CSV file to migrate into the database |

Supported tables: `departments`, `jobs`, `hired_employees`.

### Batch Insert

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/batch/departments` | Insert a batch of departments (1-1000 rows) |
| `POST` | `/api/v1/batch/jobs` | Insert a batch of jobs (1-1000 rows) |
| `POST` | `/api/v1/batch/employees` | Insert a batch of employees (1-1000 rows) |

### Backup and Restore

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/backup/{table_name}` | Create an AVRO backup of a table |
| `POST` | `/api/v1/restore/{table_name}` | Restore a table from an AVRO backup |

### Metrics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/metrics/quarter-hires` | Hires by job and department in 2021 per quarter |
| `GET` | `/api/v1/metrics/departments-above-mean` | Departments with hires above the 2021 mean |

### Example: Batch Insert

```bash
curl -X POST "http://localhost:8000/api/v1/batch/departments" \
  -H "Content-Type: application/json" \
  -d '[{"id": 1, "department": "Engineering"}, {"id": 2, "department": "Sales"}]'
```

### Example: CSV Migration

```bash
curl -X POST "http://localhost:8000/api/v1/migration/departments" \
  -F "file=@departments.csv"
```

### Example: Backup

```bash
curl -X POST "http://localhost:8000/api/v1/backup/departments"
```

Response:
```json
{
  "table": "departments",
  "backup_file": "./backups/departments_20240115_120000.avro"
}
```

### Example: Restore

```bash
curl -X POST "http://localhost:8000/api/v1/restore/departments?file_path=./backups/departments_20240115_120000.avro"
```

## Running Tests

```bash
uv run pytest tests/ -v
```

Tests use an SQLite in-memory database for fast execution.

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/        # REST API endpoints
│   ├── core/
│   │   ├── config.py             # Application settings
│   │   └── security.py           # Rate limiting
│   ├── db/
│   │   ├── base.py               # SQLAlchemy declarative base
│   │   ├── init_db.py            # Database initialization
│   │   └── session.py            # Database engine and sessions
│   ├── models/                   # SQLAlchemy models
│   ├── schemas/                  # Pydantic schemas
│   ├── services/                 # Business logic
│   ├── utils/                    # Validators
│   └── main.py                   # FastAPI application
├── data/                         # CSV files
├── backups/                      # AVRO backups
├── tests/                        # Pytest suite
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Technical Decisions

- **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- **SQLAlchemy 2.0**: ORM with type-safe `Mapped` columns
- **Pydantic**: Request/response validation and settings management
- **PostgreSQL**: Primary database (SQLite supported for testing)
- **SlowAPI**: Rate limiting to protect API endpoints
- **Pandas**: Efficient CSV processing for migrations
- **Fastavro**: AVRO serialization for backups
- **Pytest**: Testing framework with SQLite in-memory for speed
