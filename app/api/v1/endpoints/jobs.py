from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobResponse

router = APIRouter()


@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)) -> list[JobResponse]:
    """
    Retrieve all jobs from the database.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    list[JobResponse]
        A list of all jobs.

    """
    from app.models.job import Job

    return db.query(Job).all()
