from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.metric import DepartmentAboveMean, QuarterHires


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
    query = text("""
        SELECT
            d.department,
            j.job,
            SUM(CASE WHEN EXTRACT(MONTH FROM he.hire_datetime) IN (1, 2, 3) THEN 1 ELSE 0 END) as Q1,
            SUM(CASE WHEN EXTRACT(MONTH FROM he.hire_datetime) IN (4, 5, 6) THEN 1 ELSE 0 END) as Q2,
            SUM(CASE WHEN EXTRACT(MONTH FROM he.hire_datetime) IN (7, 8, 9) THEN 1 ELSE 0 END) as Q3,
            SUM(CASE WHEN EXTRACT(MONTH FROM he.hire_datetime) IN (10, 11, 12) THEN 1 ELSE 0 END) as Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE EXTRACT(YEAR FROM he.hire_datetime) = 2021
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
    query = text("""
        WITH department_hires AS (
            SELECT
                d.id,
                d.department,
                COUNT(he.id) as hired
            FROM departments d
            LEFT JOIN hired_employees he ON d.id = he.department_id
                AND EXTRACT(YEAR FROM he.hire_datetime) = 2021
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
