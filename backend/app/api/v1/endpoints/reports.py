"""
Report generation and retrieval endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.report import Report
from app.schemas.report import ReportResponse
from app.services.report_generator import generate_due_diligence_report

router = APIRouter()


@router.post("/generate/{deal_id}", status_code=202)
async def generate_report(
    deal_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Generate a full due diligence report for a deal."""
    background_tasks.add_task(generate_due_diligence_report, deal_id)
    return {"message": "Report generation started", "deal_id": deal_id}


@router.get("/deal/{deal_id}", response_model=list[ReportResponse])
async def list_reports(
    deal_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(Report).where(Report.deal_id == deal_id).order_by(Report.created_at.desc())
    )
    reports = result.scalars().all()
    return [ReportResponse.model_validate(r) for r in reports]
