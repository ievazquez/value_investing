"""
Risk Analysis Calculator
Evaluates investment risks including volatility, debt, and permanent loss risks
"""

from typing import Dict, List
import numpy as np
import pandas as pd

class RiskCalculator:
    """Calculator for risk analysis"""

    # Risk thresholds
    HIGH_VOLATILITY_THRESHOLD = 0.30  # 30% annual volatility
    HIGH_BETA_THRESHOLD = 1.5
    LOW_DEBT_COVERAGE_THRESHOLD = 3.0
    HIGH_DEBT_TO_EQUITY_THRESHOLD = 100  # 100%

    @staticmethod
    def calculate_volatility(price_history: pd.DataFrame) -> float:
        """
        Calculate historical volatility (standard deviation of returns)
        """
        if price_history.empty or len(price_history) < 2:
            return 0

        # Calculate daily returns
        prices = price_history['Close']
        returns = prices.pct_change().dropna()

        # Calculate annualized volatility
        daily_volatility = returns.std()
        annual_volatility = daily_volatility * np.sqrt(252)  # 252 trading days

        return annual_volatility

    @staticmethod
    def assess_volatility_risk(volatility: float, beta: float) -> str:
        """
        Provide explanation of volatility risk
        """
        if volatility > RiskCalculator.HIGH_VOLATILITY_THRESHOLD:
            risk_level = "ALTO"
            if beta > RiskCalculator.HIGH_BETA_THRESHOLD:
                explanation = (
                    f"Esta acción tiene alta volatilidad ({volatility:.1%}) y un beta de {beta:.2f}. "
                    f"Esto significa que cuando el mercado sube 10%, esta acción tiende a subir {beta*10:.1f}%. "
                    f"También significa mayor riesgo a la baja. La acción puede tener cambios bruscos de precio."
                )
            else:
                explanation = (
                    f"Esta acción tiene alta volatilidad ({volatility:.1%}) pero un beta moderado de {beta:.2f}. "
                    f"Los precios pueden fluctuar significativamente, incluso si el mercado general está estable."
                )
        elif volatility > 0.15:
            risk_level = "MEDIO"
            explanation = (
                f"Esta acción tiene volatilidad moderada ({volatility:.1%}) y un beta de {beta:.2f}. "
                f"Los movimientos de precio son típicos para acciones. Habrá fluctuaciones normales."
            )
        else:
            risk_level = "BAJO"
            explanation = (
                f"Esta acción tiene baja volatilidad ({volatility:.1%}) y un beta de {beta:.2f}. "
                f"Los precios tienden a ser más estables que el mercado general. Menos riesgo de grandes caídas."
            )

        return f"{risk_level}: {explanation}"

    @staticmethod
    def calculate_debt_coverage(operating_income: float, interest_expense: float) -> float:
        """
        Calculate interest coverage ratio
        Shows how many times the company can cover its interest payments
        """
        if interest_expense <= 0:
            return float('inf')  # No debt or no interest

        return operating_income / interest_expense

    @staticmethod
    def assess_debt_risk(metrics: Dict) -> str:
        """
        Assess debt-related risks
        """
        debt_to_equity = metrics.get('debt_to_equity', 0)
        total_debt = metrics.get('total_debt', 0)
        operating_income = metrics.get('historical_operating_income', [0])[-1] if metrics.get('historical_operating_income') else 0

        # Estimate interest expense (simplified)
        interest_expense = total_debt * 0.05  # Assume 5% average interest rate

        coverage_ratio = RiskCalculator.calculate_debt_coverage(operating_income, interest_expense)

        if debt_to_equity > RiskCalculator.HIGH_DEBT_TO_EQUITY_THRESHOLD:
            risk_level = "ALTO"
            if coverage_ratio < RiskCalculator.LOW_DEBT_COVERAGE_THRESHOLD:
                explanation = (
                    f"RIESGO ALTO: La empresa tiene una relación deuda/capital de {debt_to_equity:.1f}% y "
                    f"solo gana ${coverage_ratio:.1f} por cada $1 que debe pagar en intereses. "
                    f"Esto significa que la empresa está muy endeudada y podría tener problemas para pagar sus deudas "
                    f"si el negocio empeora."
                )
            else:
                explanation = (
                    f"RIESGO MEDIO-ALTO: La empresa tiene alta deuda ({debt_to_equity:.1f}% deuda/capital) pero "
                    f"genera suficientes ingresos para cubrirla ({coverage_ratio:.1f}x cobertura). "
                    f"Aún así, el alto endeudamiento limita la flexibilidad financiera."
                )
        elif debt_to_equity > 50:
            risk_level = "MEDIO"
            explanation = (
                f"RIESGO MODERADO: La empresa tiene una relación deuda/capital de {debt_to_equity:.1f}%. "
                f"Gana ${coverage_ratio:.1f} por cada $1 en intereses. "
                f"El nivel de deuda es manejable pero debe monitorearse."
            )
        else:
            risk_level = "BAJO"
            explanation = (
                f"RIESGO BAJO: La empresa tiene baja deuda ({debt_to_equity:.1f}% deuda/capital) y "
                f"gana ${coverage_ratio:.1f} por cada $1 en intereses. "
                f"Esto es saludable porque tiene capacidad de sobra para pagar sus deudas."
            )

        return explanation

    @staticmethod
    def identify_permanent_loss_risks(metrics: Dict) -> List[str]:
        """
        Identify risks that could cause permanent loss of capital
        These are the most important risks for value investors
        """
        risks = []

        # 1. Declining business
        net_income_history = metrics.get('historical_net_income', [])
        if len(net_income_history) >= 3:
            recent_trend = net_income_history[-1] < net_income_history[-3]
            if recent_trend and net_income_history[-1] < 0:
                risks.append(
                    "Negocio en declive: Las ganancias han disminuido y ahora son negativas. "
                    "Esto podría indicar un problema fundamental en el modelo de negocio."
                )

        # 2. High debt with declining earnings
        debt_to_equity = metrics.get('debt_to_equity', 0)
        if debt_to_equity > 80 and len(net_income_history) >= 2:
            if net_income_history[-1] < net_income_history[-2] * 0.8:
                risks.append(
                    "Combinación peligrosa: Alta deuda con ganancias en descenso. "
                    "La empresa podría no poder pagar sus deudas si continúa esta tendencia."
                )

        # 3. Negative free cash flow
        fcf = metrics.get('free_cash_flow', 0)
        if fcf < 0:
            risks.append(
                "Flujo de caja negativo: La empresa gasta más dinero del que genera. "
                "Eventualmente necesitará financiamiento externo o reducir operaciones."
            )

        # 4. Very high P/E ratio (overpaying risk)
        pe_ratio = metrics.get('trailing_pe', 0)
        if pe_ratio > 40:
            risks.append(
                f"Valoración muy alta: P/E de {pe_ratio:.1f} es extremadamente elevado. "
                f"Estás pagando mucho por cada dólar de ganancias. Cualquier decepción podría "
                f"causar una caída significativa del precio."
            )

        # 5. Poor liquidity
        current_ratio = metrics.get('current_ratio', 0)
        if current_ratio < 1.0:
            risks.append(
                f"Problemas de liquidez: Ratio corriente de {current_ratio:.2f} significa que la empresa "
                f"tiene más deudas a corto plazo que activos líquidos. Podría tener problemas para "
                f"pagar sus obligaciones inmediatas."
            )

        # 6. Cyclical industry risk
        sector = metrics.get('sector', '')
        cyclical_sectors = ['Energy', 'Basic Materials', 'Consumer Cyclical', 'Industrials']
        if sector in cyclical_sectors:
            risks.append(
                f"Industria cíclica: El sector {sector} es sensible a ciclos económicos. "
                f"Durante recesiones, estas empresas pueden sufrir caídas significativas en ganancias."
            )

        if not risks:
            risks.append(
                "Riesgos limitados detectados: No se identificaron riesgos graves de pérdida permanente "
                "en el análisis básico. Sin embargo, siempre investiga factores cualitativos y específicos "
                "de la industria."
            )

        return risks

    @staticmethod
    def calculate_overall_risk_level(metrics: Dict, price_history: pd.DataFrame) -> str:
        """
        Calculate overall risk level: LOW, MEDIUM, HIGH
        """
        risk_score = 0

        # Volatility risk
        volatility = RiskCalculator.calculate_volatility(price_history)
        if volatility > 0.30:
            risk_score += 2
        elif volatility > 0.15:
            risk_score += 1

        # Debt risk
        debt_to_equity = metrics.get('debt_to_equity', 0)
        if debt_to_equity > 100:
            risk_score += 2
        elif debt_to_equity > 50:
            risk_score += 1

        # Profitability risk
        profit_margin = metrics.get('profit_margins', 0)
        if profit_margin < 0:
            risk_score += 2
        elif profit_margin < 0.05:
            risk_score += 1

        # Cash flow risk
        fcf = metrics.get('free_cash_flow', 0)
        if fcf < 0:
            risk_score += 1

        # Determine overall level
        if risk_score >= 5:
            return "HIGH"
        elif risk_score >= 3:
            return "MEDIUM"
        else:
            return "LOW"

    @staticmethod
    def perform_risk_analysis(metrics: Dict, price_history: pd.DataFrame) -> Dict:
        """
        Perform complete risk analysis
        """
        # Calculate metrics
        volatility = RiskCalculator.calculate_volatility(price_history)
        beta = metrics.get('beta', 1.0)

        # Get assessments
        volatility_explanation = RiskCalculator.assess_volatility_risk(volatility, beta)
        debt_explanation = RiskCalculator.assess_debt_risk(metrics)
        permanent_loss_risks = RiskCalculator.identify_permanent_loss_risks(metrics)
        overall_risk = RiskCalculator.calculate_overall_risk_level(metrics, price_history)

        # Calculate debt coverage
        operating_income = metrics.get('historical_operating_income', [0])[-1] if metrics.get('historical_operating_income') else 0
        total_debt = metrics.get('total_debt', 0)
        interest_expense = total_debt * 0.05
        debt_coverage = RiskCalculator.calculate_debt_coverage(operating_income, interest_expense)

        return {
            'volatility': volatility,
            'beta': beta,
            'volatility_explanation': volatility_explanation,
            'debt_coverage_ratio': debt_coverage if debt_coverage != float('inf') else 999,
            'debt_risk_explanation': debt_explanation,
            'permanent_loss_risks': permanent_loss_risks,
            'overall_risk_level': overall_risk,
        }
