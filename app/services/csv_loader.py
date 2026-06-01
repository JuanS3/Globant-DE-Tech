import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
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


def _clean_row(row: pd.Series) -> Dict[str, Any]:
    """
    Clean and normalize a pandas Series row for validation.

    Parameters
    ----------
    row : pd.Series
        A row from a pandas DataFrame.

    Returns
    -------
    dict[str, Any]
        A dictionary with cleaned values and proper types.

    """
    cleaned = {}
    for key, value in row.items():
        if pd.isna(value):
            cleaned[key] = None
        elif key == "id" or key.endswith("_id"):
            try:
                cleaned[key] = int(value)
            except (ValueError, TypeError):
                cleaned[key] = value
        else:
            cleaned[key] = value
    return cleaned


def load_csv_to_db(
    db: Session, file_path: str, table_name: str
) -> Tuple[int, int, List[str]]:
    """
    Load data from a CSV file into the specified database table.

    Validate each row before insertion and log failures without
    stopping the batch process.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session.
    file_path : str
        Path to the CSV file.
    table_name : str
        Target table name (departments, jobs, or hired_employees).

    Returns
    -------
    tuple[int, int, list[str]]
        A tuple containing:
        - inserted: number of successfully inserted rows
        - failed: number of rows that failed validation or insertion
        - errors: list of error messages for failed rows

    Raises
    ------
    FileNotFoundError
        If the specified CSV file does not exist.
    ValueError
        If the table name is not supported.

    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path, header=None)

    if table_name == "departments":
        df.columns = ["id", "department"]
        model = Department
        validator = validate_department_row
    elif table_name == "jobs":
        df.columns = ["id", "job"]
        model = Job
        validator = validate_job_row
    elif table_name == "hired_employees":
        df.columns = ["id", "name", "hire_datetime", "department_id", "job_id"]
        model = Employee
        validator = validate_employee_row
    else:
        raise ValueError(f"Unknown table: {table_name}")

    inserted = 0
    failed = 0
    errors: List[str] = []

    for idx, row in df.iterrows():
        cleaned = _clean_row(row)
        valid, error_msg = validator(cleaned)
        if not valid:
            failed += 1
            log_msg = f"Row {idx + 1} invalid for {table_name}: {error_msg}"
            logger.warning(log_msg)
            errors.append(log_msg)
            continue

        try:
            instance = model(**cleaned)
            db.merge(instance)
            inserted += 1
        except Exception as e:
            failed += 1
            log_msg = f"Row {idx + 1} failed insert for {table_name}: {str(e)}"
            logger.error(log_msg)
            errors.append(log_msg)

    db.commit()
    return inserted, failed, errors
