import logging
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import tensorflow as tf

from backend.app.exceptions.custom_exceptions import InferenceException, ModelLoadingException

logger = logging.getLogger(__name__)


class ModelService:
    def __init__(self, model_path: str, class_names: List[str]):
        self.model_path = model_path
        self.class_names = class_names
        self.model: Optional[tf.keras.Model] = None

    @property
    def is_loaded(self) -> bool:
        return self.model is not None

    def load_model(self) -> None:
        try:
            path = Path(self.model_path)
            if not path.exists():
                raise ModelLoadingException(
                    f"Model path does not exist: {self.model_path}. Set MODEL_PATH correctly."
                )

            self.model = tf.keras.models.load_model(self.model_path)
            logger.info("Model loaded successfully from %s", self.model_path)
        except ModelLoadingException:
            raise
        except Exception as exc:
            raise ModelLoadingException("Failed to load TensorFlow/Keras model.") from exc

    def predict(self, preprocessed_image: np.ndarray) -> Tuple[str, float]:
        if self.model is None:
            raise InferenceException("Model is not loaded. Please check server startup logs.")

        try:
            raw_predictions = self.model.predict(preprocessed_image, verbose=0)
            vector = raw_predictions[0]

            predicted_index = int(np.argmax(vector))
            confidence = float(vector[predicted_index])

            if predicted_index >= len(self.class_names):
                disease = f"Class-{predicted_index}"
            else:
                disease = self.class_names[predicted_index]

            return disease, confidence
        except Exception as exc:
            raise InferenceException("Failed during AI inference.") from exc
