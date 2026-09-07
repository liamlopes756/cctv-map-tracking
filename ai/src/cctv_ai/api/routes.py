from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from cctv_ai.core.models import HealthResponse
from cctv_ai.core.settings import get_settings
from cctv_ai.events.publisher import EventPublisher
from cctv_ai.video.processor import VideoProcessor

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="ai")


@router.get("/stream.mjpg")
def stream_mjpeg() -> StreamingResponse:
    settings = get_settings()
    processor = VideoProcessor(settings=settings, publisher=EventPublisher(settings))
    return StreamingResponse(
        processor.mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
