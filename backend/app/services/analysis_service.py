"""
Stock Analysis Service
Main service that orchestrates the complete value investing analysis
"""

from typing import Dict
from app.services.financial_data_service import FinancialDataService
from app.calculators.graham_calculator import GrahamCalculator
from app.calculators.buffett_calculator import BuffettCalculator
from app.calculators.valuation_calculator import ValuationCalculator
from app.calculators.risk_calculator import RiskCalculator
from app.utils.explanation_generator import ExplanationGenerator
from app.models.schemas import (
    StockAnalysis, GrahamCriteria, BuffettCriteria,
    ValuationResult, RiskAnalysis, RecommendationType,
    MetricExplanation
)

class AnalysisService:
    """Service for performing complete stock analysis"""

    @staticmethod
    def analyze_stock(ticker: str) -> StockAnalysis:
        """
        Perform complete value investing analysis on a stock
        """
        # Get financial data
        metrics = FinancialDataService.get_key_metrics(ticker)
        if not metrics:
            raise ValueError(f"Unable to retrieve data for ticker: {ticker}")

        current_price = metrics.get('current_price', 0)
        if current_price <= 0:
            raise ValueError(f"Invalid price data for ticker: {ticker}")

        # Get sector info for comparisons
        sector = metrics.get('sector', 'Unknown')
        sector_averages = FinancialDataService.get_sector_averages(sector)

        # Get price history for risk analysis
        price_history = FinancialDataService.get_historical_prices(ticker)

        # 1. Evaluate Graham Criteria
        graham_results = GrahamCalculator.evaluate_graham_criteria(metrics)
        graham_criteria = GrahamCriteria(**graham_results)

        # 2. Evaluate Buffett Criteria
        buffett_results = BuffettCalculator.evaluate_buffett_criteria(metrics)
        buffett_criteria = BuffettCriteria(**buffett_results)

        # 3. DCF Valuation (three scenarios)
        dcf_base = ValuationCalculator.calculate_dcf_valuation(metrics, "base")
        dcf_optimistic = ValuationCalculator.calculate_dcf_valuation(metrics, "optimistic")
        dcf_pessimistic = ValuationCalculator.calculate_dcf_valuation(metrics, "pessimistic")

        # Use pessimistic scenario for margin of safety (conservative approach)
        dcf_intrinsic_value = dcf_pessimistic.get('intrinsic_value', 0)

        # Calculate margin of safety for DCF
        margin_dollars, margin_percentage = ValuationCalculator.calculate_margin_of_safety(
            dcf_intrinsic_value, current_price
        )
        meets_margin = ValuationCalculator.meets_minimum_margin(margin_percentage)

        dcf_valuation = ValuationResult(
            method="Discounted Cash Flow (DCF)",
            intrinsic_value=dcf_intrinsic_value,
            current_price=current_price,
            margin_of_safety=margin_dollars,
            margin_of_safety_percentage=margin_percentage,
            meets_minimum_margin=meets_margin,
            scenario_optimistic=dcf_optimistic.get('intrinsic_value', 0),
            scenario_base=dcf_base.get('intrinsic_value', 0),
            scenario_pessimistic=dcf_pessimistic.get('intrinsic_value', 0)
        )

        # 4. Multiples Valuation
        multiples_results = ValuationCalculator.calculate_multiples_valuation(metrics, sector_averages)
        multiples_intrinsic_value = multiples_results.get('intrinsic_value', 0)

        margin_dollars_mult, margin_percentage_mult = ValuationCalculator.calculate_margin_of_safety(
            multiples_intrinsic_value, current_price
        )
        meets_margin_mult = ValuationCalculator.meets_minimum_margin(margin_percentage_mult)

        multiples_valuation = ValuationResult(
            method="Comparable Multiples",
            intrinsic_value=multiples_intrinsic_value,
            current_price=current_price,
            margin_of_safety=margin_dollars_mult,
            margin_of_safety_percentage=margin_percentage_mult,
            meets_minimum_margin=meets_margin_mult
        )

        # 5. Risk Analysis
        risk_results = RiskCalculator.perform_risk_analysis(metrics, price_history)
        risk_analysis = RiskAnalysis(**risk_results)

        # 6. Generate Educational Explanations
        explanations = AnalysisService.generate_explanations(
            metrics, sector_averages, dcf_intrinsic_value, current_price, margin_percentage
        )

        # 7. Generate Recommendation
        recommendation, overall_score, strengths, weaknesses, final_text = AnalysisService.generate_recommendation(
            graham_criteria, buffett_criteria, dcf_valuation, multiples_valuation, risk_analysis
        )

        # Build complete analysis
        analysis = StockAnalysis(
            ticker=ticker.upper(),
            company_name=metrics.get('company_name', ticker),
            current_price=current_price,
            recommendation=recommendation,
            overall_score=overall_score,
            graham_criteria=graham_criteria,
            buffett_criteria=buffett_criteria,
            dcf_valuation=dcf_valuation,
            multiples_valuation=multiples_valuation,
            risk_analysis=risk_analysis,
            metric_explanations=explanations,
            strengths=strengths,
            weaknesses=weaknesses,
            final_recommendation_text=final_text
        )

        return analysis

    @staticmethod
    def generate_explanations(metrics: Dict, sector_averages: Dict,
                              intrinsic_value: float, current_price: float,
                              margin_percentage: float) -> list:
        """Generate educational explanations for all key metrics"""
        explanations = []

        # P/E Ratio
        pe_ratio = metrics.get('trailing_pe', 0)
        sector_pe = sector_averages.get('pe_ratio', 18)
        if pe_ratio > 0:
            explanations.append(
                ExplanationGenerator.explain_pe_ratio(pe_ratio, sector_pe, current_price)
            )

        # P/B Ratio
        pb_ratio = metrics.get('price_to_book', 0)
        if pb_ratio > 0:
            explanations.append(
                ExplanationGenerator.explain_pb_ratio(pb_ratio, current_price)
            )

        # Margin of Safety (MOST IMPORTANT)
        explanations.append(
            ExplanationGenerator.explain_margin_of_safety(
                margin_percentage, intrinsic_value, current_price
            )
        )

        # ROE
        roe = metrics.get('return_on_equity', 0)
        explanations.append(ExplanationGenerator.explain_roe(roe))

        # Debt to Equity
        debt_to_equity = metrics.get('debt_to_equity', 0)
        explanations.append(ExplanationGenerator.explain_debt_to_equity(debt_to_equity))

        # Current Ratio
        current_ratio = metrics.get('current_ratio', 0)
        explanations.append(ExplanationGenerator.explain_current_ratio(current_ratio))

        # Free Cash Flow
        fcf = metrics.get('free_cash_flow', 0)
        market_cap = metrics.get('market_cap', 0)
        explanations.append(ExplanationGenerator.explain_free_cash_flow(fcf, market_cap))

        return explanations

    @staticmethod
    def generate_recommendation(graham: GrahamCriteria, buffett: BuffettCriteria,
                               dcf: ValuationResult, multiples: ValuationResult,
                               risk: RiskAnalysis) -> tuple:
        """
        Generate final recommendation based on all analysis
        Returns: (recommendation_type, overall_score, strengths, weaknesses, final_text)
        """
        strengths = []
        weaknesses = []

        # Calculate overall score (0-10)
        score = 0

        # Graham score contribution (0-3 points)
        score += (graham.overall_score / 5) * 3

        # Buffett score contribution (0-2 points)
        score += (buffett.overall_score / 4) * 2

        # Margin of safety contribution (0-3 points) - MOST IMPORTANT
        if dcf.meets_minimum_margin:
            score += 3
            strengths.append(
                f"✓ Excelente margen de seguridad del {dcf.margin_of_safety_percentage:.1f}% "
                f"(supera el mínimo del 30%)"
            )
        elif dcf.margin_of_safety_percentage >= 15:
            score += 1.5
            weaknesses.append(
                f"Margen de seguridad de {dcf.margin_of_safety_percentage:.1f}% es insuficiente "
                f"(Graham requiere mínimo 30%)"
            )
        else:
            weaknesses.append(
                f"✗ Margen de seguridad muy bajo o negativo ({dcf.margin_of_safety_percentage:.1f}%) - "
                f"No hay protección contra riesgos"
            )

        # Valuation contribution (0-2 points)
        avg_margin = (dcf.margin_of_safety_percentage + multiples.margin_of_safety_percentage) / 2
        if avg_margin >= 25:
            score += 2
            strengths.append("✓ Ambos métodos de valoración sugieren subvaloración significativa")
        elif avg_margin >= 10:
            score += 1

        # Risk penalty (can subtract up to 2 points)
        if risk.overall_risk_level == "HIGH":
            score -= 2
            weaknesses.append(f"✗ Riesgo general ALTO - múltiples factores preocupantes")
        elif risk.overall_risk_level == "MEDIUM":
            score -= 0.5

        # Ensure score is between 0 and 10
        score = max(0, min(10, score))

        # Specific strengths based on Graham criteria
        if graham.pe_ratio_pass:
            strengths.append(f"✓ P/E ratio de {graham.pe_ratio:.2f} cumple criterio de Graham (< 15)")

        if graham.pb_ratio_pass:
            strengths.append(f"✓ P/B ratio de {graham.pb_ratio:.2f} cumple criterio de Graham (< 1.5)")

        if graham.debt_to_equity_pass:
            strengths.append(f"✓ Deuda manejable ({graham.debt_to_equity:.1f}% deuda/capital)")

        # Specific strengths based on Buffett criteria
        if buffett.roe_pass:
            strengths.append(f"✓ ROE excelente de {buffett.roe*100:.1f}% (criterio de Buffett > 15%)")

        if buffett.fcf_positive:
            strengths.append(f"✓ Flujo de caja libre positivo y de calidad")

        if "Strong" in buffett.competitive_advantage:
            strengths.append(f"✓ Indicadores de ventaja competitiva sostenible")

        # Weaknesses
        if not graham.pe_ratio_pass and graham.pe_ratio > 0:
            weaknesses.append(f"P/E ratio de {graham.pe_ratio:.2f} supera el límite de Graham (15)")

        if not graham.pb_ratio_pass and graham.pb_ratio > 0:
            weaknesses.append(f"P/B ratio de {graham.pb_ratio:.2f} supera el límite de Graham (1.5)")

        if not graham.debt_to_equity_pass:
            weaknesses.append(f"✗ Deuda elevada ({graham.debt_to_equity:.1f}% deuda/capital)")

        if not buffett.roe_pass:
            weaknesses.append(f"ROE de {buffett.roe*100:.1f}% por debajo del estándar de Buffett (15%)")

        if not buffett.fcf_positive:
            weaknesses.append(f"✗ Flujo de caja libre negativo o de baja calidad")

        # Determine recommendation type
        if score >= 7.5 and dcf.meets_minimum_margin and risk.overall_risk_level != "HIGH":
            recommendation = RecommendationType.STRONG_BUY
            rec_text = "COMPRA FUERTE"
        elif score >= 6 and dcf.margin_of_safety_percentage >= 20:
            recommendation = RecommendationType.BUY
            rec_text = "BUENA COMPRA"
        elif score >= 4.5:
            recommendation = RecommendationType.HOLD
            rec_text = "MANTENER / CONSIDERAR"
        else:
            recommendation = RecommendationType.AVOID
            rec_text = "EVITAR"

        # Generate final recommendation text
        criteria_met = graham.overall_score + buffett.overall_score
        criteria_total = 9

        final_text = f"""
## {rec_text}

**Puntuación General: {score:.1f}/10**

Esta acción cumple {graham.overall_score} de 5 criterios de Benjamin Graham y {buffett.overall_score} de 4 criterios de Warren Buffett ({criteria_met} de {criteria_total} criterios totales de value investing).

### Análisis del Margen de Seguridad
El margen de seguridad es el concepto más importante en value investing según Benjamin Graham.

- **Valoración DCF (conservadora)**: ${dcf.intrinsic_value:.2f}
- **Precio actual**: ${dcf.current_price:.2f}
- **Margen de seguridad**: {dcf.margin_of_safety_percentage:.1f}%
- **Cumple mínimo del 30%**: {'✓ SÍ' if dcf.meets_minimum_margin else '✗ NO'}

{
'Este amplio margen de seguridad proporciona protección significativa contra errores de análisis y eventos negativos inesperados.'
if dcf.meets_minimum_margin
else 'El margen de seguridad es insuficiente. Graham requiere mínimo 30% para protegerte contra riesgos.'
}

### Principales Fortalezas
{chr(10).join(f"• {s}" for s in strengths[:5]) if strengths else "• Pocas fortalezas identificadas"}

### Principales Debilidades y Riesgos
{chr(10).join(f"• {w}" for w in weaknesses[:5]) if weaknesses else "• Pocas debilidades identificadas"}

### Evaluación de Riesgo
**Nivel de Riesgo General: {risk.overall_risk_level}**

{risk.permanent_loss_risks[0] if risk.permanent_loss_risks else "No se identificaron riesgos críticos."}

### Conclusión
{
'Esta acción representa una excelente oportunidad de value investing. Cumple los criterios estrictos de Graham y Buffett, tiene un margen de seguridad amplio, y presenta riesgo controlado. Es el tipo de inversión que los inversores value buscan.'
if recommendation == RecommendationType.STRONG_BUY
else 'Esta acción presenta características atractivas de value investing. Tiene un margen de seguridad aceptable y cumple varios criterios importantes. Considera los riesgos mencionados antes de invertir.'
if recommendation == RecommendationType.BUY
else 'Esta acción tiene algunos aspectos positivos pero no cumple los estándares estrictos de value investing. El margen de seguridad es insuficiente o hay riesgos significativos. Podrías considerar esperar un mejor precio de entrada.'
if recommendation == RecommendationType.HOLD
else 'Esta acción NO es recomendable según principios de value investing. No cumple criterios básicos de Graham y Buffett, tiene margen de seguridad insuficiente o negativo, y/o presenta riesgos altos. Busca mejores oportunidades con mayor protección contra pérdidas.'
}

**Recuerda**: Este análisis es educativo. Siempre investiga factores cualitativos adicionales (calidad del management, ventajas competitivas, tendencias de la industria) antes de invertir. El value investing requiere paciencia y disciplina.
"""

        return recommendation, score, strengths, weaknesses, final_text
