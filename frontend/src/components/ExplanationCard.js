import React from 'react';

function ExplanationCard({ explanation }) {
  const getStatusBadge = () => {
    switch (explanation.status) {
      case 'PASS':
        return <span className="badge badge-success">Cumple Criterio</span>;
      case 'NEUTRAL':
        return <span className="badge badge-warning">Neutral</span>;
      case 'FAIL':
        return <span className="badge badge-danger">No Cumple</span>;
      default:
        return null;
    }
  };

  return (
    <div className="explanation-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
        <h3 className="explanation-title">{explanation.metric_name}</h3>
        {getStatusBadge()}
      </div>

      <div className="explanation-section">
        <h4>¿Qué es?</h4>
        <p>{explanation.simple_definition}</p>
      </div>

      <div className="explanation-section">
        <h4>¿Por qué es importante?</h4>
        <p>{explanation.why_important}</p>
      </div>

      <div className="explanation-section">
        <h4>Cálculo</h4>
        <div className="formula">{explanation.formula}</div>
      </div>

      <div className="explanation-section">
        <h4>Ejemplo Numérico</h4>
        <div className="example-box">
          <p style={{ whiteSpace: 'pre-line' }}>{explanation.numeric_example}</p>
        </div>
      </div>

      {explanation.sector_comparison && (
        <div className="explanation-section">
          <h4>Comparación con el Sector</h4>
          <p>{explanation.sector_comparison}</p>
        </div>
      )}

      <div className="explanation-section">
        <h4>Interpretación</h4>
        <p style={{ fontWeight: '600', fontSize: '1.05rem' }}>
          {explanation.interpretation}
        </p>
      </div>
    </div>
  );
}

export default ExplanationCard;
