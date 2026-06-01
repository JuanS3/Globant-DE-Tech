import logging
from pathlib import Path

import fastavro
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.models.job import Job
from app.utils.validators import (
    validate_department_row,
    validate_employee_row,
    validate_job_row,
)

logger = logging.getLogger(__name__)

MODEL_MAP: dict[str, tuple[type[Department | Job | Employee], callable]] = {
    "departments": (Department, validate_department_row),
    "jobs": (Job, validate_job_row),
    "hired_employees": (Employee, validate_employee_row),
}


def restore_table(
    db: Session,
    table_name: str,
    file_path: str,
) -> tuple[int, int, list[str]]:
    """
    Restore a database table from an AVRO backup file.

    Validate each record before insertion and log failures without
    stopping the restore process.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session.
    table_name : str
        Name of the table to restore (departments, jobs, or hired_employees).
    file_path : str
        Path to the AVRO backup file.

    Returns
    -------
    tuple[int, int, list[str]]
        A tuple containing:
        - inserted: number of successfully restored records
        - failed: number of records that failed validation or insertion
        - errors: list of error messages for failed records

    Raises
    ------
    ValueError
        If the table name is not supported.
    FileNotFoundError
        If the specified backup file does not exist.

    """
    if table_name not in MODEL_MAP:
        raise ValueError(f"Unknown table: {table_name}")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Backup file not found: {file_path}")

    model, validator = MODEL_MAP[table_name]
    inserted: int = 0
    failed: int = 0
    errors: list[str] = []

    with open(path, "rb") as f:
        reader = fastavro.reader(f)
        for idx, record in enumerate(reader):
            try:
                valid, error_msg = validator(record)
                if not valid:
                    failed += 1
                    log_msg = f"Record {idx + 1} invalid: {error_msg}"
                    logger.warning(log_msg)
                    errors.append(log_msg)
                    continue

                instance = model(**record)
                db.merge(instance)
                inserted += 1
            except Exception as e:
                failed += 1
                log_msg = f"Record {idx + 1} failed: {str(e)}"
                logger.error(log_msg)
                errors.append(log_msg)

    db.commit()
    logger.info(f"Restored {inserted} rows into {table_name}")
    return inserted, failed, errors
