from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Job(Base):
    """
    Represent a job position in the organization.

    Attributes
    ----------
    id : int
        Unique identifier for the job.
    job : str
        Title of the job position.

    """

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job: Mapped[str] = mapped_column(String(100), nullable=False)
