import logging

from fastapi import FastAPI
from uvicorn import run

from core.config import settings


settings.log.setup_logging()
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    app = FastAPI(title="Title API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

    return app

main_app = create_application()


if __name__ == '__main__':
    logger.info("Starting server")
    run("main:main_app", host=settings.run.host, port=settings.run.port)