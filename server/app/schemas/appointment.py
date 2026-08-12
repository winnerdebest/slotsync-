from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.appointment import AppointmentStatus
from app.schemas.creator import CreatorProfileResponse
from app.schemas.user import UserResponse


class AppointmentCreate(BaseModel):
    creator_id: str
    start_time_utc: datetime
    notes: Optional[str] = None


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentResponse(BaseModel):
    id: str
    client_id: str
    creator_id: str
    start_time_utc: datetime
    end_time_utc: datetime
    status: AppointmentStatus
    notes: Optional[str] = None
    created_at: datetime
    client: Optional[UserResponse] = None
    creator: Optional[CreatorProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)
