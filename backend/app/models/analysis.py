"""
AI Analysis results ORM model.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Float, JSON, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    deal_id: Mapped[str] = mapped_column(String(36), ForeignKey("deals.id"))
    agent_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # startup_understanding, financial, market, competitive, risk, fraud, valuation, recommendation
    status: Mapped[str] = mapped_column(String(50), default="pending")
    result: Mapped[dict] = mapped_column(JSON, nullable=True)
    score: Mapped[float] = mapped_column(Float, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=True)  # source docs, citations
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    deal = relationship("Deal", back_populates="analyses")
