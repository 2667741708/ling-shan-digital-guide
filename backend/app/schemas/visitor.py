from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    device_type: str = "web"
    user_profile: dict = Field(default_factory=dict)
    start_location: dict = Field(default_factory=dict)


class ChatTextRequest(BaseModel):
    session_uuid: str
    message: str
    current_location: dict = Field(default_factory=dict)


class RouteRecommendRequest(BaseModel):
    session_uuid: str
    interest: list[str] = Field(default_factory=list)
    available_time: int = 120
    physical_strength: str = "normal"
    start_spot_id: int = 1
    avoid_crowd: bool = True
