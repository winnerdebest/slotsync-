from pydantic import BaseModel, ConfigDict


class DeviceRegisterRequest(BaseModel):
    fcm_token: str
    device_type: str = "android"  # "android" or "ios"


class DeviceResponse(BaseModel):
    id: str
    user_id: str
    fcm_token: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)
