"""
Uploaded document ORM model.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    deal_id: Mapped[str] = mapped_column(String(36), ForeignKey("deals.id"))
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pdf, xlsx, docx, pptx, csv
    document_category: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # pitch_deck, financials, cap_table, legal, market_report, other
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=True)
    processing_status: Mapped[str] = mapped_column(
        String(50), default="uploaded"
    )  # uploaded, processing, processed, failed
    extracted_text: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    deal = relationship("Deal", back_populates="documents")
