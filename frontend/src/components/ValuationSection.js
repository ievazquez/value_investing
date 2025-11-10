import React from 'react';

function ValuationSection({ dcf, multiples }) {
  const formatCurrency = (value) => {
    return `$${value.toFixed(2)}`;
  };

  const ValuationCard = ({ valuation }) => {
    const isUndervalued = valuation.margin_of_safety_percentage > 0;
    const meetsMinimum = valuation.meets_minimum_margin;

    return (
      <div className="card" style={{
        border: `2px solid ${meetsMinimum ? '#10b981' : isUndervalued ? '#f59e0b' : '#ef4444'}`,
        backgroundColor: meetsMinimum ? '#f0fdf4' : isUndervalued ? '#fffbeb' : '#fef2f2'
      }}>
        <h4 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>{valuation.method}</h4>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
              VALOR INTRÍNSECO
            </div>
            <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#2563eb' }}>
              {formatCurrency(valuation.intrinsic_value)}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
              PRECIO ACTUAL
            </div>
            <div style={{ fontSize: '1.75rem', fontWeight: '700' }}>
              {formatCurrency(valuation.current_price)}
            </div>
          </div>
        </div>

        <div style={{
          padding: '1rem',
          borderRadius: '8px',
          backgroundColor: 'white',
          border: `2px solid ${meetsMinimum ? '#10b981' : isUndervalued ? '#f59e0b' : '#ef4444'}`
        }}>
          <div style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.25rem' }}>
            MARGEN DE SEGURIDAD
          </div>
          <div style={{ fontSize: '2rem', fontWeight: '800', marginBottom: '0.5rem' }}>
            {valuation.margin_of_safety_percentage.toFixed(1)}%
          </div>
          <div style={{ fontSize: '0.95rem' }}>
            {meetsMinimum && (
              <span style={{ color: '#065f46', fontWeight: '600' }}>
                ✓ Supera el mínimo del 30% requerido por Graham
              </span>
            )}
            {!meetsMinimum && isUndervalued && (
              <span style={{ color: '#92400e', fontWeight: '600' }}>
                ⚠ Por debajo del mínimo del 30% requerido por Graham
              </span>
            )}
            {!isUndervalued && (
              <span style={{ color: '#991b1b', fontWeight: '600' }}>
                ✗ La acción está sobrevalorada - no hay margen de seguridad
              </span>
            )}
          </div>
        </div>

        {valuation.scenario_optimistic && (
          <div style={{ marginTop: '1rem', padding: '0.75rem', backgroundColor: 'white', borderRadius: '6px' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem' }}>
              Escenarios de Valoración:
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
              <span>Pesimista: {formatCurrency(valuation.scenario_pessimistic)}</span>
              <span>Base: {formatCurrency(valuation.scenario_base)}</span>
              <span>Optimista: {formatCurrency(valuation.scenario_optimistic)}</span>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div>
      <h3 className="mb-2">Valoración Intrínseca</h3>
      <p className="text-secondary mb-3">
        La valoración intrínseca estima el valor "real" de la empresa basándose en sus fundamentales.
        El <strong>margen de seguridad</strong> es la diferencia entre este valor y el precio actual.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem' }}>
        <ValuationCard valuation={dcf} />
        <ValuationCard valuation={multiples} />
      </div>

      <div className="mt-3 card" style={{ backgroundColor: '#eff6ff', border: '2px solid #3b82f6' }}>
        <h4 style={{ marginBottom: '0.75rem' }}>💡 ¿Qué es el Margen de Seguridad?</h4>
        <p style={{ lineHeight: '1.7' }}>
          El margen de seguridad es el concepto MÁS IMPORTANTE de Benjamin Graham.
          Es tu "colchón de protección" contra errores de cálculo, eventos inesperados o caídas del mercado.
          <br /><br />
          <strong>Graham requería un mínimo del 30%</strong> para considerar una inversión segura.
          Esto significa que si calculas que una empresa vale $100, solo deberías comprarla a $70 o menos.
          <br /><br />
          Este margen te protege si tu análisis tiene errores o si la empresa enfrenta problemas imprevistos.
        </p>
      </div>
    </div>
  );
}

export default ValuationSection;
