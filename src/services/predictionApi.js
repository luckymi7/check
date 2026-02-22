import { ErrorCodes, MedAIError } from '../utils/errors';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const PREDICT_ENDPOINT = import.meta.env.VITE_PREDICT_ENDPOINT || '/predict';

async function parseErrorResponse(response) {
  try {
    const body = await response.json();
    if (body?.detail) {
      return body.detail;
    }
    if (body?.message) {
      return body.message;
    }
  } catch {
    // Intentionally ignored: fallback to status text.
  }

  return response.statusText || 'Unknown API error';
}

export async function requestPrediction(imageBlob) {
  const formData = new FormData();
  formData.append('file', imageBlob, `capture-${Date.now()}.jpg`);

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${PREDICT_ENDPOINT}`, {
      method: 'POST',
      body: formData,
    });
  } catch (error) {
    throw new MedAIError(ErrorCodes.NETWORK_ERROR, 'Network communication failed', error);
  }

  if (!response.ok) {
    const message = await parseErrorResponse(response);
    throw new MedAIError(ErrorCodes.API_ERROR, message);
  }

  let data;
  try {
    data = await response.json();
  } catch (error) {
    throw new MedAIError(ErrorCodes.INVALID_RESPONSE, 'Unable to parse prediction response', error);
  }

  const diseaseName = data?.disease ?? data?.disease_name ?? data?.label;
  const confidence = data?.confidence;
  const susceptibility = data?.treatment_susceptibility ?? data?.susceptibility;

  if (!diseaseName || confidence === undefined || confidence === null) {
    throw new MedAIError(
      ErrorCodes.EMPTY_PREDICTION,
      'Prediction response missing disease name or confidence',
      data,
    );
  }

  return {
    disease: diseaseName,
    confidence: Number(confidence),
    susceptibility: susceptibility || 'Not provided',
    raw: data,
  };
}
