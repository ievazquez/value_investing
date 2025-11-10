import React from 'react';
import MetricCard from './MetricCard';

function GrahamCriteriaSection({ criteria }) {
  return (
    <div>
      <h3 className="mb-2">Criterios de Benjamin Graham</h3>
      <p className="text-secondary mb-3">
        Benjamin Graham, el padre del value investing, estableció criterios estrictos
        para identificar acciones infravaloradas con bajo riesgo.
      </p>

      <div className="metric-grid">
        <MetricCard
          label="P/E Ratio"
          value={criteria.pe_ratio.toFixed(2)}
          status={criteria.pe_ratio_pass ? 'PASS' : 'FAIL'}
          description={criteria.pe_ratio_pass ? 'Menor a 15 ✓' : 'Debe ser menor a 15'}
        />
        <MetricCard
          label="P/B Ratio"
          value={criteria.pb_ratio.toFixed(2)}
          status={criteria.pb_ratio_pass ? 'PASS' : 'FAIL'}
          description={criteria.pb_ratio_pass ? 'Menor a 1.5 ✓' : 'Debe ser menor a 1.5'}
        />
        <MetricCard
          label="Deuda / Capital"
          value={`${criteria.debt_to_equity.toFixed(1)}%`}
          status={criteria.debt_to_equity_pass ? 'PASS' : 'FAIL'}
          description={criteria.debt_to_equity_pass ? 'Menor a 50% ✓' : 'Debe ser menor a 50%'}
        />
        <MetricCard
          label="Current Ratio"
          value={criteria.current_ratio.toFixed(2)}
          status={criteria.current_ratio_pass ? 'PASS' : 'FAIL'}
          description={criteria.current_ratio_pass ? 'Mayor a 2.0 ✓' : 'Debe ser mayor a 2.0'}
        />
      </div>

      <div className="mt-3">
        <div className={`badge ${criteria.overall_score >= 4 ? 'badge-success' : criteria.overall_score >= 3 ? 'badge-warning' : 'badge-danger'}`}>
          Puntuación Graham: {criteria.overall_score} / 5
        </div>
        <p className="mt-2">
          {criteria.overall_score >= 4 && '✓ Excelente - Cumple los criterios estrictos de Graham'}
          {criteria.overall_score === 3 && '≈ Bueno - Cumple la mayoría de criterios con algunas preocupaciones'}
          {criteria.overall_score === 2 && '⚠ Regular - Cumple algunos criterios pero tiene preocupaciones significativas'}
          {criteria.overall_score < 2 && '✗ Pobre - No cumple los estándares de value investing de Graham'}
        </p>
      </div>
    </div>
  );
}

export default GrahamCriteriaSection;
