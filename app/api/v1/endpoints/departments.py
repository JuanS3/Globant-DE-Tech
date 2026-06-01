from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.department import DepartmentResponse

router = APIRouter()


@router.get("/", response_model=list[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)) -> list[DepartmentResponse]:
    """
    Retrieve all departments from the database.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    list[DepartmentResponse]
        A list of all departments.

    """
    from app.models.department import Department

    return db.query(Department).all()
