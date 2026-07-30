"""
Deal / Investment Opportunity ORM model.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=True)
    stage: Mapped[str] = mapped_column(String(50), nullable=True)  # Pre-Seed, Seed, Series A...
    business_model: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    website: Mapped[str] = mapped_column(String(500), nullable=True)
    funding_ask: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, in_progress, completed, archived
    investment_score: Mapped[int] = mapped_column(Integer, nullable=True)
    recommendation: Mapped[str] = mapped_column(String(50), nullable=True)  # INVEST, CONDITIONAL, DO_NOT_INVEST

    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    created_by_user = relationship("User", back_populates="deals")
    documents = relationship("Document", back_populates="deal", lazy="selectin")
    analyses = relationship("Analysis", back_populates="deal", lazy="selectin")
    reports = relationship("Report", back_populates="deal", lazy="selectin")
