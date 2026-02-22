function formatConfidence(value) {
  if (Number.isNaN(value)) {
    return 'N/A';
  }

  const normalized = value > 1 ? value : value * 100;
  return `${Math.min(100, Math.max(0, normalized)).toFixed(1)}%`;
}

export default function ResultPanel({ prediction, loading, lastUpdated }) {
  if (loading) {
    return (
      <section className="panel result-panel loading-state" aria-live="polite">
        <h2>AI Prediction</h2>
        <p>Analyzing image…</p>
      </section>
    );
  }

  if (!prediction) {
    return (
      <section className="panel result-panel" aria-live="polite">
        <h2>AI Prediction</h2>
        <p>No prediction yet. Start the camera or upload an image.</p>
      </section>
    );
  }

  return (
    <section className="panel result-panel" aria-live="polite">
      <h2>AI Prediction</h2>
      <dl>
        <div>
          <dt>Disease</dt>
          <dd>{prediction.disease}</dd>
        </div>
        <div>
          <dt>Confidence</dt>
          <dd>{formatConfidence(prediction.confidence)}</dd>
        </div>
        <div>
          <dt>Treatment susceptibility</dt>
          <dd>{prediction.susceptibility}</dd>
        </div>
      </dl>
      {lastUpdated && <p className="timestamp">Last updated: {lastUpdated.toLocaleTimeString()}</p>}
    </section>
  );
}
