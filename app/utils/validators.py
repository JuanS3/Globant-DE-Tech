import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def validate_department_row(row: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate a department row against data rules.

    Parameters
    ----------
    row : dict[str, Any]
        Dictionary containing department data.

    Returns
    -------
    tuple[bool, str]
        A tuple where the first element indicates if the row is valid
        and the second element contains an error message if invalid.

    """
    if not row.get("id"):
        return False, "Missing id"
    if not isinstance(row.get("id"), int) or row["id"] <= 0:
        return False, f"Invalid id: {row.get('id')}"
    if not row.get("department") or str(row["department"]).strip() == "":
        return False, "Missing department"
    return True, ""


def validate_job_row(row: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate a job row against data rules.

    Parameters
    ----------
    row : dict[str, Any]
        Dictionary containing job data.

    Returns
    -------
    tuple[bool, str]
        A tuple where the first element indicates if the row is valid
        and the second element contains an error message if invalid.

    """
    if not row.get("id"):
        return False, "Missing id"
    if not isinstance(row.get("id"), int) or row["id"] <= 0:
        return False, f"Invalid id: {row.get('id')}"
    if not row.get("job") or str(row["job"]).strip() == "":
        return False, "Missing job"
    return True, ""


def validate_employee_row(row: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate an employee row against data rules.

    Parameters
    ----------
    row : dict[str, Any]
        Dictionary containing employee data.

    Returns
    -------
    tuple[bool, str]
        A tuple where the first element indicates if the row is valid
        and the second element contains an error message if invalid.

    """
    if not row.get("id"):
        return False, "Missing id"
    if not isinstance(row.get("id"), int) or row["id"] <= 0:
        return False, f"Invalid id: {row.get('id')}"
    if not row.get("name") or str(row["name"]).strip() == "":
        return False, "Missing name"
    if not row.get("hire_datetime"):
        return False, "Missing hire_datetime"
    if not row.get("department_id"):
        return False, "Missing department_id"
    if not isinstance(row.get("department_id"), int) or row["department_id"] <= 0:
        return False, f"Invalid department_id: {row.get('department_id')}"
    if not row.get("job_id"):
        return False, "Missing job_id"
    if not isinstance(row.get("job_id"), int) or row["job_id"] <= 0:
        return False, f"Invalid job_id: {row.get('job_id')}"
    return True, ""
