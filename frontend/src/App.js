import React, { useState } from 'react';
import './App.css';
import { stockAPI } from './services/api';
import SearchBar from './components/SearchBar';
import RecommendationBanner from './components/RecommendationBanner';
import ExpandableSection from './components/ExpandableSection';
import GrahamCriteriaSection from './components/GrahamCriteriaSection';
import BuffettCriteriaSection from './components/BuffettCriteriaSection';
import ValuationSection from './components/ValuationSection';
import RiskSection from './components/RiskSection';
import ExplanationCard from './components/ExplanationCard';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (ticker) => {
    setIsLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const data = await stockAPI.analyzeStock(ticker);
      setAnalysis(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Error al analizar la acción. Verifica que el ticker sea válido e intenta nuevamente.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1>📊 Value Investing Analyzer</h1>
          <p>
            Aprende a invertir como Benjamin Graham y Warren Buffett.
            Analiza acciones con explicaciones paso a paso para principiantes.
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container">
        {/* Search */}
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />

        {/* Loading State */}
        {isLoading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analizando acción... Esto puede tomar unos segundos.</p>
            <p className="text-secondary" style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
              Obteniendo datos financieros, calculando valoraciones y generando explicaciones educativas...
            </p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Analysis Results */}
        {analysis && !isLoading && (
          <div className="analysis-results">
            {/* Recommendation Banner */}
            <RecommendationBanner
              recommendation={analysis.recommendation}
              score={analysis.overall_score}
              companyName={analysis.company_name}
              ticker={analysis.ticker}
            />

            {/* Quick Summary */}
            <div className="card">
              <h3 className="mb-2">Resumen Rápido</h3>
              <p className="text-secondary mb-3">
                Precio actual: <strong>${analysis.current_price.toFixed(2)}</strong>
              </p>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                <div>
                  <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
                    CRITERIOS GRAHAM
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
                    {analysis.graham_criteria.overall_score} / 5
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
                    CRITERIOS BUFFETT
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
                    {analysis.buffett_criteria.overall_score} / 4
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
                    MARGEN DE SEGURIDAD
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '700', color: analysis.dcf_valuation.meets_minimum_margin ? '#10b981' : '#ef4444' }}>
                    {analysis.dcf_valuation.margin_of_safety_percentage.toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>
                    NIVEL DE RIESGO
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
                    {analysis.risk_analysis.overall_risk_level}
                  </div>
                </div>
              </div>
            </div>

            {/* Expandable Sections */}
            <div className="mt-3">
              <h2 style={{ marginBottom: '1rem', fontSize: '1.75rem' }}>Análisis Detallado</h2>

              {/* Lo Básico - Métricas Clave con Explicaciones */}
              <ExpandableSection title="📚 Lo Básico - Métricas Principales" defaultExpanded={true}>
                <p className="text-secondary mb-3">
                  Estas son las métricas más importantes para value investing. Cada una tiene una
                  explicación detallada para que entiendas exactamente qué significan y por qué importan.
                </p>
                {analysis.metric_explanations.map((explanation, index) => (
                  <ExplanationCard key={index} explanation={explanation} />
                ))}
              </ExpandableSection>

              {/* Criterios de Benjamin Graham */}
              <ExpandableSection title="📖 Criterios de Benjamin Graham" defaultExpanded={false}>
                <GrahamCriteriaSection criteria={analysis.graham_criteria} />
              </ExpandableSection>

              {/* Criterios de Warren Buffett */}
              <ExpandableSection title="💼 Criterios de Warren Buffett" defaultExpanded={false}>
                <BuffettCriteriaSection criteria={analysis.buffett_criteria} />
              </ExpandableSection>

              {/* Valoración Intrínseca */}
              <ExpandableSection title="💰 Valoración Intrínseca y Margen de Seguridad" defaultExpanded={false}>
                <ValuationSection
                  dcf={analysis.dcf_valuation}
                  multiples={analysis.multiples_valuation}
                />
              </ExpandableSection>

              {/* Análisis de Riesgo */}
              <ExpandableSection title="⚠️ Análisis de Riesgo" defaultExpanded={false}>
                <RiskSection risk={analysis.risk_analysis} />
              </ExpandableSection>

              {/* Fortalezas y Debilidades */}
              <ExpandableSection title="✅ Fortalezas y ❌ Debilidades" defaultExpanded={false}>
                <div>
                  <h3 style={{ marginBottom: '1rem', color: '#065f46' }}>✅ Principales Fortalezas</h3>
                  {analysis.strengths.length > 0 ? (
                    <ul className="strength-list">
                      {analysis.strengths.map((strength, index) => (
                        <li key={index}>{strength}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-secondary">No se identificaron fortalezas significativas.</p>
                  )}

                  <h3 style={{ marginTop: '2rem', marginBottom: '1rem', color: '#991b1b' }}>
                    ❌ Principales Debilidades
                  </h3>
                  {analysis.weaknesses.length > 0 ? (
                    <ul className="weakness-list">
                      {analysis.weaknesses.map((weakness, index) => (
                        <li key={index}>{weakness}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-secondary">No se identificaron debilidades significativas.</p>
                  )}
                </div>
              </ExpandableSection>

              {/* Recomendación Final */}
              <ExpandableSection title="📋 Recomendación Final Detallada" defaultExpanded={true}>
                <div style={{ whiteSpace: 'pre-line', lineHeight: '1.8' }}>
                  {analysis.final_recommendation_text}
                </div>
              </ExpandableSection>
            </div>
          </div>
        )}

        {/* Initial State - No Analysis Yet */}
        {!analysis && !isLoading && !error && (
          <div className="card text-center" style={{ padding: '3rem', marginTop: '2rem' }}>
            <h2 style={{ marginBottom: '1rem' }}>Comienza tu Análisis</h2>
            <p className="text-secondary" style={{ fontSize: '1.1rem', maxWidth: '600px', margin: '0 auto' }}>
              Ingresa el ticker de una acción para obtener un análisis completo de value investing
              con explicaciones paso a paso. Perfecto para principiantes que quieren aprender a
              invertir como Benjamin Graham y Warren Buffett.
            </p>
            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
              <button className="badge badge-neutral" style={{ cursor: 'pointer', padding: '0.75rem 1.5rem', fontSize: '1rem' }} onClick={() => handleSearch('AAPL')}>
                Probar con AAPL
              </button>
              <button className="badge badge-neutral" style={{ cursor: 'pointer', padding: '0.75rem 1.5rem', fontSize: '1rem' }} onClick={() => handleSearch('MSFT')}>
                Probar con MSFT
              </button>
              <button className="badge badge-neutral" style={{ cursor: 'pointer', padding: '0.75rem 1.5rem', fontSize: '1rem' }} onClick={() => handleSearch('KO')}>
                Probar con KO
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{
        textAlign: 'center',
        padding: '2rem',
        marginTop: '4rem',
        borderTop: '1px solid var(--color-border)',
        color: 'var(--color-text-secondary)'
      }}>
        <p>
          <strong>Value Investing Analyzer</strong> - Herramienta educativa para aprender value investing
        </p>
        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
          Basado en los principios de Benjamin Graham y Warren Buffett
        </p>
        <p style={{ fontSize: '0.875rem', marginTop: '1rem', fontStyle: 'italic' }}>
          ⚠️ Esta herramienta es solo para fines educativos. Siempre realiza tu propia investigación
          antes de invertir y consulta con un asesor financiero profesional.
        </p>
      </footer>
    </div>
  );
}

export default App;
