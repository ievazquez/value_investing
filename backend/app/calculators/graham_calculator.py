"""
Benjamin Graham Value Investing Criteria Calculator
Implements Graham's principles from "The Intelligent Investor"
"""

from typing import Dict, List
import numpy as np

class GrahamCalculator:
    """Calculator for Benjamin Graham's value investing criteria"""

    # Graham's recommended thresholds
    PE_RATIO_THRESHOLD = 15
    PB_RATIO_THRESHOLD = 1.5
    DEBT_TO_EQUITY_THRESHOLD = 50  # 50%
    CURRENT_RATIO_THRESHOLD = 2.0
    MIN_EARNINGS_YEARS = 5

    @staticmethod
    def calculate_pe_ratio(price: float, earnings_per_share: float) -> float:
        """Calculate Price-to-Earnings ratio"""
        if earnings_per_share <= 0:
            return float('inf')
        return price / earnings_per_share

    @staticmethod
    def calculate_pb_ratio(price: float, book_value_per_share: float) -> float:
        """Calculate Price-to-Book ratio"""
        if book_value_per_share <= 0:
            return float('inf')
        return price / book_value_per_share

    @staticmethod
    def check_earnings_consistency(net_income_history: List[float]) -> bool:
        """
        Check if company has consistent positive earnings
        Graham requires positive earnings in at least 8 of the last 10 years
        We'll use 5 years and require at least 4 positive years
        """
        if not net_income_history or len(net_income_history) < 3:
            return False

        positive_years = sum(1 for income in net_income_history if income > 0)
        required_positive = max(len(net_income_history) - 1, 3)

        return positive_years >= required_positive

    @staticmethod
    def check_earnings_growth(net_income_history: List[float]) -> bool:
        """
        Check if earnings have grown over time
        Compare first third average to last third average
        """
        if not net_income_history or len(net_income_history) < 3:
            return False

        # Split into periods
        third = len(net_income_history) // 3
        early_period = net_income_history[:third] if third > 0 else net_income_history[:1]
        late_period = net_income_history[-third:] if third > 0 else net_income_history[-1:]

        early_avg = np.mean(early_period)
        late_avg = np.mean(late_period)

        # Check for growth (late period should be higher)
        return late_avg > early_avg * 1.1  # At least 10% growth

    @staticmethod
    def evaluate_graham_criteria(metrics: Dict) -> Dict:
        """
        Evaluate all Graham criteria and return results with explanations
        """
        pe_ratio = metrics.get('trailing_pe', 0)
        pb_ratio = metrics.get('price_to_book', 0)
        debt_to_equity = metrics.get('debt_to_equity', 0)
        current_ratio = metrics.get('current_ratio', 0)

        # Check earnings consistency
        net_income_history = metrics.get('historical_net_income', [])
        earnings_consistent = GrahamCalculator.check_earnings_consistency(net_income_history)

        # Calculate Graham Score
        criteria_results = {
            'pe_ratio': pe_ratio,
            'pe_ratio_pass': 0 < pe_ratio <= GrahamCalculator.PE_RATIO_THRESHOLD,
            'pb_ratio': pb_ratio,
            'pb_ratio_pass': 0 < pb_ratio <= GrahamCalculator.PB_RATIO_THRESHOLD,
            'debt_to_equity': debt_to_equity,
            'debt_to_equity_pass': debt_to_equity <= GrahamCalculator.DEBT_TO_EQUITY_THRESHOLD,
            'current_ratio': current_ratio,
            'current_ratio_pass': current_ratio >= GrahamCalculator.CURRENT_RATIO_THRESHOLD,
            'earnings_growth_consistent': earnings_consistent,
        }

        # Calculate overall score (0-5)
        score = sum([
            criteria_results['pe_ratio_pass'],
            criteria_results['pb_ratio_pass'],
            criteria_results['debt_to_equity_pass'],
            criteria_results['current_ratio_pass'],
            criteria_results['earnings_growth_consistent']
        ])

        criteria_results['overall_score'] = score

        return criteria_results

    @staticmethod
    def get_graham_score_interpretation(score: int) -> str:
        """Get interpretation of Graham score"""
        if score >= 4:
            return "Excellent - Meets Graham's strict value investing criteria"
        elif score >= 3:
            return "Good - Meets most of Graham's criteria with minor concerns"
        elif score >= 2:
            return "Fair - Meets some criteria but has significant concerns"
        else:
            return "Poor - Does not meet Graham's value investing standards"

    @staticmethod
    def calculate_graham_number(eps: float, book_value_per_share: float) -> float:
        """
        Calculate Graham Number - the fair value according to Graham's formula
        Graham Number = √(22.5 × EPS × Book Value per Share)
        """
        if eps <= 0 or book_value_per_share <= 0:
            return 0

        try:
            graham_number = (22.5 * eps * book_value_per_share) ** 0.5
            return graham_number
        except:
            return 0
