"""
Valuation Calculator
Implements DCF (Discounted Cash Flow) and Comparable Multiples valuation methods
"""

from typing import Dict, List, Tuple
import numpy as np

class ValuationCalculator:
    """Calculator for stock valuation"""

    # Default assumptions
    DEFAULT_RISK_FREE_RATE = 0.04  # 4% (approximate 10-year Treasury rate)
    DEFAULT_MARKET_RETURN = 0.10  # 10% (historical market average)
    DEFAULT_TERMINAL_GROWTH_RATE = 0.025  # 2.5% (conservative perpetual growth)
    DEFAULT_PROJECTION_YEARS = 5

    @staticmethod
    def calculate_wacc(metrics: Dict) -> float:
        """
        Calculate Weighted Average Cost of Capital (WACC)
        WACC = (E/V × Re) + (D/V × Rd × (1-Tc))
        """
        # Get values
        market_cap = metrics.get('market_cap', 0)
        total_debt = metrics.get('total_debt', 0)
        beta = metrics.get('beta', 1.0)
        tax_rate = 0.21  # Approximate corporate tax rate

        # Calculate cost of equity using CAPM
        risk_free_rate = ValuationCalculator.DEFAULT_RISK_FREE_RATE
        market_return = ValuationCalculator.DEFAULT_MARKET_RETURN
        cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)

        # Estimate cost of debt (simplified)
        cost_of_debt = 0.05  # 5% average

        # Calculate weights
        total_value = market_cap + total_debt
        if total_value == 0:
            return cost_of_equity

        equity_weight = market_cap / total_value
        debt_weight = total_debt / total_value

        # Calculate WACC
        wacc = (equity_weight * cost_of_equity +
                debt_weight * cost_of_debt * (1 - tax_rate))

        return max(wacc, 0.08)  # Minimum 8% discount rate

    @staticmethod
    def project_free_cash_flows(base_fcf: float, growth_rates: List[float]) -> List[float]:
        """
        Project future free cash flows based on growth rates
        """
        if base_fcf <= 0:
            return []

        projected_fcf = []
        current_fcf = base_fcf

        for growth_rate in growth_rates:
            current_fcf = current_fcf * (1 + growth_rate)
            projected_fcf.append(current_fcf)

        return projected_fcf

    @staticmethod
    def calculate_terminal_value(final_fcf: float, wacc: float,
                                 terminal_growth_rate: float) -> float:
        """
        Calculate terminal value using perpetuity growth model
        Terminal Value = FCF(final year) × (1 + g) / (WACC - g)
        """
        if wacc <= terminal_growth_rate:
            terminal_growth_rate = wacc * 0.5  # Adjust if needed

        terminal_value = final_fcf * (1 + terminal_growth_rate) / (wacc - terminal_growth_rate)
        return terminal_value

    @staticmethod
    def discount_cash_flows(cash_flows: List[float], wacc: float) -> float:
        """
        Discount future cash flows to present value
        """
        present_value = 0
        for year, cf in enumerate(cash_flows, start=1):
            discount_factor = (1 + wacc) ** year
            present_value += cf / discount_factor

        return present_value

    @staticmethod
    def calculate_dcf_valuation(metrics: Dict, scenario: str = "base") -> Dict:
        """
        Calculate intrinsic value using DCF method
        Returns valuation result with three scenarios
        """
        # Get base free cash flow
        base_fcf = metrics.get('free_cash_flow', 0)
        if base_fcf <= 0:
            # Try to estimate from operating cash flow
            operating_cf = metrics.get('operating_cash_flow', 0)
            base_fcf = operating_cf * 0.8  # Rough estimate

        if base_fcf <= 0:
            return {
                'intrinsic_value': 0,
                'scenario': scenario,
                'error': 'Unable to calculate DCF - insufficient cash flow data'
            }

        # Get number of shares
        market_cap = metrics.get('market_cap', 0)
        current_price = metrics.get('current_price', 0)
        if current_price > 0:
            shares_outstanding = market_cap / current_price
        else:
            shares_outstanding = 1

        # Calculate WACC
        wacc = ValuationCalculator.calculate_wacc(metrics)

        # Estimate growth rate from historical data
        revenue_growth = metrics.get('revenue_growth', 0)
        earnings_growth = metrics.get('earnings_growth', 0)
        base_growth_rate = (revenue_growth + earnings_growth) / 2 if revenue_growth and earnings_growth else 0.05

        # Define scenarios
        if scenario == "optimistic":
            growth_rates = [base_growth_rate * 1.5] * 5
            terminal_growth = ValuationCalculator.DEFAULT_TERMINAL_GROWTH_RATE * 1.2
        elif scenario == "pessimistic":
            growth_rates = [base_growth_rate * 0.5] * 5
            terminal_growth = ValuationCalculator.DEFAULT_TERMINAL_GROWTH_RATE * 0.8
        else:  # base
            growth_rates = [base_growth_rate] * 5
            terminal_growth = ValuationCalculator.DEFAULT_TERMINAL_GROWTH_RATE

        # Project cash flows
        projected_fcf = ValuationCalculator.project_free_cash_flows(base_fcf, growth_rates)

        if not projected_fcf:
            return {'intrinsic_value': 0, 'scenario': scenario, 'error': 'Unable to project cash flows'}

        # Calculate terminal value
        terminal_value = ValuationCalculator.calculate_terminal_value(
            projected_fcf[-1], wacc, terminal_growth
        )

        # Discount cash flows
        pv_projected_fcf = ValuationCalculator.discount_cash_flows(projected_fcf, wacc)
        pv_terminal_value = terminal_value / ((1 + wacc) ** len(projected_fcf))

        # Calculate enterprise value
        enterprise_value = pv_projected_fcf + pv_terminal_value

        # Adjust for cash and debt
        total_cash = metrics.get('total_cash', 0)
        total_debt = metrics.get('total_debt', 0)
        equity_value = enterprise_value + total_cash - total_debt

        # Calculate per-share value
        intrinsic_value_per_share = equity_value / shares_outstanding if shares_outstanding > 0 else 0

        return {
            'intrinsic_value': max(intrinsic_value_per_share, 0),
            'scenario': scenario,
            'enterprise_value': enterprise_value,
            'equity_value': equity_value,
            'wacc': wacc,
            'growth_rate': base_growth_rate,
            'terminal_growth': terminal_growth,
            'projected_fcf': projected_fcf,
        }

    @staticmethod
    def calculate_multiples_valuation(metrics: Dict, sector_averages: Dict) -> Dict:
        """
        Calculate intrinsic value using comparable multiples method
        Uses P/E and P/B ratios compared to sector averages
        """
        # Get company metrics
        current_price = metrics.get('current_price', 0)
        trailing_pe = metrics.get('trailing_pe', 0)
        pb_ratio = metrics.get('price_to_book', 0)

        # Get sector averages
        sector_pe = sector_averages.get('pe_ratio', 18)
        sector_pb = sector_averages.get('pb_ratio', 3)

        # Calculate implied values
        values = []

        # P/E based valuation
        if trailing_pe > 0 and current_price > 0:
            eps = current_price / trailing_pe
            pe_based_value = eps * sector_pe
            values.append(pe_based_value)

        # P/B based valuation
        if pb_ratio > 0 and current_price > 0:
            book_value = current_price / pb_ratio
            pb_based_value = book_value * sector_pb
            values.append(pb_based_value)

        # Average the valuations
        if values:
            intrinsic_value = np.mean(values)
        else:
            intrinsic_value = 0

        return {
            'intrinsic_value': intrinsic_value,
            'pe_based_value': values[0] if len(values) > 0 else 0,
            'pb_based_value': values[1] if len(values) > 1 else 0,
            'sector_pe': sector_pe,
            'sector_pb': sector_pb,
        }

    @staticmethod
    def calculate_margin_of_safety(intrinsic_value: float, current_price: float) -> Tuple[float, float]:
        """
        Calculate margin of safety
        Margin of Safety = (Intrinsic Value - Current Price) / Intrinsic Value
        """
        if intrinsic_value <= 0:
            return 0, 0

        margin_dollars = intrinsic_value - current_price
        margin_percentage = (margin_dollars / intrinsic_value) * 100

        return margin_dollars, margin_percentage

    @staticmethod
    def meets_minimum_margin(margin_percentage: float, minimum: float = 30) -> bool:
        """
        Check if margin of safety meets the minimum threshold
        Graham recommends at least 30% margin
        """
        return margin_percentage >= minimum
