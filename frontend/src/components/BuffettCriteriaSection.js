import React from 'react';
import MetricCard from './MetricCard';

function BuffettCriteriaSection({ criteria }) {
  const formatCurrency = (value) => {
    if (Math.abs(value) >= 1e9) {
      return `$${(value / 1e9).toFixed(2)}B`;
    } else if (Math.abs(value) >= 1e6) {
      return `$${(value / 1e6).toFixed(2)}M`;
    } else if (Math.abs(value) >= 1e3) {
      return `$${(value / 1e3).toFixed(2)}K`;
    }
    return `$${value.toFixed(2)}`;
  };

  return (
    <div>
      <h3 className="mb-2">Criterios de Warren Buffett</h3>
      <p className="text-secondary mb-3">
        Warren Buffett se enfoca en la calidad del negocio: empresas con ventajas competitivas
        sostenibles, alta rentabilidad y management excelente.
      </p>

      <div className="metric-grid">
        <MetricCard
          label="ROE (Return on Equity)"
          value={`${(criteria.roe * 100).toFixed(1)}%`}
          status={criteria.roe_pass ? 'PASS' : 'FAIL'}
          description={criteria.roe_pass ? 'Mayor a 15% ✓' : 'Debe ser mayor a 15%'}
        />
        <MetricCard
          label="Margen Operativo"
          value={`${(criteria.operating_margin * 100).toFixed(1)}%`}
          status={criteria.operating_margin_stable ? 'PASS' : 'NEUTRAL'}
          description={criteria.operating_margin_stable ? 'Estable y saludable ✓' : 'Revisar estabilidad'}
        />
        <MetricCard
          label="Free Cash Flow"
          value={formatCurrency(criteria.free_cash_flow)}
          status={criteria.fcf_positive ? 'PASS' : 'FAIL'}
          description={criteria.fcf_positive ? 'Positivo y de calidad ✓' : 'Negativo o bajo'}
        />
      </div>

      <div className="mt-3 card" style={{ backgroundColor: '#f0f9ff', border: '2px solid #3b82f6' }}>
        <h4 style={{ marginBottom: '0.5rem' }}>Ventaja Competitiva (Economic Moat)</h4>
        <p>{criteria.competitive_advantage}</p>
      </div>

      <div className="mt-3">
        <div className={`badge ${criteria.overall_score >= 3 ? 'badge-success' : criteria.overall_score >= 2 ? 'badge-warning' : 'badge-danger'}`}>
          Puntuación Buffett: {criteria.overall_score} / 4
        </div>
        <p className="mt-2">
          {criteria.overall_score >= 3 && '✓ Excelente - Negocio de alta calidad que Buffett consideraría'}
          {criteria.overall_score === 2 && '≈ Bueno - Negocio de calidad con algunas características atractivas'}
          {criteria.overall_score === 1 && '⚠ Regular - Negocio promedio, puede carecer de ventajas competitivas'}
          {criteria.overall_score === 0 && '✗ Pobre - Negocio de baja calidad, no suitable para value investing'}
        </p>
      </div>
    </div>
  );
}

export default BuffettCriteriaSection;
