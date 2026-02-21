import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from backend.app.exceptions.custom_exceptions import (
    ImageDecodingException,
    InferenceException,
    InvalidImageFormatException,
    MedAIException,
    ModelLoadingException,
)

logger = logging.getLogger(__name__)


def build_error_response(error_code: str, message: str, http_status: int) -> JSONResponse:
    return JSONResponse(
        status_code=http_status,
        content={
            "success": False,
            "error_code": error_code,
            "message": message,
        },
    )


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(MedAIException)
    async def medai_exception_handler(_: Request, exc: MedAIException) -> JSONResponse:
        logger.warning("Handled MedAI exception: %s - %s", exc.error_code, exc.message)

        status_map = {
            InvalidImageFormatException: status.HTTP_400_BAD_REQUEST,
            ImageDecodingException: status.HTTP_400_BAD_REQUEST,
            ModelLoadingException: status.HTTP_503_SERVICE_UNAVAILABLE,
            InferenceException: status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
        http_status = status_map.get(type(exc), status.HTTP_400_BAD_REQUEST)
        return build_error_response(exc.error_code, exc.message, http_status)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning("Validation error: %s", exc.errors())
        return build_error_response(
            error_code="REQUEST_VALIDATION_ERROR",
            message="Invalid request payload. Please verify submitted fields.",
            http_status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled server error: %s", str(exc))
        return build_error_response(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
