import React from 'react';

function RiskSection({ risk }) {
  const getRiskClass = () => {
    switch (risk.overall_risk_level) {
      case 'LOW':
        return 'risk-low';
      case 'MEDIUM':
        return 'risk-medium';
      case 'HIGH':
        return 'risk-high';
      default:
        return 'risk-medium';
    }
  };

  const getRiskDescription = () => {
    switch (risk.overall_risk_level) {
      case 'LOW':
        return 'Esta inversión presenta bajo riesgo general. Los fundamentos son sólidos y los riesgos identificados son manejables.';
      case 'MEDIUM':
        return 'Esta inversión presenta riesgo moderado. Hay algunos factores a considerar pero son manejables con la debida diligencia.';
      case 'HIGH':
        return 'Esta inversión presenta alto riesgo. Hay múltiples factores preocupantes que podrían resultar en pérdidas significativas.';
      default:
        return 'Evaluando nivel de riesgo...';
    }
  };

  return (
    <div>
      <h3 className="mb-2">Análisis de Riesgo</h3>
      <p className="text-secondary mb-3">
        Para los inversores value, lo más importante es evitar la pérdida permanente de capital.
        Este análisis identifica riesgos que podrían afectar tu inversión.
      </p>

      <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
        <div style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '1rem', color: '#6b7280' }}>
          NIVEL DE RIESGO GENERAL
        </div>
        <div className={`risk-level ${getRiskClass()}`} style={{ fontSize: '1.5rem' }}>
          {risk.overall_risk_level}
        </div>
        <p style={{ marginTop: '1rem', color: '#6b7280' }}>
          {getRiskDescription()}
        </p>
      </div>

      <div className="card mt-3">
        <h4 style={{ marginBottom: '1rem' }}>Volatilidad y Beta</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
              VOLATILIDAD ANUAL
            </div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
              {(risk.volatility * 100).toFixed(1)}%
            </div>
          </div>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
              BETA
            </div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
              {risk.beta.toFixed(2)}
            </div>
          </div>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
          <p style={{ whiteSpace: 'pre-line' }}>{risk.volatility_explanation}</p>
        </div>
      </div>

      <div className="card mt-3">
        <h4 style={{ marginBottom: '1rem' }}>Riesgo de Deuda</h4>
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
            COBERTURA DE INTERESES
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
            {risk.debt_coverage_ratio >= 999 ? '∞' : risk.debt_coverage_ratio.toFixed(2)}x
          </div>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
          <p style={{ whiteSpace: 'pre-line' }}>{risk.debt_risk_explanation}</p>
        </div>
      </div>

      <div className="card mt-3" style={{ border: '2px solid #ef4444', backgroundColor: '#fef2f2' }}>
        <h4 style={{ marginBottom: '1rem', color: '#991b1b' }}>
          ⚠️ Riesgos de Pérdida Permanente de Capital
        </h4>
        <p className="text-secondary mb-2">
          Estos son los riesgos más importantes para un inversor value. Una pérdida permanente
          ocurre cuando el valor fundamental de la empresa se deteriora de forma irreversible.
        </p>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {risk.permanent_loss_risks.map((riskItem, index) => (
            <li key={index} style={{
              padding: '0.75rem',
              marginBottom: '0.5rem',
              backgroundColor: 'white',
              borderRadius: '6px',
              borderLeft: '3px solid #ef4444'
            }}>
              {riskItem}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default RiskSection;
