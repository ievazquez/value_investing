import React from 'react';

function RecommendationBanner({ recommendation, score, companyName, ticker }) {
  const getRecommendationClass = () => {
    switch (recommendation) {
      case 'STRONG_BUY':
        return 'recommendation-strong-buy';
      case 'BUY':
        return 'recommendation-buy';
      case 'HOLD':
        return 'recommendation-hold';
      case 'AVOID':
        return 'recommendation-avoid';
      default:
        return 'recommendation-hold';
    }
  };

  const getRecommendationText = () => {
    switch (recommendation) {
      case 'STRONG_BUY':
        return '✓ COMPRA FUERTE';
      case 'BUY':
        return '✓ BUENA COMPRA';
      case 'HOLD':
        return '≈ MANTENER / CONSIDERAR';
      case 'AVOID':
        return '✗ EVITAR';
      default:
        return 'SIN RECOMENDACIÓN';
    }
  };

  const getRecommendationDescription = () => {
    switch (recommendation) {
      case 'STRONG_BUY':
        return 'Excelente oportunidad de value investing';
      case 'BUY':
        return 'Buena oportunidad con algunos aspectos a considerar';
      case 'HOLD':
        return 'No cumple todos los criterios estrictos';
      case 'AVOID':
        return 'No recomendable según principios de value investing';
      default:
        return '';
    }
  };

  return (
    <div className={`recommendation-banner ${getRecommendationClass()}`}>
      <h2>{getRecommendationText()}</h2>
      <div className="score-display">{score.toFixed(1)} / 10</div>
      <h3>{companyName} ({ticker})</h3>
      <p style={{ marginTop: '0.5rem', fontSize: '1.1rem' }}>
        {getRecommendationDescription()}
      </p>
    </div>
  );
}

export default RecommendationBanner;
