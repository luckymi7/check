from fastapi import APIRouter, Depends, File, UploadFile
from starlette.concurrency import run_in_threadpool

from backend.app.core.config import settings
from backend.app.core.dependencies import get_model_service
from backend.app.exceptions.custom_exceptions import ImageDecodingException
from backend.app.schemas.prediction import CameraImageRequest, ErrorResponse, PredictionResponse
from backend.app.services.model_service import ModelService
from backend.app.utils.image_processing import (
    confidence_to_susceptibility,
    decode_base64_image,
    preprocess_image_bytes,
    validate_filename,
)

router = APIRouter(prefix="/api/v1", tags=["inference"])


ERROR_RESPONSES = {
    400: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
    503: {"model": ErrorResponse},
}


@router.post("/predict/upload", response_model=PredictionResponse, responses=ERROR_RESPONSES)
async def predict_from_upload(
    file: UploadFile = File(...), model_service: ModelService = Depends(get_model_service)
) -> PredictionResponse:
    validate_filename(file.filename)
    image_bytes = await file.read()
    if not image_bytes:
        raise ImageDecodingException("Uploaded file is empty.")

    image_array = preprocess_image_bytes(image_bytes, settings.image_size)
    disease, confidence = await run_in_threadpool(model_service.predict, image_array)
    return PredictionResponse(
        success=True,
        disease=disease,
        confidence=round(confidence, 4),
        treatment_susceptibility=confidence_to_susceptibility(confidence),
    )


@router.post("/predict/camera", response_model=PredictionResponse, responses=ERROR_RESPONSES)
async def predict_from_camera(
    payload: CameraImageRequest, model_service: ModelService = Depends(get_model_service)
) -> PredictionResponse:
    image_bytes = decode_base64_image(payload.image_base64)
    image_array = preprocess_image_bytes(image_bytes, settings.image_size)

    disease, confidence = await run_in_threadpool(model_service.predict, image_array)
    return PredictionResponse(
        success=True,
        disease=disease,
        confidence=round(confidence, 4),
        treatment_susceptibility=confidence_to_susceptibility(confidence),
    )
