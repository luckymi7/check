from fastapi import Request

from backend.app.exceptions.custom_exceptions import ModelLoadingException
from backend.app.services.model_service import ModelService


def get_model_service(request: Request) -> ModelService:
    model_service = request.app.state.model_service
    if not model_service.is_loaded:
        startup_error = getattr(request.app.state, "model_startup_error", None)
        detail = startup_error or "AI model is unavailable. Please check MODEL_PATH and startup logs."
        raise ModelLoadingException(detail)
    return model_service
