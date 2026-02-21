import base64
import io
import numpy as np
from PIL import Image, UnidentifiedImageError

from backend.app.exceptions.custom_exceptions import ImageDecodingException, InvalidImageFormatException

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def validate_filename(filename: str) -> None:
    if not filename:
        raise InvalidImageFormatException("Uploaded image must include a filename.")

    lowered = filename.lower()
    if not any(lowered.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise InvalidImageFormatException(
            "Unsupported image format. Allowed: .jpg, .jpeg, .png, .bmp, .webp"
        )


def decode_base64_image(base64_string: str) -> bytes:
    try:
        payload = base64_string.split(",", 1)[1] if "," in base64_string else base64_string
        return base64.b64decode(payload, validate=True)
    except Exception as exc:
        raise ImageDecodingException("Unable to decode base64 image payload.") from exc


def preprocess_image_bytes(image_bytes: bytes, image_size: int) -> np.ndarray:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise ImageDecodingException("Image content could not be decoded.") from exc
    except Exception as exc:
        raise ImageDecodingException("Unexpected image decoding error.") from exc

    image = image.resize((image_size, image_size))
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    return np.expand_dims(image_array, axis=0)


def confidence_to_susceptibility(confidence: float) -> str:
    if confidence >= 0.85:
        return "High confidence for targeted treatment planning"
    if confidence >= 0.60:
        return "Moderate confidence - consider confirmatory tests"
    return "Low confidence - specialist review recommended"
