from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.classifier import router as classifier_router
from src.redis import setup_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await setup_redis_client()
    yield
    await app.state.redis.close()


def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.include_router(classifier_router)

    return app


app = get_app()
