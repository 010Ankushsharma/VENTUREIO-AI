from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ReportResponse(BaseModel):
    id: str
    deal_id: str
    report_type: str
    title: str
    content: Optional[str]
    sections: Optional[Dict[str, Any]]
    recommendation: Optional[str]
    file_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
