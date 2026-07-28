"""
Deal CRUD endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.deal import Deal
from app.schemas.deal import DealCreate, DealUpdate, DealResponse, DealListResponse

router = APIRouter()


@router.post("/", response_model=DealResponse, status_code=201)
async def create_deal(
    payload: DealCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    deal = Deal(**payload.model_dump(), created_by=current_user["sub"])
    db.add(deal)
    await db.flush()
    await db.refresh(deal)
    return DealResponse.model_validate(deal)


@router.get("/", response_model=DealListResponse)
async def list_deals(
    status: Optional[str] = None,
    industry: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = select(Deal).where(Deal.created_by == current_user["sub"])
    if status:
        query = query.where(Deal.status == status)
    if industry:
        query = query.where(Deal.industry == industry)

    total_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(total_q)).scalar() or 0

    result = await db.execute(query.offset(skip).limit(limit).order_by(Deal.created_at.desc()))
    deals = result.scalars().all()

    return DealListResponse(
        deals=[DealResponse.model_validate(d) for d in deals],
        total=total,
    )


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return DealResponse.model_validate(deal)


@router.patch("/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: str,
    payload: DealUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(deal, key, value)
    await db.flush()
    await db.refresh(deal)
    return DealResponse.model_validate(deal)


@router.delete("/{deal_id}", status_code=204)
async def delete_deal(
    deal_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    await db.delete(deal)
