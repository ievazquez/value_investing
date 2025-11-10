/**
 * API Service
 * Handles all API calls to the backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const stockAPI = {
  /**
   * Search for stocks by ticker or name
   */
  searchStocks: async (query) => {
    try {
      const response = await api.get(`/search`, {
        params: { query }
      });
      return response.data;
    } catch (error) {
      console.error('Error searching stocks:', error);
      throw error;
    }
  },

  /**
   * Get complete analysis for a stock
   */
  analyzeStock: async (ticker) => {
    try {
      const response = await api.get(`/analyze/${ticker}`);
      return response.data;
    } catch (error) {
      console.error('Error analyzing stock:', error);
      throw error;
    }
  },

  /**
   * Get basic stock info
   */
  getStockInfo: async (ticker) => {
    try {
      const response = await api.get(`/info/${ticker}`);
      return response.data;
    } catch (error) {
      console.error('Error getting stock info:', error);
      throw error;
    }
  },
};

export default api;
