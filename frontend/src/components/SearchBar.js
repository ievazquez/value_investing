import React, { useState } from 'react';

function SearchBar({ onSearch, isLoading }) {
  const [ticker, setTicker] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ticker.trim()) {
      onSearch(ticker.trim().toUpperCase());
    }
  };

  return (
    <div className="search-section">
      <form onSubmit={handleSubmit} className="search-box">
        <input
          type="text"
          className="search-input"
          placeholder="Ingresa el ticker (ej: AAPL, MSFT, TSLA)..."
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="search-button"
          disabled={isLoading || !ticker.trim()}
        >
          {isLoading ? 'Analizando...' : 'Analizar'}
        </button>
      </form>
      <div className="text-center mt-2 text-secondary">
        <small>
          Ejemplos: AAPL (Apple), MSFT (Microsoft), KO (Coca-Cola), JPM (JPMorgan)
        </small>
      </div>
    </div>
  );
}

export default SearchBar;
