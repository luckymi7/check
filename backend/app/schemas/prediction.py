from typing import Optional

from pydantic import BaseModel, Field


class CameraImageRequest(BaseModel):
    image_base64: str = Field(..., description="Base64-encoded image string.")


class PredictionResponse(BaseModel):
    success: bool = True
    disease: str
    confidence: float
    treatment_susceptibility: str


class HealthResponse(BaseModel):
    success: bool
    status: str
    model_loaded: bool
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
