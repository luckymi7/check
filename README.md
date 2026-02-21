# MedAI Backend (FastAPI + TensorFlow/Keras)

Production-oriented backend service for skin disease detection and treatment susceptibility insights.

## Features

- FastAPI async API with OpenAPI/Swagger docs
- Accepts image input via:
  - `multipart/form-data` upload
  - base64 camera payload
- Image preprocessing:
  - RGB conversion
  - resize to configured model size
  - normalization to `[0, 1]`
- TensorFlow/Keras model inference
- Global exception handling with standardized error response
- CORS enabled for React frontend
- `/health` endpoint for service/model readiness
- Centralized logging

## Project Structure

```txt
backend/
└── app/
    ├── main.py
    ├── routers/
    ├── services/
    ├── schemas/
    ├── utils/
    ├── core/
    └── exceptions/
```

## Setup

1. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set model path (optional if using default):

```bash
export MODEL_PATH="backend/model/skin_model.h5"
```

4. Run server:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### `GET /health`
Returns service status and model load state. If the model failed during startup, status is `degraded` and `message` includes failure details.

### `POST /api/v1/predict/upload`
Accepts image file upload in `multipart/form-data`.

Example:

```bash
curl -X POST "http://localhost:8000/api/v1/predict/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.jpg"
```

### `POST /api/v1/predict/camera`
Accepts base64 image payload:

```json
{
  "image_base64": "data:image/png;base64,iVBORw0..."
}
```

## Success Response

```json
{
  "success": true,
  "disease": "Melanoma",
  "confidence": 0.9421,
  "treatment_susceptibility": "High confidence for targeted treatment planning"
}
```

## Error Response

```json
{
  "success": false,
  "error_code": "ERROR_CODE",
  "message": "User-friendly explanation"
}
```
