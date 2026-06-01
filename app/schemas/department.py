from pydantic import BaseModel, ConfigDict, Field


class DepartmentBase(BaseModel):
    """
    Define the base schema for department data.

    Attributes
    ----------
    id : int
        Unique identifier for the department.
    department : str
        Name of the department.

    """

    id: int = Field(..., gt=0)
    department: str = Field(..., min_length=1, max_length=100)


class DepartmentCreate(DepartmentBase):
    """
    Define the schema for creating a new department.

    """

    pass


class DepartmentResponse(DepartmentBase):
    """
    Define the schema for department responses.

    """

    model_config = ConfigDict(from_attributes=True)
