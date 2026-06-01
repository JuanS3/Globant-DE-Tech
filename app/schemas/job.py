from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    """
    Define the base schema for job data.

    Attributes
    ----------
    id : int
        Unique identifier for the job.
    job : str
        Title of the job position.

    """

    id: int = Field(..., gt=0)
    job: str = Field(..., min_length=1, max_length=100)


class JobCreate(JobBase):
    """
    Define the schema for creating a new job.

    """

    pass


class JobResponse(JobBase):
    """
    Define the schema for job responses.

    """

    model_config = ConfigDict(from_attributes=True)
