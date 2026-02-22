import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import ErrorBanner from './components/ErrorBanner';
import ResultPanel from './components/ResultPanel';
import { requestPrediction } from './services/predictionApi';
import { ErrorCodes, MedAIError, getUserFriendlyMessage } from './utils/errors';

const CAPTURE_INTERVAL_MS = Number(import.meta.env.VITE_CAPTURE_INTERVAL_MS || 1500);

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);

  const [cameraActive, setCameraActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');
  const [previewUrl, setPreviewUrl] = useState('');
  const [lastUpdated, setLastUpdated] = useState(null);

  const canUseCamera = useMemo(
    () => typeof navigator !== 'undefined' && !!navigator.mediaDevices?.getUserMedia,
    [],
  );

  const clearPreview = useCallback(() => {
    setPreviewUrl((current) => {
      if (current) {
        URL.revokeObjectURL(current);
      }
      return '';
    });
  }, []);

  const predictFromBlob = useCallback(async (blob) => {
    setLoading(true);
    setError('');

    try {
      const result = await requestPrediction(blob);
      setPrediction(result);
      setLastUpdated(new Date());
    } catch (err) {
      const msg = getUserFriendlyMessage(err);
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  const captureFrame = useCallback(async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas || video.videoWidth === 0 || video.videoHeight === 0) {
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.85));
    if (!blob) {
      setError('Failed to capture image. Please retry.');
      return;
    }

    await predictFromBlob(blob);
  }, [predictFromBlob]);

  const stopCamera = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setCameraActive(false);
  }, []);

  const startCamera = useCallback(async () => {
    if (!canUseCamera) {
      setError(getUserFriendlyMessage(new MedAIError(ErrorCodes.CAMERA_NOT_SUPPORTED, 'Camera API missing')));
      return;
    }

    setError('');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: 'environment' },
        },
        audio: false,
      });

      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      setCameraActive(true);

      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }

      intervalRef.current = setInterval(() => {
        captureFrame();
      }, CAPTURE_INTERVAL_MS);
    } catch (err) {
      if (err?.name === 'NotAllowedError') {
        setError(
          getUserFriendlyMessage(
            new MedAIError(ErrorCodes.CAMERA_PERMISSION_DENIED, 'Camera permission denied', err),
          ),
        );
      } else {
        setError(
          getUserFriendlyMessage(new MedAIError(ErrorCodes.CAMERA_STREAM_FAILURE, 'Unable to start camera', err)),
        );
      }
      stopCamera();
    }
  }, [canUseCamera, captureFrame, stopCamera]);

  const handleImageUpload = useCallback(
    async (event) => {
      const file = event.target.files?.[0];
      if (!file || !file.type.startsWith('image/')) {
        setError('Please select a valid image file.');
        return;
      }

      stopCamera();
      clearPreview();

      const localUrl = URL.createObjectURL(file);
      setPreviewUrl(localUrl);
      await predictFromBlob(file);
      event.target.value = '';
    },
    [clearPreview, predictFromBlob, stopCamera],
  );

  useEffect(
    () => () => {
      stopCamera();
      clearPreview();
    },
    [clearPreview, stopCamera],
  );

  return (
    <main className="app-shell">
      <header className="page-header">
        <h1>MedAI Skin Disease Detection</h1>
        <p className="subtitle">AI-assisted skin condition screening for clinical decision support.</p>
      </header>

      <ErrorBanner message={error} onRetry={cameraActive ? captureFrame : null} />

      <section className="content-grid">
        <section className="panel">
          <h2>Image Input</h2>
          <div className="preview-area">
            {cameraActive ? (
              <video ref={videoRef} autoPlay playsInline muted className="media-preview" />
            ) : previewUrl ? (
              <img src={previewUrl} alt="Uploaded skin sample" className="media-preview" />
            ) : (
              <div className="placeholder">Camera inactive. Start camera or upload an image.</div>
            )}
          </div>

          <canvas ref={canvasRef} className="hidden-canvas" aria-hidden="true" />

          <div className="controls">
            <button type="button" className="primary-btn" onClick={startCamera} disabled={cameraActive || loading}>
              Start Camera
            </button>
            <button type="button" className="secondary-btn" onClick={stopCamera} disabled={!cameraActive}>
              Stop Camera
            </button>
            <label className="upload-btn" htmlFor="upload-input">
              Upload Image
            </label>
            <input
              id="upload-input"
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              disabled={loading}
            />
          </div>
          <p className="hint">Live mode captures a frame every {CAPTURE_INTERVAL_MS / 1000}s for near real-time inference.</p>
        </section>

        <ResultPanel prediction={prediction} loading={loading} lastUpdated={lastUpdated} />
      </section>

      <footer className="disclaimer">
        <strong>Medical disclaimer:</strong> MedAI provides AI-assisted suggestions and is not a standalone diagnostic
        tool. Final diagnosis must be made by qualified clinicians.
      </footer>
    </main>
  );
}

export default App;
