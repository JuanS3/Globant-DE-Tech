import logging
from typing import Type

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.models.job import Job
from app.schemas.department import DepartmentCreate
from app.schemas.employee import EmployeeCreate
from app.schemas.job import JobCreate
from app.utils.validators import (
    validate_department_row,
    validate_employee_row,
    validate_job_row,
)

logger = logging.getLogger(__name__)

MODEL_MAP: dict[
    str, tuple[Type[Department | Job | Employee], Type[BaseModel], callable]
] = {
    "departments": (Department, DepartmentCreate, validate_department_row),
    "jobs": (Job, JobCreate, validate_job_row),
    "hired_employees": (Employee, EmployeeCreate, validate_employee_row),
}


def process_batch(
    db: Session,
    table_name: str,
    items: list[dict[str, object]],
) -> tuple[int, int, list[str]]:
    """
    Process a batch of items for insertion into the specified table.

    Validate each item before parsing and insertion. Log failures
    without stopping the batch process.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session.
    table_name : str
        Target table name (departments, jobs, or hired_employees).
    items : list[dict[str, object]]
        List of dictionaries containing row data.

    Returns
    -------
    tuple[int, int, list[str]]
        A tuple containing:
        - inserted: number of successfully inserted records
        - failed: number of records that failed validation or insertion
        - errors: list of error messages for failed records

    Raises
    ------
    ValueError
        If the table name is not supported.

    """
    if table_name not in MODEL_MAP:
        raise ValueError(f"Unknown table: {table_name}")

    model, schema, validator = MODEL_MAP[table_name]
    inserted: int = 0
    failed: int = 0
    errors: list[str] = []

    for idx, raw in enumerate(items):
        try:
            valid, error_msg = validator(raw)
            if not valid:
                failed += 1
                log_msg = f"Item {idx + 1} invalid: {error_msg}"
                logger.warning(log_msg)
                errors.append(log_msg)
                continue

            parsed = schema(**raw)
            instance = model(**parsed.model_dump())
            db.merge(instance)
            inserted += 1
        except Exception as e:
            failed += 1
            log_msg = f"Item {idx + 1} failed: {str(e)}"
            logger.error(log_msg)
            errors.append(log_msg)

    db.commit()
    return inserted, failed, errors
