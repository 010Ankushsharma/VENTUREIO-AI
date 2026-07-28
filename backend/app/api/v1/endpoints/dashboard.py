"""
Dashboard data endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.deal import Deal
from app.models.analysis import Analysis

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get high-level dashboard statistics."""
    user_id = current_user["sub"]

    total_deals = (
        await db.execute(select(func.count(Deal.id)).where(Deal.created_by == user_id))
    ).scalar() or 0

    active_deals = (
        await db.execute(
            select(func.count(Deal.id)).where(
                Deal.created_by == user_id, Deal.status == "in_progress"
            )
        )
    ).scalar() or 0

    completed_deals = (
        await db.execute(
            select(func.count(Deal.id)).where(
                Deal.created_by == user_id, Deal.status == "completed"
            )
        )
    ).scalar() or 0

    avg_score = (
        await db.execute(
            select(func.avg(Deal.investment_score)).where(
                Deal.created_by == user_id, Deal.investment_score.isnot(None)
            )
        )
    ).scalar()

    return {
        "total_deals": total_deals,
        "active_deals": active_deals,
        "completed_deals": completed_deals,
        "average_investment_score": round(avg_score, 1) if avg_score else None,
    }


@router.get("/pipeline")
async def get_pipeline(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get deal pipeline grouped by status."""
    user_id = current_user["sub"]
    result = await db.execute(
        select(Deal.status, func.count(Deal.id))
        .where(Deal.created_by == user_id)
        .group_by(Deal.status)
    )
    pipeline = {row[0]: row[1] for row in result.all()}
    return {"pipeline": pipeline}
