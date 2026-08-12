from typing import List
from pydantic import BaseModel, ConfigDict, Field


class AvailabilityRuleCreate(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="HH:MM format, e.g., 09:00")
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="HH:MM format, e.g., 17:00")


class AvailabilityRuleResponse(BaseModel):
    id: str
    creator_id: str
    day_of_week: int
    start_time: str
    end_time: str

    model_config = ConfigDict(from_attributes=True)


class SetAvailabilityRequest(BaseModel):
    rules: List[AvailabilityRuleCreate]


class SlotResponse(BaseModel):
    start_time_utc: str  # ISO string in UTC
    end_time_utc: str    # ISO string in UTC
    is_available: bool = True
