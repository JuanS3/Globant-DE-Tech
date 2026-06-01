from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.employee import EmployeeResponse

router = APIRouter()


@router.get("/", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)) -> list[EmployeeResponse]:
    """
    Retrieve all employees from the database.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    list[EmployeeResponse]
        A list of all employees.

    """
    from app.models.employee import Employee

    return db.query(Employee).all()
