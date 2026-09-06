from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "CCTV AI Service"
    host: str = "0.0.0.0"
    port: int = 8010
    reload: bool = True
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    video_source: str = "samples/input.mp4"

    model_config = SettingsConfigDict(env_prefix="AI_", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
