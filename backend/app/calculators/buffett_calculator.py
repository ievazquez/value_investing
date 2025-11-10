"""
Warren Buffett Value Investing Criteria Calculator
Implements Buffett's quality-focused investment principles
"""

from typing import Dict, List
import numpy as np

class BuffettCalculator:
    """Calculator for Warren Buffett's value investing criteria"""

    # Buffett's quality thresholds
    ROE_THRESHOLD = 0.15  # 15%
    MIN_OPERATING_MARGIN = 0.15  # 15%
    MIN_MARGIN_STABILITY = 0.8  # 80% of years should be above threshold

    @staticmethod
    def calculate_roe(net_income: float, shareholders_equity: float) -> float:
        """Calculate Return on Equity"""
        if shareholders_equity <= 0:
            return 0
        return net_income / shareholders_equity

    @staticmethod
    def check_roe_consistency(net_income_history: List[float],
                               equity_history: List[float]) -> bool:
        """
        Check if ROE is consistently above threshold
        Buffett looks for consistent high returns
        """
        if not net_income_history or not equity_history:
            return False

        if len(net_income_history) != len(equity_history):
            return False

        roe_history = []
        for income, equity in zip(net_income_history, equity_history):
            if equity > 0:
                roe = income / equity
                roe_history.append(roe)

        if not roe_history:
            return False

        # Check what percentage of years had ROE > 15%
        good_years = sum(1 for roe in roe_history if roe >= BuffettCalculator.ROE_THRESHOLD)
        percentage = good_years / len(roe_history)

        return percentage >= BuffettCalculator.MIN_MARGIN_STABILITY

    @staticmethod
    def check_operating_margin_stability(revenue_history: List[float],
                                         operating_income_history: List[float]) -> bool:
        """
        Check if operating margins are stable or improving
        Buffett looks for predictable businesses with pricing power
        """
        if not revenue_history or not operating_income_history:
            return False

        if len(revenue_history) != len(operating_income_history):
            return False

        margins = []
        for revenue, op_income in zip(revenue_history, operating_income_history):
            if revenue > 0:
                margin = op_income / revenue
                margins.append(margin)

        if len(margins) < 3:
            return False

        # Check if margins are generally stable (low volatility)
        margin_std = np.std(margins)
        margin_mean = np.mean(margins)

        # Coefficient of variation should be low for stability
        if margin_mean > 0:
            cv = margin_std / margin_mean
            is_stable = cv < 0.3  # Less than 30% variation
        else:
            is_stable = False

        # Check if recent margins are good
        recent_margins = margins[-2:]  # Last 2 years
        good_margins = all(m >= BuffettCalculator.MIN_OPERATING_MARGIN for m in recent_margins)

        return is_stable and good_margins

    @staticmethod
    def assess_competitive_advantage(metrics: Dict) -> str:
        """
        Assess if company has a competitive advantage (economic moat)
        This is a simplified assessment based on financial metrics
        """
        roe = metrics.get('return_on_equity', 0)
        operating_margin = metrics.get('operating_margins', 0)
        profit_margin = metrics.get('profit_margins', 0)

        # High and consistent returns suggest a moat
        high_roe = roe >= 0.20
        high_margins = operating_margin >= 0.20

        if high_roe and high_margins:
            return "Strong - High returns and margins suggest competitive advantage"
        elif high_roe or high_margins:
            return "Moderate - Some indicators of competitive advantage"
        else:
            return "Weak - Limited evidence of sustainable competitive advantage"

    @staticmethod
    def check_free_cash_flow_quality(fcf_history: List[float],
                                     net_income_history: List[float]) -> bool:
        """
        Check if free cash flow is strong relative to earnings
        Buffett prefers businesses that convert earnings to cash
        """
        if not fcf_history or not net_income_history:
            return False

        # Take the minimum length
        min_len = min(len(fcf_history), len(net_income_history))
        fcf_history = fcf_history[:min_len]
        net_income_history = net_income_history[:min_len]

        # Calculate FCF to Net Income ratios
        ratios = []
        for fcf, ni in zip(fcf_history, net_income_history):
            if ni > 0:
                ratio = fcf / ni
                ratios.append(ratio)

        if not ratios:
            return False

        # Good quality: FCF is at least 80% of net income on average
        avg_ratio = np.mean(ratios)
        return avg_ratio >= 0.8

    @staticmethod
    def evaluate_buffett_criteria(metrics: Dict) -> Dict:
        """
        Evaluate all Buffett criteria and return results
        """
        roe = metrics.get('return_on_equity', 0)
        operating_margin = metrics.get('operating_margins', 0)
        free_cash_flow = metrics.get('free_cash_flow', 0)

        # Check consistency
        net_income_history = metrics.get('historical_net_income', [])
        equity_history = metrics.get('historical_stockholder_equity', [])
        roe_consistent = BuffettCalculator.check_roe_consistency(
            net_income_history, equity_history
        )

        # Check margin stability
        revenue_history = metrics.get('historical_revenue', [])
        op_income_history = metrics.get('historical_operating_income', [])
        margin_stable = BuffettCalculator.check_operating_margin_stability(
            revenue_history, op_income_history
        )

        # Check FCF quality
        fcf_history = metrics.get('historical_free_cf', [])
        fcf_quality = BuffettCalculator.check_free_cash_flow_quality(
            fcf_history, net_income_history
        )

        # Assess competitive advantage
        competitive_advantage = BuffettCalculator.assess_competitive_advantage(metrics)

        criteria_results = {
            'roe': roe,
            'roe_pass': roe >= BuffettCalculator.ROE_THRESHOLD and roe_consistent,
            'operating_margin': operating_margin,
            'operating_margin_stable': margin_stable,
            'free_cash_flow': free_cash_flow,
            'fcf_positive': fcf_quality and free_cash_flow > 0,
            'competitive_advantage': competitive_advantage,
        }

        # Calculate overall score (0-4)
        score = sum([
            criteria_results['roe_pass'],
            criteria_results['operating_margin_stable'],
            criteria_results['fcf_positive'],
            'Strong' in criteria_results['competitive_advantage']
        ])

        criteria_results['overall_score'] = score

        return criteria_results

    @staticmethod
    def get_buffett_score_interpretation(score: int) -> str:
        """Get interpretation of Buffett score"""
        if score >= 3:
            return "Excellent - High-quality business that Buffett would consider"
        elif score >= 2:
            return "Good - Quality business with some attractive characteristics"
        elif score >= 1:
            return "Fair - Average business, may lack competitive advantages"
        else:
            return "Poor - Low-quality business, not suitable for value investing"
