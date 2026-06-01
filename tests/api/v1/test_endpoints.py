from datetime import datetime
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.models.job import Job


class TestHealth:
    """Test the health check endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """
        Verify the health endpoint returns ok status.

        """
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestIndex:
    """Test the root index endpoint."""

    def test_root_redirect(self, client: TestClient) -> None:
        """
        Verify the root endpoint redirects to /docs.

        """
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"


class TestDepartments:
    """Test department endpoints."""

    def test_list_departments_empty(self, client: TestClient) -> None:
        """
        Verify listing departments returns an empty list initially.

        """
        response = client.get("/api/v1/departments/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_departments(
        self, client: TestClient, db_session: Session
    ) -> None:
        """
        Verify listing departments returns created departments.

        """
        db_session.add(Department(id=1, department="Engineering"))
        db_session.commit()

        response = client.get("/api/v1/departments/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["department"] == "Engineering"


class TestJobs:
    """Test job endpoints."""

    def test_list_jobs_empty(self, client: TestClient) -> None:
        """
        Verify listing jobs returns an empty list initially.

        """
        response = client.get("/api/v1/jobs/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_jobs(self, client: TestClient, db_session: Session) -> None:
        """
        Verify listing jobs returns created jobs.

        """
        db_session.add(Job(id=1, job="Developer"))
        db_session.commit()

        response = client.get("/api/v1/jobs/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["job"] == "Developer"


class TestEmployees:
    """Test employee endpoints."""

    def test_list_employees_empty(self, client: TestClient) -> None:
        """
        Verify listing employees returns an empty list initially.

        """
        response = client.get("/api/v1/employees/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_employees(
        self, client: TestClient, db_session: Session
    ) -> None:
        """
        Verify listing employees returns created employees.

        """
        db_session.add(Department(id=1, department="Engineering"))
        db_session.add(Job(id=1, job="Developer"))
        db_session.add(
            Employee(
                id=1,
                name="John Doe",
                hire_datetime=datetime(2021, 6, 15, 10, 0, 0),
                department_id=1,
                job_id=1,
            )
        )
        db_session.commit()

        response = client.get("/api/v1/employees/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["name"] == "John Doe"


class TestBatch:
    """Test batch insert endpoints."""

    def test_batch_departments(
        self, client: TestClient, db_session: Session
    ) -> None:
        """
        Verify batch insert of departments works correctly.

        """
        payload = [
            {"id": 1, "department": "Engineering"},
            {"id": 2, "department": "Sales"},
        ]
        response = client.post("/api/v1/batch/departments", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["inserted"] == 2
        assert data["failed"] == 0
        assert data["errors"] == []

    def test_batch_departments_invalid(
        self, client: TestClient, db_session: Session
    ) -> None:
        """
        Verify batch insert returns validation error for invalid data.

        """
        payload = [
            {"id": -1, "department": ""},
        ]
        response = client.post("/api/v1/batch/departments", json=payload)
        assert response.status_code == 422


class TestMigration:
    """Test CSV migration endpoint."""

    def test_migration_csv(self, client: TestClient) -> None:
        """
        Verify CSV migration endpoint accepts file uploads.

        """
        csv_content = b"1,Engineering\n2,Sales\n"
        file = BytesIO(csv_content)
        response = client.post(
            "/api/v1/migration/departments",
            files={"file": ("departments.csv", file, "text/csv")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["inserted"] == 2
        assert data["failed"] == 0

    def test_migration_empty_csv(self, client: TestClient) -> None:
        """
        Verify CSV migration endpoint handles empty files gracefully.

        """
        file = BytesIO(b"")
        response = client.post(
            "/api/v1/migration/departments",
            files={"file": ("empty.csv", file, "text/csv")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["inserted"] == 0
        assert data["failed"] == 0
        assert "Empty CSV file" in data["errors"][0]


class TestBackupRestore:
    """Test backup and restore endpoints."""

    def test_backup_and_restore(
        self, client: TestClient, db_session: Session
    ) -> None:
        """
        Verify backup creation and restoration cycle.

        """
        db_session.add(Department(id=1, department="Engineering"))
        db_session.commit()

        response = client.post("/api/v1/backup/departments")
        assert response.status_code == 200
        data = response.json()
        assert "backup_file" in data

        file_path = data["backup_file"]
        response = client.post(
            "/api/v1/restore/departments",
            params={"file_path": file_path},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["inserted"] == 1


class TestMetrics:
    """Test metrics endpoints."""

    def test_quarter_hires(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Verify the quarter hires endpoint returns metrics.

        """
        def mock_get_hires_by_quarter(db):
            from app.schemas.metric import QuarterHires

            return [
                QuarterHires(
                    department="Engineering",
                    job="Developer",
                    Q1=1,
                    Q2=2,
                    Q3=3,
                    Q4=4,
                )
            ]

        monkeypatch.setattr(
            "app.api.v1.endpoints.metrics.get_hires_by_quarter",
            mock_get_hires_by_quarter,
        )

        response = client.get("/api/v1/metrics/quarter-hires")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["department"] == "Engineering"
        assert data[0]["Q1"] == 1

    def test_departments_above_mean(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Verify the departments above mean endpoint returns metrics.

        """
        def mock_get_departments_above_mean(db):
            from app.schemas.metric import DepartmentAboveMean

            return [DepartmentAboveMean(id=1, department="Engineering", hired=10)]

        monkeypatch.setattr(
            "app.api.v1.endpoints.metrics.get_departments_above_mean",
            mock_get_departments_above_mean,
        )

        response = client.get("/api/v1/metrics/departments-above-mean")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["department"] == "Engineering"
        assert data[0]["hired"] == 10
