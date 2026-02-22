export default function ErrorBanner({ message, onRetry }) {
  if (!message) {
    return null;
  }

  return (
    <div className="error-banner" role="alert">
      <p>{message}</p>
      {onRetry && (
        <button type="button" className="secondary-btn" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
}
