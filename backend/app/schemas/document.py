from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    document_category: str
    processing_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: str
    deal_id: str
    filename: str
    file_type: str
    document_category: str
    storage_path: str
    file_size: Optional[int]
    processing_status: str
    created_at: datetime

    class Config:
        from_attributes = True
