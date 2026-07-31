from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DealCreate(BaseModel):
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    stage: Optional[str] = None
    business_model: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    funding_ask: Optional[float] = None


class DealUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    stage: Optional[str] = None
    status: Optional[str] = None


class DealResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    industry: Optional[str]
    stage: Optional[str]
    business_model: Optional[str]
    country: Optional[str]
    website: Optional[str]
    funding_ask: Optional[float]
    status: str
    investment_score: Optional[int]
    recommendation: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DealListResponse(BaseModel):
    deals: List[DealResponse]
    total: int
