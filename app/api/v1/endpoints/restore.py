from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.batch import BatchResult
from app.services.restore_service import restore_table

router = APIRouter()


@router.post("/{table_name}", response_model=BatchResult)
def restore(
    table_name: str,
    file_path: str,
    db: Session = Depends(get_db),
) -> BatchResult:
    """
    Restore a table from an AVRO backup file.

    Parameters
    ----------
    table_name : str
        Name of the table to restore.
    file_path : str
        Path to the AVRO backup file.
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    BatchResult
        Result of the restore operation with inserted and failed counts.

    """
    inserted, failed, errors = restore_table(db, table_name, file_path)
    return BatchResult(inserted=inserted, failed=failed, errors=errors)
