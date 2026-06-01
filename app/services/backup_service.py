import logging
from datetime import datetime
from pathlib import Path

import fastavro
from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

BACKUP_DIR = Path("./backups")

AVRO_SCHEMAS: dict[str, dict] = {
    "departments": {
        "type": "record",
        "name": "Department",
        "fields": [
            {"name": "id", "type": "long"},
            {"name": "department", "type": "string"},
        ],
    },
    "jobs": {
        "type": "record",
        "name": "Job",
        "fields": [
            {"name": "id", "type": "long"},
            {"name": "job", "type": "string"},
        ],
    },
    "hired_employees": {
        "type": "record",
        "name": "Employee",
        "fields": [
            {"name": "id", "type": "long"},
            {"name": "name", "type": "string"},
            {"name": "hire_datetime", "type": "string"},
            {"name": "department_id", "type": "long"},
            {"name": "job_id", "type": "long"},
        ],
    },
}


def backup_table(db: Session, table_name: str) -> str:
    """
    Create an AVRO backup of the specified database table.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session.
    table_name : str
        Name of the table to backup (departments, jobs, or hired_employees).

    Returns
    -------
    str
        Path to the generated AVRO backup file.

    Raises
    ------
    ValueError
        If the table name is not supported.

    """
    if table_name not in AVRO_SCHEMAS:
        raise ValueError(f"Unknown table: {table_name}")

    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path: Path = BACKUP_DIR / f"{table_name}_{timestamp}.avro"

    result = db.execute(text(f"SELECT * FROM {table_name}"))
    rows: list[dict] = [dict(row._mapping) for row in result]

    for row in rows:
        if "hire_datetime" in row and row["hire_datetime"] is not None:
            row["hire_datetime"] = str(row["hire_datetime"])

    schema = fastavro.parse_schema(AVRO_SCHEMAS[table_name])
    with open(file_path, "wb") as f:
        fastavro.writer(f, schema, rows)

    logger.info(f"Backup created: {file_path}")
    return str(file_path)
