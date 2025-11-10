"""
Explanation Generator
Generates educational explanations for financial metrics in simple language
"""

from typing import Dict, List
from app.models.schemas import MetricExplanation, CriteriaStatus

class ExplanationGenerator:
    """Generates beginner-friendly explanations for financial metrics"""

    @staticmethod
    def format_currency(value: float) -> str:
        """Format value as currency"""
        if abs(value) >= 1_000_000_000:
            return f"${value/1_000_000_000:.2f}B"
        elif abs(value) >= 1_000_000:
            return f"${value/1_000_000:.2f}M"
        elif abs(value) >= 1_000:
            return f"${value/1_000:.2f}K"
        else:
            return f"${value:.2f}"

    @staticmethod
    def format_percentage(value: float) -> str:
        """Format value as percentage"""
        return f"{value*100:.2f}%" if value < 1 else f"{value:.2f}%"

    @staticmethod
    def explain_pe_ratio(pe_ratio: float, sector_pe: float, current_price: float) -> MetricExplanation:
        """Generate explanation for P/E ratio"""
        eps = current_price / pe_ratio if pe_ratio > 0 else 0

        # Determine status
        if pe_ratio <= 0:
            status = CriteriaStatus.FAIL
        elif pe_ratio < 15:
            status = CriteriaStatus.PASS
        elif pe_ratio < 25:
            status = CriteriaStatus.NEUTRAL
        else:
            status = CriteriaStatus.FAIL

        numeric_example = (
            f"Si la empresa gana ${eps:.2f} por acción al año, y el precio de la acción es ${current_price:.2f}, "
            f"entonces estás pagando ${pe_ratio:.2f} por cada dólar de ganancias anuales. "
            f"\n\nImaginalo así: Es como comprar un negocio que gana $1,000 al año. "
            f"Con un P/E de {pe_ratio:.2f}, pagarías ${pe_ratio*1000:.0f} por ese negocio. "
            f"Tardarías {pe_ratio:.1f} años en recuperar tu inversión si las ganancias se mantienen constantes."
        )

        sector_comparison = (
            f"El P/E promedio del sector es {sector_pe:.2f}. "
            f"Esta empresa {'cotiza con un descuento' if pe_ratio < sector_pe else 'cotiza con una prima'} "
            f"de {abs((pe_ratio - sector_pe) / sector_pe * 100):.1f}% respecto a sus competidores."
        )

        if status == CriteriaStatus.PASS:
            interpretation = (
                f"✓ BUENO: El P/E de {pe_ratio:.2f} cumple el criterio de Graham (menor a 15). "
                f"Esto sugiere que la acción podría estar subvalorada o que el mercado tiene bajas expectativas."
            )
        elif status == CriteriaStatus.NEUTRAL:
            interpretation = (
                f"≈ NEUTRAL: El P/E de {pe_ratio:.2f} está en rango moderado. "
                f"No es una ganga pero tampoco está sobrevalorada según estándares de Graham."
            )
        else:
            interpretation = (
                f"✗ ALTO: El P/E de {pe_ratio:.2f} supera el límite de Graham (15). "
                f"Estás pagando mucho por cada dólar de ganancias. Esto puede indicar sobrevaloración "
                f"o altas expectativas de crecimiento futuro."
            )

        return MetricExplanation(
            metric_name="P/E Ratio (Precio/Ganancias)",
            simple_definition=(
                "El P/E ratio muestra cuánto estás pagando por cada dólar que la empresa gana al año. "
                "Es como el 'precio de entrada' para ser dueño de las ganancias de la empresa."
            ),
            why_important=(
                "Benjamin Graham usaba el P/E para identificar acciones baratas. Un P/E bajo puede significar "
                "que estás comprando ganancias a buen precio. Un P/E muy alto puede significar que estás "
                "pagando de más y asumiendo más riesgo."
            ),
            formula=f"P/E Ratio = Precio por Acción / Ganancias por Acción = ${current_price:.2f} / ${eps:.2f} = {pe_ratio:.2f}",
            calculated_value=pe_ratio,
            formatted_value=f"{pe_ratio:.2f}",
            numeric_example=numeric_example,
            sector_comparison=sector_comparison,
            interpretation=interpretation,
            status=status
        )

    @staticmethod
    def explain_pb_ratio(pb_ratio: float, current_price: float) -> MetricExplanation:
        """Generate explanation for P/B ratio"""
        book_value = current_price / pb_ratio if pb_ratio > 0 else 0

        # Determine status
        if pb_ratio <= 0:
            status = CriteriaStatus.FAIL
        elif pb_ratio < 1.5:
            status = CriteriaStatus.PASS
        elif pb_ratio < 3:
            status = CriteriaStatus.NEUTRAL
        else:
            status = CriteriaStatus.FAIL

        numeric_example = (
            f"El valor en libros por acción es ${book_value:.2f}. Esto es lo que 'vale' la empresa en papel "
            f"según su balance (activos menos deudas dividido entre acciones).\n\n"
            f"Con un precio de ${current_price:.2f} y un P/B de {pb_ratio:.2f}, estás pagando "
            f"{pb_ratio:.2f} veces el valor contable.\n\n"
            f"Ejemplo: Si una empresa tiene edificios, máquinas y efectivo que valen $100, "
            f"y deudas de $40, su valor en libros es $60. Con un P/B de {pb_ratio:.2f}, "
            f"pagarías ${pb_ratio * 60:.0f} por esos $60 de activos netos."
        )

        if status == CriteriaStatus.PASS:
            interpretation = (
                f"✓ EXCELENTE: El P/B de {pb_ratio:.2f} cumple el criterio de Graham (menor a 1.5). "
                f"Estás comprando por {'menos' if pb_ratio < 1 else 'cerca'} del valor de los activos de la empresa. "
                f"Esto proporciona un 'respaldo' tangible a tu inversión."
            )
        elif status == CriteriaStatus.NEUTRAL:
            interpretation = (
                f"≈ MODERADO: El P/B de {pb_ratio:.2f} está en rango medio. "
                f"Pagas una prima moderada sobre el valor contable. Esto es común para empresas rentables."
            )
        else:
            interpretation = (
                f"✗ ALTO: El P/B de {pb_ratio:.2f} supera ampliamente el límite de Graham (1.5). "
                f"Estás pagando mucho más que el valor de los activos. Esto puede estar justificado "
                f"para empresas con ventajas competitivas fuertes, pero aumenta el riesgo."
            )

        return MetricExplanation(
            metric_name="P/B Ratio (Precio/Valor en Libros)",
            simple_definition=(
                "El P/B ratio compara el precio de la acción con el valor contable (valor en libros) de la empresa. "
                "Te dice si estás pagando más o menos que el 'valor en papel' de los activos de la empresa."
            ),
            why_important=(
                "Graham prefería empresas con P/B bajo porque significa que hay activos tangibles respaldando "
                "tu inversión. Si P/B es menor a 1, estás comprando por menos del valor de los activos, "
                "lo que proporciona un 'colchón de seguridad'."
            ),
            formula=f"P/B Ratio = Precio por Acción / Valor en Libros por Acción = ${current_price:.2f} / ${book_value:.2f} = {pb_ratio:.2f}",
            calculated_value=pb_ratio,
            formatted_value=f"{pb_ratio:.2f}",
            numeric_example=numeric_example,
            interpretation=interpretation,
            status=status
        )

    @staticmethod
    def explain_roe(roe: float) -> MetricExplanation:
        """Generate explanation for ROE"""
        # Determine status
        if roe < 0:
            status = CriteriaStatus.FAIL
        elif roe >= 0.15:
            status = CriteriaStatus.PASS
        elif roe >= 0.10:
            status = CriteriaStatus.NEUTRAL
        else:
            status = CriteriaStatus.FAIL

        numeric_example = (
            f"Si los accionistas han invertido $100 en la empresa, y el ROE es {ExplanationGenerator.format_percentage(roe)}, "
            f"significa que la empresa genera ${roe * 100:.2f} de ganancia al año con esos $100.\n\n"
            f"Es como tener $10,000 en un negocio. Con un ROE de {ExplanationGenerator.format_percentage(roe)}, "
            f"ese negocio te genera ${roe * 10000:.0f} de ganancia anual. "
            f"{'¡Excelente retorno!' if roe >= 0.15 else 'Retorno moderado.' if roe >= 0.10 else 'Retorno bajo o negativo.'}"
        )

        if status == CriteriaStatus.PASS:
            interpretation = (
                f"✓ EXCELENTE: ROE de {ExplanationGenerator.format_percentage(roe)} cumple el criterio de Buffett (mayor a 15%). "
                f"La empresa es muy eficiente convirtiendo el capital de los accionistas en ganancias. "
                f"Esto sugiere una ventaja competitiva o un management excepcional."
            )
        elif status == CriteriaStatus.NEUTRAL:
            interpretation = (
                f"≈ MODERADO: ROE de {ExplanationGenerator.format_percentage(roe)} es aceptable pero no excepcional. "
                f"La empresa genera retornos decentes para los accionistas."
            )
        else:
            interpretation = (
                f"✗ BAJO: ROE de {ExplanationGenerator.format_percentage(roe)} no cumple estándares de calidad. "
                f"La empresa no está generando buenos retornos sobre el capital invertido. "
                f"Esto puede indicar un negocio de baja calidad o problemas operativos."
            )

        return MetricExplanation(
            metric_name="ROE (Return on Equity - Retorno sobre Capital)",
            simple_definition=(
                "El ROE muestra cuánta ganancia genera la empresa por cada dólar que los accionistas han invertido. "
                "Es una medida de qué tan eficientemente la empresa usa el dinero de los dueños."
            ),
            why_important=(
                "Warren Buffett busca empresas con ROE alto y consistente (mayor a 15%). "
                "Un ROE alto significa que la empresa es excelente convirtiendo capital en ganancias, "
                "lo que sugiere ventajas competitivas sostenibles."
            ),
            formula=f"ROE = Ganancia Neta / Capital de Accionistas = {ExplanationGenerator.format_percentage(roe)}",
            calculated_value=roe,
            formatted_value=ExplanationGenerator.format_percentage(roe),
            numeric_example=numeric_example,
            interpretation=interpretation,
            status=status
        )

    @staticmethod
    def explain_debt_to_equity(debt_to_equity: float) -> MetricExplanation:
        """Generate explanation for Debt-to-Equity ratio"""
        # Determine status
        if debt_to_equity < 0:
            status = CriteriaStatus.FAIL
        elif debt_to_equity <= 50:
            status = CriteriaStatus.PASS
        elif debt_to_equity <= 100:
            status = CriteriaStatus.NEUTRAL
        else:
            status = CriteriaStatus.FAIL

        numeric_example = (
            f"Si la empresa tiene $100 de capital propio (patrimonio), entonces tiene "
            f"${debt_to_equity:.0f} de deuda.\n\n"
            f"Imaginalo como tu situación personal: si tienes $50,000 ahorrados (tu patrimonio) "
            f"y debes ${debt_to_equity/100 * 50000:.0f} en préstamos, tu ratio deuda/capital es {debt_to_equity:.0f}%. "
            f"{'Esto es manejable.' if debt_to_equity <= 50 else 'Esto es riesgoso.' if debt_to_equity <= 100 else 'Esto es muy peligroso.'}"
        )

        if status == CriteriaStatus.PASS:
            interpretation = (
                f"✓ BAJO: Ratio de {debt_to_equity:.1f}% cumple el criterio de Graham (menor a 50%). "
                f"La empresa tiene deuda manejable. Esto reduce el riesgo financiero y da flexibilidad "
                f"para invertir o capear crisis económicas."
            )
        elif status == CriteriaStatus.NEUTRAL:
            interpretation = (
                f"≈ MODERADO: Ratio de {debt_to_equity:.1f}% es elevado pero no crítico. "
                f"La empresa usa apalancamiento significativo. Monitorea que pueda pagar sus deudas."
            )
        else:
            interpretation = (
                f"✗ ALTO: Ratio de {debt_to_equity:.1f}% supera ampliamente el límite de Graham (50%). "
                f"La empresa está muy endeudada. Esto es riesgoso porque en tiempos difíciles, "
                f"la carga de deuda puede llevar a problemas serios o incluso quiebra."
            )

        return MetricExplanation(
            metric_name="Ratio Deuda/Capital",
            simple_definition=(
                "Este ratio muestra cuánta deuda tiene la empresa en relación a su capital propio (patrimonio). "
                "Te dice si la empresa está muy endeudada o tiene finanzas sólidas."
            ),
            why_important=(
                "Graham enfatizaba empresas con poca deuda (menor a 50%). "
                "Mucha deuda aumenta el riesgo de pérdida permanente de capital en tiempos difíciles. "
                "Empresas con poca deuda tienen más flexibilidad y menor riesgo de quiebra."
            ),
            formula=f"Deuda/Capital = (Deuda Total / Patrimonio) × 100 = {debt_to_equity:.1f}%",
            calculated_value=debt_to_equity,
            formatted_value=f"{debt_to_equity:.1f}%",
            numeric_example=numeric_example,
            interpretation=interpretation,
            status=status
        )

    @staticmethod
    def explain_current_ratio(current_ratio: float) -> MetricExplanation:
        """Generate explanation for Current Ratio"""
        # Determine status
        if current_ratio >= 2.0:
            status = CriteriaStatus.PASS
        elif current_ratio >= 1.0:
            status = CriteriaStatus.NEUTRAL
        else:
            status = CriteriaStatus.FAIL

        numeric_example = (
            f"Si la empresa tiene ${current_ratio * 100:.0f} en efectivo y activos que puede convertir "
            f"rápidamente en dinero, y debe pagar $100 en el corto plazo, su current ratio es {current_ratio:.2f}.\n\n"
            f"Ejemplo personal: tienes ${current_ratio * 1000:.0f} en el banco y debes pagar $1,000 "
            f"en cuentas este mes. {'Tienes suficiente y te sobra.' if current_ratio >= 2 else 'Tienes justo lo necesario.' if current_ratio >= 1 else 'No tienes suficiente, tendrás problemas.'}"
        )

        if status == CriteriaStatus.PASS:
            interpretation = (
                f"✓ EXCELENTE: Current ratio de {current_ratio:.2f} cumple el criterio de Graham (mayor a 2.0). "
                f"La empresa tiene activos líquidos más que suficientes para cubrir sus obligaciones a corto plazo. "
                f"Esto indica salud financiera sólida y bajo riesgo de problemas de liquidez."
            )
        elif status == CriteriaStatus.NEUTRAL:
            interpretation = (
                f"≈ ACEPTABLE: Current ratio de {current_ratio:.2f} es suficiente pero ajustado. "
                f"La empresa puede cubrir sus obligaciones pero tiene poco margen de error."
            )
        else:
            interpretation = (
                f"✗ RIESGOSO: Current ratio de {current_ratio:.2f} está por debajo de 1.0. "
                f"La empresa no tiene suficientes activos líquidos para pagar sus deudas a corto plazo. "
                f"Esto es una señal de alerta roja - posibles problemas de liquidez o solvencia."
            )

        return MetricExplanation(
            metric_name="Current Ratio (Ratio Corriente)",
            simple_definition=(
                "El current ratio compara los activos líquidos de la empresa (efectivo, cuentas por cobrar, inventario) "
                "con sus deudas a corto plazo. Te dice si la empresa puede pagar sus cuentas inmediatas."
            ),
            why_important=(
                "Graham requería un current ratio de al menos 2.0 para asegurar liquidez adecuada. "
                "Si es menor a 1.0, la empresa podría tener problemas para pagar sus deudas, "
                "lo que aumenta el riesgo de crisis financiera."
            ),
            formula=f"Current Ratio = Activos Corrientes / Pasivos Corrientes = {current_ratio:.2f}",
            calculated_value=current_ratio,
            formatted_value=f"{current_ratio:.2f}",
            numeric_example=numeric_example,
            interpretation=interpretation,
            status=status
        )

    @staticmethod
    def explain_margin_of_safety(margin_percentage: float, intrinsic_value: float,
                                 current_price: float) -> MetricExplanation:
        """Generate explanation for Margin of Safety"""
        # Determine status
        if margin_percentage >= 30:
            status = CriteriaStatus.PASS
        elif margin_percentage >= 15:
            status = CriteriaStatus.NEUTRAL
        else:
            status = CriteriaStatus.FAIL

        margin_dollars = intrinsic_value - current_price

        numeric_example = (
            f"Valor Intrínseco Estimado: ${intrinsic_value:.2f}\n"
            f"Precio Actual de Mercado: ${current_price:.2f}\n"
            f"Diferencia (Descuento): ${margin_dollars:.2f} ({margin_percentage:.1f}%)\n\n"
            f"Ejemplo: Si calculas que una casa vale $300,000 pero la puedes comprar por ${current_price/intrinsic_value * 300000:.0f}, "
            f"tu margen de seguridad es {margin_percentage:.1f}%. Este 'colchón' te protege si:\n"
            f"- Tu valoración tiene errores\n"
            f"- El mercado baja\n"
            f"- La empresa enfrenta problemas inesperados"
        )

        if status == CriteriaStatus.PASS:
            interpretation = (
                f"✓ EXCELENTE: Margen de seguridad de {margin_percentage:.1f}% SUPERA el mínimo de Graham (30%). "
                f"La acción cotiza con un descuento significativo respecto a su valor real estimado. "
                f"Este amplio margen te protege contra errores de cálculo y eventos negativos inesperados. "
                f"Esta es una característica clave de una buena inversión value."
            )
        elif status == CriteriaStatus.NEUTRAL:
            interpretation = (
                f"≈ MODERADO: Margen de seguridad de {margin_percentage:.1f}% es insuficiente según Graham (requiere 30%). "
                f"Hay algo de descuento, pero el margen de protección es limitado. "
                f"Considera esperar a un mejor precio o buscar otras oportunidades con mayor margen."
            )
        else:
            interpretation = (
                f"✗ INSUFICIENTE: {'La acción cotiza SOBRE su valor intrínseco' if margin_percentage < 0 else f'Margen de seguridad de {margin_percentage:.1f}% es muy bajo'}. "
                f"No cumple el principio fundamental de Graham. "
                f"{'Estás pagando de más.' if margin_percentage < 0 else 'No hay suficiente protección contra riesgos.'} "
                f"Graham rechazaría esta inversión por falta de margen de seguridad adecuado."
            )

        return MetricExplanation(
            metric_name="Margen de Seguridad",
            simple_definition=(
                "El margen de seguridad es la diferencia entre lo que vale realmente la empresa (valor intrínseco) "
                "y lo que estás pagando por ella (precio de mercado). Es tu 'colchón de protección' contra errores."
            ),
            why_important=(
                "Este es el concepto MÁS IMPORTANTE de Benjamin Graham. Un margen del 30% o más te protege si:\n"
                "- Tu análisis tiene errores\n"
                "- La empresa enfrenta problemas imprevistos\n"
                "- El mercado general cae\n\n"
                "Graham decía: 'El margen de seguridad es el secreto de la inversión inteligente.'"
            ),
            formula=f"Margen de Seguridad = (Valor Intrínseco - Precio Actual) / Valor Intrínseco × 100 = ({intrinsic_value:.2f} - {current_price:.2f}) / {intrinsic_value:.2f} × 100 = {margin_percentage:.1f}%",
            calculated_value=margin_percentage,
            formatted_value=f"{margin_percentage:.1f}%",
            numeric_example=numeric_example,
            interpretation=interpretation,
            status=status
        )

    @staticmethod
    def explain_free_cash_flow(fcf: float, market_cap: float) -> MetricExplanation:
        """Generate explanation for Free Cash Flow"""
        fcf_yield = (fcf / market_cap * 100) if market_cap > 0 else 0

        # Determine status
        if fcf > 0 and fcf_yield >= 5:
            status = CriteriaStatus.PASS
        elif fcf > 0:
            status = CriteriaStatus.NEUTRAL
        else:
            status = CriteriaStatus.FAIL

        numeric_example = (
            f"La empresa genera {ExplanationGenerator.format_currency(fcf)} en flujo de caja libre anualmente. "
            f"Este es el dinero 'sobrante' después de pagar todos los gastos e inversiones necesarias.\n\n"
            f"FCF Yield: {fcf_yield:.2f}% (FCF / Capitalización de Mercado)\n\n"
            f"Ejemplo: Es como tu salario después de pagar todas tus cuentas, comida, renta Y ahorrar "
            f"para reparaciones necesarias. El FCF es lo que realmente queda 'libre' para los dueños. "
            f"{'Pueden usarlo para dividendos, reducir deuda o reinvertir.' if fcf > 0 else 'No queda nada libre - la empresa consume más de lo que genera.'}"
        )

        if status == CriteriaStatus.PASS:
            interpretation = (
                f"✓ EXCELENTE: FCF positivo de {ExplanationGenerator.format_currency(fcf)} con yield de {fcf_yield:.2f}%. "
                f"Buffett busca empresas que generan mucho cash flow. Esto significa que el negocio "
                f"realmente genera dinero que puede usar para crecer, pagar dividendos o reducir deuda. "
                f"Un FCF yield alto es señal de posible subvaloración."
            )
        elif status == CriteriaStatus.NEUTRAL:
            interpretation = (
                f"≈ POSITIVO: FCF de {ExplanationGenerator.format_currency(fcf)} es positivo pero el yield de {fcf_yield:.2f}% es modesto. "
                f"La empresa genera efectivo, lo cual es bueno, pero no es una ganga en términos de FCF."
            )
        else:
            interpretation = (
                f"✗ NEGATIVO: FCF de {ExplanationGenerator.format_currency(fcf)} es negativo. "
                f"La empresa está consumiendo más efectivo del que genera. Eventualmente necesitará "
                f"financiamiento externo (deuda o vender más acciones). Esto es una señal de alerta roja."
            )

        return MetricExplanation(
            metric_name="Free Cash Flow (Flujo de Caja Libre)",
            simple_definition=(
                "El FCF es el efectivo que genera la empresa después de pagar todos sus gastos operativos "
                "y las inversiones necesarias para mantener el negocio. Es el dinero 'verdadero' que queda libre."
            ),
            why_important=(
                "Warren Buffett prefiere empresas con FCF fuerte y creciente. El FCF es más difícil de "
                "manipular que las ganancias contables. Un FCF positivo significa que la empresa realmente "
                "genera efectivo, no solo 'ganancias en papel'. FCF negativo es una señal de alerta."
            ),
            formula=f"FCF = {ExplanationGenerator.format_currency(fcf)} | FCF Yield = {fcf_yield:.2f}%",
            calculated_value=fcf,
            formatted_value=ExplanationGenerator.format_currency(fcf),
            numeric_example=numeric_example,
            interpretation=interpretation,
            status=status
        )
