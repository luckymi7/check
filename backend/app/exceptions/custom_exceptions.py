class MedAIException(Exception):
    error_code = "INTERNAL_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidImageFormatException(MedAIException):
    error_code = "INVALID_IMAGE_FORMAT"


class ImageDecodingException(MedAIException):
    error_code = "IMAGE_DECODING_ERROR"


class ModelLoadingException(MedAIException):
    error_code = "MODEL_LOADING_FAILED"


class InferenceException(MedAIException):
    error_code = "INFERENCE_FAILED"
