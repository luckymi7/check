from pydantic import BaseSettings, Field
from typing import List


class Settings(BaseSettings):
    app_name: str = "MedAI Backend"
    app_version: str = "1.0.0"
    debug: bool = False

    model_path: str = Field("backend/model/skin_model.h5", env="MODEL_PATH")
    image_size: int = Field(224, env="IMAGE_SIZE")
    class_names: List[str] = Field(
        default_factory=lambda: [
            "Acne",
            "Eczema",
            "Melanoma",
            "Psoriasis",
            "Rosacea",
        ]
    )

    cors_origins: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
