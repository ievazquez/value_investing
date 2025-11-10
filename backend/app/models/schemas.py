"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum

class RecommendationType(str, Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    AVOID = "AVOID"

class CriteriaStatus(str, Enum):
    PASS = "PASS"
    NEUTRAL = "NEUTRAL"
    FAIL = "FAIL"

class MetricExplanation(BaseModel):
    """Detailed explanation of a financial metric"""
    metric_name: str
    simple_definition: str
    why_important: str
    formula: str
    calculated_value: float
    formatted_value: str
    numeric_example: str
    sector_comparison: Optional[str] = None
    interpretation: str
    status: CriteriaStatus

class GrahamCriteria(BaseModel):
    """Benjamin Graham's value investing criteria"""
    pe_ratio: float
    pe_ratio_pass: bool
    pb_ratio: float
    pb_ratio_pass: bool
    debt_to_equity: float
    debt_to_equity_pass: bool
    current_ratio: float
    current_ratio_pass: bool
    earnings_growth_consistent: bool
    overall_score: int = Field(ge=0, le=5)

class BuffettCriteria(BaseModel):
    """Warren Buffett's value investing criteria"""
    roe: float
    roe_pass: bool
    operating_margin: float
    operating_margin_stable: bool
    free_cash_flow: float
    fcf_positive: bool
    competitive_advantage: str
    overall_score: int = Field(ge=0, le=4)

class ValuationResult(BaseModel):
    """Valuation calculation results"""
    method: str
    intrinsic_value: float
    current_price: float
    margin_of_safety: float
    margin_of_safety_percentage: float
    meets_minimum_margin: bool
    scenario_optimistic: Optional[float] = None
    scenario_base: Optional[float] = None
    scenario_pessimistic: Optional[float] = None

class RiskAnalysis(BaseModel):
    """Risk assessment results"""
    volatility: float
    beta: float
    volatility_explanation: str
    debt_coverage_ratio: float
    debt_risk_explanation: str
    concentration_risk: Optional[str] = None
    permanent_loss_risks: List[str]
    overall_risk_level: str  # "LOW", "MEDIUM", "HIGH"

class StockAnalysis(BaseModel):
    """Complete stock analysis result"""
    ticker: str
    company_name: str
    current_price: float
    recommendation: RecommendationType
    overall_score: float = Field(ge=0, le=10)

    # Criteria
    graham_criteria: GrahamCriteria
    buffett_criteria: BuffettCriteria

    # Valuations
    dcf_valuation: ValuationResult
    multiples_valuation: ValuationResult

    # Risk
    risk_analysis: RiskAnalysis

    # Explanations
    metric_explanations: List[MetricExplanation]

    # Summary
    strengths: List[str]
    weaknesses: List[str]
    final_recommendation_text: str

class StockSearchResult(BaseModel):
    """Stock search result"""
    ticker: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None

class FinancialData(BaseModel):
    """Historical financial data"""
    ticker: str
    years: List[int]
    revenue: List[float]
    net_income: List[float]
    total_assets: List[float]
    total_liabilities: List[float]
    shareholders_equity: List[float]
    operating_cash_flow: List[float]
    free_cash_flow: List[float]
