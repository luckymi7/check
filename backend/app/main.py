from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.logging import configure_logging
from backend.app.exceptions.handlers import add_exception_handlers
from backend.app.routers.inference import router as inference_router
from backend.app.schemas.prediction import HealthResponse
from backend.app.services.model_service import ModelService


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()

    model_service = ModelService(settings.model_path, settings.class_names)
    app.state.model_startup_error = None
    try:
        model_service.load_model()
    except Exception as exc:
        app.state.model_startup_error = str(exc)
    app.state.model_service = model_service

    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    description=(
        "MedAI backend for skin disease detection and treatment susceptibility insights "
        "using a TensorFlow/Keras model."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handlers(app)
app.include_router(inference_router)


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    model_service = app.state.model_service
    return HealthResponse(
        success=True,
        status="ok" if model_service.is_loaded else "degraded",
        model_loaded=model_service.is_loaded,
        message=app.state.model_startup_error,
    )
