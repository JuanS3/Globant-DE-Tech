from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.metric import DepartmentAboveMean, QuarterHires


def _get_month_condition(dialect: str, months: tuple[int, ...]) -> str:
    """
    Return a SQL month extraction condition compatible with the dialect.

    Parameters
    ----------
    dialect : str
        Database dialect name (sqlite or postgresql).
    months : tuple[int, ...]
        Tuple of month numbers to match.

    Returns
    -------
    str
        SQL condition for month extraction.

    """
    if dialect == "sqlite":
        month_strs = ",".join(f"'{m:02d}'" for m in months)
        return f"strftime('%m', he.hire_datetime) IN ({month_strs})"
    month_strs = ",".join(str(m) for m in months)
    return f"EXTRACT(MONTH FROM he.hire_datetime) IN ({month_strs})"


def _get_year_condition(dialect: str, year: int) -> str:
    """
    Return a SQL year extraction condition compatible with the dialect.

    Parameters
    ----------
    dialect : str
        Database dialect name (sqlite or postgresql).
    year : int
        Year number to match.

    Returns
    -------
    str
        SQL condition for year extraction.

    """
    if dialect == "sqlite":
        return f"strftime('%Y', he.hire_datetime) = '{year}'"
    return f"EXTRACT(YEAR FROM he.hire_datetime) = {year}"


def get_hires_by_quarter(db: Session) -> list[QuarterHires]:
    """
    Retrieve the number of employees hired for each job and department in 2021 divided by quarter.

    Order the results alphabetically by department and job.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session.

    Returns
    -------
    list[QuarterHires]
        A list of quarterly hire metrics per department and job.

    """
    dialect = db.bind.dialect.name if db.bind else "postgresql"
    q1 = _get_month_condition(dialect, (1, 2, 3))
    q2 = _get_month_condition(dialect, (4, 5, 6))
    q3 = _get_month_condition(dialect, (7, 8, 9))
    q4 = _get_month_condition(dialect, (10, 11, 12))
    year = _get_year_condition(dialect, 2021)

    query = text(f"""
        SELECT
            d.department,
            j.job,
            SUM(CASE WHEN {q1} THEN 1 ELSE 0 END) as Q1,
            SUM(CASE WHEN {q2} THEN 1 ELSE 0 END) as Q2,
            SUM(CASE WHEN {q3} THEN 1 ELSE 0 END) as Q3,
            SUM(CASE WHEN {q4} THEN 1 ELSE 0 END) as Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE {year}
        GROUP BY d.department, j.job
        ORDER BY d.department ASC, j.job ASC
    """)
    result = db.execute(query)
    return [
        QuarterHires(
            department=row.department,
            job=row.job,
            Q1=row.Q1,
            Q2=row.Q2,
            Q3=row.Q3,
            Q4=row.Q4,
        )
        for row in result
    ]


def get_departments_above_mean(db: Session) -> list[DepartmentAboveMean]:
    """
    Retrieve departments that hired more employees than the mean in 2021.

    Order the results by the number of employees hired in descending order.

    Parameters
    ----------
    db : Session
        SQLAlchemy database session.

    Returns
    -------
    list[DepartmentAboveMean]
        A list of departments with hire counts above the 2021 mean.

    """
    dialect = db.bind.dialect.name if db.bind else "postgresql"
    year = _get_year_condition(dialect, 2021)

    query = text(f"""
        WITH department_hires AS (
            SELECT
                d.id,
                d.department,
                COUNT(he.id) as hired
            FROM departments d
            LEFT JOIN hired_employees he ON d.id = he.department_id
                AND {year}
            GROUP BY d.id, d.department
        ),
        mean_hires AS (
            SELECT AVG(hired) as mean_hired FROM department_hires
        )
        SELECT dh.id, dh.department, dh.hired
        FROM department_hires dh, mean_hires mh
        WHERE dh.hired > mh.mean_hired
        ORDER BY dh.hired DESC
    """)
    result = db.execute(query)
    return [
        DepartmentAboveMean(
            id=row.id,
            department=row.department,
            hired=row.hired,
        )
        for row in result
    ]
