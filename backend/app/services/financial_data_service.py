"""
Financial Data Service
Retrieves financial data from Yahoo Finance using yfinance
"""

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class FinancialDataService:
    """Service for fetching financial data"""

    @staticmethod
    def search_stock(query: str) -> List[Dict]:
        """
        Search for stocks by ticker or company name
        Returns a list of matching stocks
        """
        try:
            ticker = yf.Ticker(query.upper())
            info = ticker.info

            if not info or 'symbol' not in info:
                return []

            return [{
                'ticker': info.get('symbol', query.upper()),
                'name': info.get('longName', info.get('shortName', 'Unknown')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A')
            }]
        except Exception as e:
            print(f"Error searching stock: {e}")
            return []

    @staticmethod
    def get_stock_info(ticker: str) -> Optional[Dict]:
        """Get basic stock information"""
        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info
            return info
        except Exception as e:
            print(f"Error getting stock info: {e}")
            return None

    @staticmethod
    def get_historical_prices(ticker: str, period: str = "5y") -> pd.DataFrame:
        """Get historical price data"""
        try:
            stock = yf.Ticker(ticker.upper())
            history = stock.history(period=period)
            return history
        except Exception as e:
            print(f"Error getting historical prices: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_financial_statements(ticker: str) -> Dict:
        """
        Get financial statements (Income Statement, Balance Sheet, Cash Flow)
        Returns data for the last 5 years
        """
        try:
            stock = yf.Ticker(ticker.upper())

            # Get annual financial statements
            income_stmt = stock.financials  # Annual income statement
            balance_sheet = stock.balance_sheet  # Annual balance sheet
            cash_flow = stock.cashflow  # Annual cash flow statement

            return {
                'income_statement': income_stmt,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow
            }
        except Exception as e:
            print(f"Error getting financial statements: {e}")
            return {
                'income_statement': pd.DataFrame(),
                'balance_sheet': pd.DataFrame(),
                'cash_flow': pd.DataFrame()
            }

    @staticmethod
    def get_key_metrics(ticker: str) -> Dict:
        """
        Extract key financial metrics from financial statements
        """
        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info

            # Get financial statements
            statements = FinancialDataService.get_financial_statements(ticker)
            income_stmt = statements['income_statement']
            balance_sheet = statements['balance_sheet']
            cash_flow = statements['cash_flow']

            # Extract key metrics
            metrics = {
                # Current data from info
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'trailing_pe': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'price_to_book': info.get('priceToBook', 0),
                'beta': info.get('beta', 0),

                # Profitability metrics
                'profit_margins': info.get('profitMargins', 0),
                'operating_margins': info.get('operatingMargins', 0),
                'return_on_assets': info.get('returnOnAssets', 0),
                'return_on_equity': info.get('returnOnEquity', 0),

                # Financial health
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'total_debt': info.get('totalDebt', 0),
                'total_cash': info.get('totalCash', 0),

                # Cash flow
                'free_cash_flow': info.get('freeCashflow', 0),
                'operating_cash_flow': info.get('operatingCashflow', 0),

                # Growth
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),

                # Company info
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'company_name': info.get('longName', ticker),
            }

            # Historical data arrays for analysis
            if not income_stmt.empty:
                metrics['historical_revenue'] = income_stmt.loc['Total Revenue'].tolist() if 'Total Revenue' in income_stmt.index else []
                metrics['historical_net_income'] = income_stmt.loc['Net Income'].tolist() if 'Net Income' in income_stmt.index else []
                metrics['historical_operating_income'] = income_stmt.loc['Operating Income'].tolist() if 'Operating Income' in income_stmt.index else []

            if not balance_sheet.empty:
                metrics['historical_total_assets'] = balance_sheet.loc['Total Assets'].tolist() if 'Total Assets' in balance_sheet.index else []
                metrics['historical_total_liabilities'] = balance_sheet.loc['Total Liabilities Net Minority Interest'].tolist() if 'Total Liabilities Net Minority Interest' in balance_sheet.index else []
                metrics['historical_stockholder_equity'] = balance_sheet.loc['Stockholders Equity'].tolist() if 'Stockholders Equity' in balance_sheet.index else []

            if not cash_flow.empty:
                metrics['historical_operating_cf'] = cash_flow.loc['Operating Cash Flow'].tolist() if 'Operating Cash Flow' in cash_flow.index else []
                metrics['historical_free_cf'] = cash_flow.loc['Free Cash Flow'].tolist() if 'Free Cash Flow' in cash_flow.index else []

            return metrics

        except Exception as e:
            print(f"Error getting key metrics: {e}")
            return {}

    @staticmethod
    def get_sector_averages(sector: str) -> Dict:
        """
        Get average metrics for a sector
        Note: This is a simplified version. In production, you'd want to
        calculate this from multiple companies in the sector.
        """
        # Default sector averages (these are approximate market averages)
        sector_defaults = {
            'Technology': {'pe_ratio': 25, 'pb_ratio': 5, 'roe': 0.20, 'debt_to_equity': 30},
            'Financial Services': {'pe_ratio': 12, 'pb_ratio': 1.2, 'roe': 0.12, 'debt_to_equity': 150},
            'Healthcare': {'pe_ratio': 20, 'pb_ratio': 4, 'roe': 0.15, 'debt_to_equity': 40},
            'Consumer Cyclical': {'pe_ratio': 18, 'pb_ratio': 3, 'roe': 0.18, 'debt_to_equity': 50},
            'Consumer Defensive': {'pe_ratio': 20, 'pb_ratio': 5, 'roe': 0.25, 'debt_to_equity': 45},
            'Energy': {'pe_ratio': 15, 'pb_ratio': 1.5, 'roe': 0.08, 'debt_to_equity': 60},
            'Industrials': {'pe_ratio': 18, 'pb_ratio': 3, 'roe': 0.15, 'debt_to_equity': 55},
            'Basic Materials': {'pe_ratio': 16, 'pb_ratio': 1.8, 'roe': 0.12, 'debt_to_equity': 50},
            'Real Estate': {'pe_ratio': 30, 'pb_ratio': 2, 'roe': 0.10, 'debt_to_equity': 100},
            'Utilities': {'pe_ratio': 20, 'pb_ratio': 1.5, 'roe': 0.10, 'debt_to_equity': 80},
            'Communication Services': {'pe_ratio': 22, 'pb_ratio': 3.5, 'roe': 0.18, 'debt_to_equity': 65},
        }

        return sector_defaults.get(sector, {
            'pe_ratio': 18,
            'pb_ratio': 3,
            'roe': 0.15,
            'debt_to_equity': 50
        })
