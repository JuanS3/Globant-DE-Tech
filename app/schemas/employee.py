from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    """
    Define the base schema for employee data.

    Attributes
    ----------
    id : int
        Unique identifier for the employee.
    name : str
        Full name of the employee.
    hire_datetime : datetime
        Date and time when the employee was hired.
    department_id : int
        Identifier of the department.
    job_id : int
        Identifier of the job.

    """

    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=200)
    hire_datetime: datetime
    department_id: int = Field(..., gt=0)
    job_id: int = Field(..., gt=0)


class EmployeeCreate(EmployeeBase):
    """
    Define the schema for creating a new employee.

    """

    pass


class EmployeeResponse(EmployeeBase):
    """
    Define the schema for employee responses.

    """

    model_config = ConfigDict(from_attributes=True)
