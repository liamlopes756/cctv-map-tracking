from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class TrackEvent(BaseModel):
    camera_id: str
    source_uri: str
    track_id: str
    frame_number: int
    x: float
    y: float
    width: float
    height: float
    confidence: float
