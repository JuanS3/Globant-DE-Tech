from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Employee(Base):
    """
    Represent an employee hired by the organization.

    Attributes
    ----------
    id : int
        Unique identifier for the employee.
    name : str
        Full name of the employee.
    hire_datetime : datetime
        Date and time when the employee was hired.
    department_id : int
        Foreign key referencing the department.
    job_id : int
        Foreign key referencing the job.

    """

    __tablename__ = "hired_employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    hire_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("departments.id"), nullable=False
    )
    job_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("jobs.id"), nullable=False
    )
