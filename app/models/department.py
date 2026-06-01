from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Department(Base):
    """
    Represent a department in the organization.

    Attributes
    ----------
    id : int
        Unique identifier for the department.
    department : str
        Name of the department.

    """

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
