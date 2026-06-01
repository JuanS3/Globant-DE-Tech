from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.backup_service import backup_table

router = APIRouter()


@router.post("/{table_name}")
def backup(
    table_name: str,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """
    Create an AVRO backup of the specified table.

    Parameters
    ----------
    table_name : str
        Name of the table to backup.
    db : Session
        SQLAlchemy database session provided by dependency injection.

    Returns
    -------
    dict[str, str]
        A dictionary with the table name and backup file path.

    """
    file_path = backup_table(db, table_name)
    return {"table": table_name, "backup_file": file_path}
