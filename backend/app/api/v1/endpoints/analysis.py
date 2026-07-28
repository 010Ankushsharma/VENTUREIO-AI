"""
Analysis trigger and retrieval endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.analysis import Analysis
from app.models.deal import Deal
from app.schemas.analysis import AnalysisTrigger, AnalysisResponse
from app.services.analysis_orchestrator import run_due_diligence

router = APIRouter()

ALL_AGENTS = [
    "startup_understanding",
    "financial",
    "market_intelligence",
    "competitive_intelligence",
    "risk_assessment",
    "fraud_detection",
    "valuation",
    "investment_recommendation",
]


@router.post("/trigger", status_code=202)
async def trigger_analysis(
    payload: AnalysisTrigger,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Trigger AI due diligence analysis for a deal."""
    result = await db.execute(select(Deal).where(Deal.id == payload.deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    agent_types = payload.agent_types or ALL_AGENTS

    # Create pending analysis records
    analysis_ids = []
    for agent_type in agent_types:
        analysis = Analysis(deal_id=payload.deal_id, agent_type=agent_type, status="pending")
        db.add(analysis)
        await db.flush()
        await db.refresh(analysis)
        analysis_ids.append(analysis.id)

    # Update deal status
    deal.status = "in_progress"
    await db.flush()

    # Run analysis in background
    background_tasks.add_task(run_due_diligence, payload.deal_id, agent_types)

    return {"message": "Analysis triggered", "deal_id": payload.deal_id, "analysis_ids": analysis_ids}


@router.get("/deal/{deal_id}", response_model=list[AnalysisResponse])
async def get_analyses(
    deal_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(Analysis).where(Analysis.deal_id == deal_id).order_by(Analysis.created_at)
    )
    analyses = result.scalars().all()
    return [AnalysisResponse.model_validate(a) for a in analyses]


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisResponse.model_validate(analysis)
