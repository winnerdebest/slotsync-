import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Enum, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class AppointmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    creator_id: Mapped[str] = mapped_column(String(36), ForeignKey("creator_profiles.id", ondelete="CASCADE"), nullable=False)
    start_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.CONFIRMED, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    client = relationship("User", foreign_keys=[client_id], back_populates="client_appointments")
    creator = relationship("CreatorProfile", foreign_keys=[creator_id], back_populates="creator_appointments")

    __table_args__ = (
        # Ensure a creator cannot be double-booked at the exact same start time unless CANCELLED/REJECTED
        # (Conflict check logic handles overlap, unique constraint guards exact start time collisions)
        UniqueConstraint("creator_id", "start_time_utc", name="uq_creator_start_time"),
    )
