from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class AnalysisTrigger(BaseModel):
    deal_id: str
    agent_types: Optional[list] = None  # None = run all agents


class AnalysisResponse(BaseModel):
    id: str
    deal_id: str
    agent_type: str
    status: str
    result: Optional[Dict[str, Any]]
    score: Optional[float]
    confidence: Optional[float]
    summary: Optional[str]
    evidence: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True
