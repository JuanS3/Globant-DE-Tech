from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.metric import DepartmentAboveMean, QuarterHires
from app.services.metrics_service import (
    get_departments_above_mean,
    get_hires_by_quarter,
)

router = APIRouter()


@router.get("/quarter-hires", response_model=list[QuarterHires])
def quarter_hires(
    db: Session = Depends(get_db),
) -> list[QuarterHires]:
    """
    Retrieve the number of employees hired for each job and department in 2021 divided by quarter.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    list[QuarterHires]
        A list of quarterly hire metrics.

    """
    return get_hires_by_quarter(db)


@router.get("/departments-above-mean", response_model=list[DepartmentAboveMean])
def departments_above_mean(
    db: Session = Depends(get_db),
) -> list[DepartmentAboveMean]:
    """
    Retrieve departments that hired more employees than the mean in 2021.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    list[DepartmentAboveMean]
        A list of departments above the mean hire count.

    """
    return get_departments_above_mean(db)
