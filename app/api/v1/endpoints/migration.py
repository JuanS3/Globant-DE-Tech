import os
import tempfile

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.batch import BatchResult
from app.services.csv_loader import load_csv_to_db

router = APIRouter()


@router.post("/{table_name}", response_model=BatchResult)
def migrate_csv(
    table_name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> BatchResult:
    """
    Migrate data from an uploaded CSV file into the specified table.

    Parameters
    ----------
    table_name : str
        Target table name (departments, jobs, or hired_employees).
    file : UploadFile
        The CSV file to upload.
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    BatchResult
        Result of the migration with inserted and failed counts.

    """
    suffix = ".csv"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        inserted, failed, errors = load_csv_to_db(db, tmp_path, table_name)
        return BatchResult(inserted=inserted, failed=failed, errors=errors)
    finally:
        os.remove(tmp_path)
