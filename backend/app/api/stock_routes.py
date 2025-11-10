"""
Stock API Routes
Endpoints for stock search and analysis
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.financial_data_service import FinancialDataService
from app.services.analysis_service import AnalysisService
from app.models.schemas import StockAnalysis, StockSearchResult

router = APIRouter()

@router.get("/search", response_model=List[StockSearchResult])
async def search_stocks(
    query: str = Query(..., min_length=1, description="Stock ticker or company name")
):
    """
    Search for stocks by ticker or company name
    """
    try:
        results = FinancialDataService.search_stock(query)
        return [StockSearchResult(**result) for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching stocks: {str(e)}")

@router.get("/analyze/{ticker}", response_model=StockAnalysis)
async def analyze_stock(ticker: str):
    """
    Perform complete value investing analysis on a stock
    Returns detailed analysis with Graham/Buffett criteria, valuations, risk assessment,
    and educational explanations
    """
    try:
        analysis = AnalysisService.analyze_stock(ticker)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing stock: {str(e)}")

@router.get("/info/{ticker}")
async def get_stock_info(ticker: str):
    """
    Get basic stock information
    """
    try:
        info = FinancialDataService.get_stock_info(ticker)
        if not info:
            raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stock info: {str(e)}")
