from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse


class CreatorProfileCreate(BaseModel):
    category: str  # e.g., Doctor, Lawyer, Barber
    title: Optional[str] = None
    bio: Optional[str] = None
    hourly_rate: float = 0.0
    slot_duration_minutes: int = 30
    timezone: str = "UTC"


class CreatorProfileUpdate(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    hourly_rate: Optional[float] = None
    slot_duration_minutes: Optional[int] = None
    timezone: Optional[str] = None
    is_active: Optional[bool] = None


class CreatorProfileResponse(BaseModel):
    id: str
    user_id: str
    category: str
    title: Optional[str] = None
    bio: Optional[str] = None
    hourly_rate: float
    slot_duration_minutes: int
    timezone: str
    is_active: bool
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
