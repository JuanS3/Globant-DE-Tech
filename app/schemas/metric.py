from pydantic import BaseModel


class QuarterHires(BaseModel):
    """
    Define the schema for quarterly hire metrics.

    Attributes
    ----------
    department : str
        Name of the department.
    job : str
        Title of the job.
    Q1 : int
        Number of hires in the first quarter.
    Q2 : int
        Number of hires in the second quarter.
    Q3 : int
        Number of hires in the third quarter.
    Q4 : int
        Number of hires in the fourth quarter.

    """

    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int


class DepartmentAboveMean(BaseModel):
    """
    Define the schema for departments above mean hires.

    Attributes
    ----------
    id : int
        Unique identifier for the department.
    department : str
        Name of the department.
    hired : int
        Total number of employees hired.

    """

    id: int
    department: str
    hired: int
