import React from 'react';

function MetricCard({ label, value, status, description }) {
  const getStatusClass = () => {
    switch (status) {
      case 'PASS':
        return 'pass';
      case 'NEUTRAL':
        return 'neutral';
      case 'FAIL':
        return 'fail';
      default:
        return 'neutral';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'PASS':
        return '✓';
      case 'NEUTRAL':
        return '≈';
      case 'FAIL':
        return '✗';
      default:
        return '';
    }
  };

  return (
    <div className={`metric-card ${getStatusClass()}`}>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      {description && (
        <div className="metric-status">
          {getStatusIcon()} {description}
        </div>
      )}
    </div>
  );
}

export default MetricCard;
