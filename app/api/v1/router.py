from fastapi import APIRouter

from app.api.v1.endpoints import (
    backup,
    batch,
    departments,
    employees,
    jobs,
    metrics,
    migration,
    restore,
)

api_router = APIRouter()

api_router.include_router(
    departments.router, prefix="/departments", tags=["departments"]
)
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(migration.router, prefix="/migration", tags=["migration"])
api_router.include_router(batch.router, prefix="/batch", tags=["batch"])
api_router.include_router(backup.router, prefix="/backup", tags=["backup"])
api_router.include_router(restore.router, prefix="/restore", tags=["restore"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
