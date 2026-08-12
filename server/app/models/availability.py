import uuid
from sqlalchemy import String, Integer, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class AvailabilityRule(Base):
    __tablename__ = "availability_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id: Mapped[str] = mapped_column(String(36), ForeignKey("creator_profiles.id", ondelete="CASCADE"), nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)  # 0 = Monday, ..., 6 = Sunday
    start_time: Mapped[str] = mapped_column(String(8), nullable=False)  # HH:MM format (e.g. "09:00")
    end_time: Mapped[str] = mapped_column(String(8), nullable=False)    # HH:MM format (e.g. "17:00")

    # Relationships
    creator = relationship("CreatorProfile", back_populates="availability_rules")
