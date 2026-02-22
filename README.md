# MedAI Frontend (React + Vite)

Modern React frontend for AI-assisted skin disease detection that connects to a FastAPI backend.

## Features

- Live camera preview with browser `getUserMedia`
- Near real-time capture (default every 1.5s) and prediction
- Device image upload fallback
- Structured prediction panel:
  - Disease name
  - Confidence percentage
  - Treatment susceptibility
- Centralized error handling for:
  - Camera permission and stream failures
  - Network/API failures
  - Invalid or empty backend responses
- Loading and retry states
- Mobile-friendly responsive layout
- Clinical safety disclaimer in UI

## Tech Stack

- React 18
- Vite 5
- Native Fetch API for backend calls

## Environment Variables

Create a `.env` file in the project root:

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_PREDICT_ENDPOINT=/predict
VITE_CAPTURE_INTERVAL_MS=1500
```

## FastAPI Contract Assumption

The frontend sends `multipart/form-data` with a `file` field containing the captured/uploaded image.

Expected successful response shape (flexible key support is included):

```json
{
  "disease": "Eczema",
  "confidence": 0.94,
  "treatment_susceptibility": "Responsive to topical corticosteroids"
}
```

Also supported aliases:
- `disease_name` or `label` instead of `disease`
- `susceptibility` instead of `treatment_susceptibility`

## Setup

```bash
npm install
npm run dev
```

Open the app at the URL printed by Vite (typically `http://localhost:5173`).

## Build for Production

```bash
npm run build
npm run preview
```

## Reliability Notes

- Camera stream is fully stopped when user clicks **Stop Camera** or when component unmounts.
- Preview object URLs are revoked to avoid memory leaks.
- Failed prediction responses do not crash UI; they surface actionable messages and allow retry.

## Clinical Safety Note

This interface is intended for **AI-assisted triage/decision support only** and must not replace clinician judgment.
