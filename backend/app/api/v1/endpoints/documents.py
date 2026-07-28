"""
Document upload and management endpoints.
"""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.document import Document
from app.schemas.document import DocumentUploadResponse, DocumentResponse

router = APIRouter()

UPLOAD_DIR = "/app/uploads"


@router.post("/upload/{deal_id}", response_model=DocumentUploadResponse, status_code=201)
async def upload_document(
    deal_id: str,
    document_category: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Upload a document for a deal."""
    # Determine file type
    ext = os.path.splitext(file.filename or "")[1].lower().strip(".")
    allowed = {"pdf", "xlsx", "xls", "csv", "docx", "pptx", "png", "jpg", "jpeg"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"File type .{ext} not supported")

    # Save file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, deal_id, f"{file_id}.{ext}")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    doc = Document(
        id=file_id,
        deal_id=deal_id,
        filename=file.filename or "unknown",
        file_type=ext,
        document_category=document_category,
        storage_path=file_path,
        file_size=len(content),
        processing_status="uploaded",
    )
    db.add(doc)
    await db.flush()
    await db.refresh(doc)

    # TODO: trigger async document processing pipeline
    return DocumentUploadResponse.model_validate(doc)


@router.get("/deal/{deal_id}", response_model=list[DocumentResponse])
async def list_documents(
    deal_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.deal_id == deal_id))
    docs = result.scalars().all()
    return [DocumentResponse.model_validate(d) for d in docs]


@router.delete("/{doc_id}", status_code=204)
async def delete_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    # Remove file from disk
    if os.path.exists(doc.storage_path):
        os.remove(doc.storage_path)
    await db.delete(doc)
