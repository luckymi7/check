export class MedAIError extends Error {
  constructor(code, message, details = null) {
    super(message);
    this.name = 'MedAIError';
    this.code = code;
    this.details = details;
  }
}

export const ErrorCodes = {
  CAMERA_PERMISSION_DENIED: 'CAMERA_PERMISSION_DENIED',
  CAMERA_NOT_SUPPORTED: 'CAMERA_NOT_SUPPORTED',
  CAMERA_STREAM_FAILURE: 'CAMERA_STREAM_FAILURE',
  API_ERROR: 'API_ERROR',
  NETWORK_ERROR: 'NETWORK_ERROR',
  INVALID_RESPONSE: 'INVALID_RESPONSE',
  EMPTY_PREDICTION: 'EMPTY_PREDICTION',
};

export function getUserFriendlyMessage(error) {
  if (!(error instanceof MedAIError)) {
    return 'Unexpected issue detected. Please refresh and try again.';
  }

  switch (error.code) {
    case ErrorCodes.CAMERA_PERMISSION_DENIED:
      return 'Camera access denied. Please allow camera access to enable live detection.';
    case ErrorCodes.CAMERA_NOT_SUPPORTED:
      return 'Your browser does not support camera access. Please use a modern browser.';
    case ErrorCodes.CAMERA_STREAM_FAILURE:
      return 'Unable to start camera stream. Try closing other camera apps and retry.';
    case ErrorCodes.NETWORK_ERROR:
      return 'Cannot reach the MedAI server. Check your connection and backend status.';
    case ErrorCodes.API_ERROR:
      return error.message || 'The AI service returned an error. Please retry shortly.';
    case ErrorCodes.INVALID_RESPONSE:
    case ErrorCodes.EMPTY_PREDICTION:
      return 'Prediction response was incomplete. Capture another image to retry.';
    default:
      return 'Something went wrong. Please retry.';
  }
}
