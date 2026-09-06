import uvicorn

from cctv_ai.core.settings import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "cctv_ai.app:create_app",
        host=settings.host,
        port=settings.port,
        factory=True,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
