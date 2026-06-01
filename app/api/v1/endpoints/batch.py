from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.batch import BatchResult
from app.schemas.department import DepartmentCreate
from app.schemas.employee import EmployeeCreate
from app.schemas.job import JobCreate
from app.services.batch_processor import process_batch

router = APIRouter()


@router.post("/departments", response_model=BatchResult)
def batch_departments(
    items: list[DepartmentCreate],
    db: Session = Depends(get_db),
) -> BatchResult:
    """
    Insert a batch of departments.

    Parameters
    ----------
    items : list[DepartmentCreate]
        List of departments to insert.
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    BatchResult
        Result of the batch operation with inserted and failed counts.

    """
    raw = [item.model_dump() for item in items]
    inserted, failed, errors = process_batch(db, "departments", raw)
    return BatchResult(inserted=inserted, failed=failed, errors=errors)


@router.post("/jobs", response_model=BatchResult)
def batch_jobs(
    items: list[JobCreate],
    db: Session = Depends(get_db),
) -> BatchResult:
    """
    Insert a batch of jobs.

    Parameters
    ----------
    items : list[JobCreate]
        List of jobs to insert.
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    BatchResult
        Result of the batch operation with inserted and failed counts.

    """
    raw = [item.model_dump() for item in items]
    inserted, failed, errors = process_batch(db, "jobs", raw)
    return BatchResult(inserted=inserted, failed=failed, errors=errors)


@router.post("/employees", response_model=BatchResult)
def batch_employees(
    items: list[EmployeeCreate],
    db: Session = Depends(get_db),
) -> BatchResult:
    """
    Insert a batch of employees.

    Parameters
    ----------
    items : list[EmployeeCreate]
        List of employees to insert.
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    BatchResult
        Result of the batch operation with inserted and failed counts.

    """
    raw = [item.model_dump() for item in items]
    inserted, failed, errors = process_batch(db, "hired_employees", raw)
    return BatchResult(inserted=inserted, failed=failed, errors=errors)
