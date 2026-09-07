from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "CCTV AI Service"
    host: str = "0.0.0.0"
    port: int = 8010
    reload: bool = False
    rabbitmq_url: str = "amqp://cctv:cctv@rabbitmq:5672/"
    rabbitmq_exchange: str = "cctv.tracking"
    rabbitmq_queue: str = "track-events"
    rabbitmq_routing_key: str = "track.events"
    video_source: str = "samples/input.mp4"
    camera_id: str = "camera-01"
    stream_width: int = 1280
    stream_height: int = 720
    stream_fps: int = 20
    model_path: str = "yolo11n.pt"
    detection_confidence: float = 0.35
    inference_device: str = "cpu"

    model_config = SettingsConfigDict(env_prefix="AI_", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
