from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class BatchRequest(BaseModel, Generic[T]):
    """
    Define the schema for batch request payloads.

    Attributes
    ----------
    items : list[T]
        List of items to process in the batch.

    """

    items: List[T] = Field(..., min_length=1, max_length=1000)


class BatchResult(BaseModel):
    """
    Define the schema for batch operation results.

    Attributes
    ----------
    inserted : int
        Number of successfully inserted records.
    failed : int
        Number of records that failed validation or insertion.
    errors : list[str]
        List of error messages for failed records.

    """

    inserted: int
    failed: int
    errors: List[str]
