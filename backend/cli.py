#!/usr/bin/env python3
"""
Value Investing Analyzer - CLI
Analiza acciones desde la línea de comandos usando principios de Graham y Buffett
"""

import argparse
import json
import sys
from typing import Dict, Optional
from services.analysis_service import AnalysisService
from services.financial_data_service import FinancialDataService

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text: str, color: str = Colors.ENDC):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(text: str):
    """Print a styled header"""
    print_colored(f"\n{'=' * 80}", Colors.CYAN)
    print_colored(f"  {text}", Colors.BOLD + Colors.CYAN)
    print_colored(f"{'=' * 80}", Colors.CYAN)

def print_subheader(text: str):
    """Print a styled subheader"""
    print_colored(f"\n{text}", Colors.BOLD + Colors.BLUE)
    print_colored("-" * len(text), Colors.BLUE)

def format_currency(value: float) -> str:
    """Format value as currency"""
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def format_percentage(value: float) -> str:
    """Format value as percentage"""
    return f"{value:.2f}%" if abs(value) < 1 else f"{value:.2f}%"

def get_status_symbol(status: str) -> str:
    """Get colored symbol for status"""
    if status == "PASS":
        return f"{Colors.GREEN}✓{Colors.ENDC}"
    elif status == "NEUTRAL":
        return f"{Colors.YELLOW}≈{Colors.ENDC}"
    else:
        return f"{Colors.RED}✗{Colors.ENDC}"

def get_recommendation_color(recommendation: str) -> str:
    """Get color for recommendation"""
    if recommendation == "STRONG_BUY":
        return Colors.GREEN
    elif recommendation == "BUY":
        return Colors.CYAN
    elif recommendation == "HOLD":
        return Colors.YELLOW
    else:
        return Colors.RED

def print_summary(analysis: Dict):
    """Print summary of analysis"""
    print_header(f"📊 {analysis['company_name']} ({analysis['ticker']})")

    # Recommendation
    rec_color = get_recommendation_color(analysis['recommendation'])
    rec_text = analysis['recommendation'].replace('_', ' ')
    print_colored(f"\n🎯 RECOMENDACIÓN: {rec_text}", Colors.BOLD + rec_color)
    print_colored(f"   Puntuación: {analysis['overall_score']:.1f}/10", rec_color)
    print_colored(f"   Precio actual: ${analysis['current_price']:.2f}", Colors.BOLD)

    # Quick metrics
    print_subheader("📈 Resumen Rápido")
    print(f"  Criterios Graham:  {analysis['graham_criteria']['overall_score']}/5")
    print(f"  Criterios Buffett: {analysis['buffett_criteria']['overall_score']}/4")

    margin = analysis['dcf_valuation']['margin_of_safety_percentage']
    margin_color = Colors.GREEN if margin >= 30 else Colors.YELLOW if margin >= 15 else Colors.RED
    print_colored(f"  Margen de Seguridad: {margin:.1f}%", margin_color)
    print(f"  Riesgo General: {analysis['risk_analysis']['overall_risk_level']}")

def print_detailed(analysis: Dict):
    """Print detailed analysis"""
    print_summary(analysis)

    # Graham Criteria
    print_subheader("📖 Criterios de Benjamin Graham")
    graham = analysis['graham_criteria']

    print(f"  {get_status_symbol('PASS' if graham['pe_ratio_pass'] else 'FAIL')} P/E Ratio: {graham['pe_ratio']:.2f} (debe ser < 15)")
    print(f"  {get_status_symbol('PASS' if graham['pb_ratio_pass'] else 'FAIL')} P/B Ratio: {graham['pb_ratio']:.2f} (debe ser < 1.5)")
    print(f"  {get_status_symbol('PASS' if graham['debt_to_equity_pass'] else 'FAIL')} Deuda/Capital: {graham['debt_to_equity']:.1f}% (debe ser < 50%)")
    print(f"  {get_status_symbol('PASS' if graham['current_ratio_pass'] else 'FAIL')} Current Ratio: {graham['current_ratio']:.2f} (debe ser > 2.0)")
    print(f"  {get_status_symbol('PASS' if graham['earnings_growth_consistent'] else 'FAIL')} Ganancias Consistentes")

    # Buffett Criteria
    print_subheader("💼 Criterios de Warren Buffett")
    buffett = analysis['buffett_criteria']

    print(f"  {get_status_symbol('PASS' if buffett['roe_pass'] else 'FAIL')} ROE: {buffett['roe']*100:.1f}% (debe ser > 15%)")
    print(f"  {get_status_symbol('PASS' if buffett['operating_margin_stable'] else 'FAIL')} Margen Operativo: {buffett['operating_margin']*100:.1f}%")
    print(f"  {get_status_symbol('PASS' if buffett['fcf_positive'] else 'FAIL')} Free Cash Flow: {format_currency(buffett['free_cash_flow'])}")
    print(f"  Ventaja Competitiva: {buffett['competitive_advantage']}")

    # Valuation
    print_subheader("💰 Valoración Intrínseca")
    dcf = analysis['dcf_valuation']
    multiples = analysis['multiples_valuation']

    print(f"\n  DCF (Discounted Cash Flow):")
    print(f"    Valor Intrínseco: ${dcf['intrinsic_value']:.2f}")
    print(f"    Precio Actual: ${dcf['current_price']:.2f}")
    margin_color = Colors.GREEN if dcf['meets_minimum_margin'] else Colors.YELLOW if dcf['margin_of_safety_percentage'] >= 15 else Colors.RED
    print_colored(f"    Margen de Seguridad: {dcf['margin_of_safety_percentage']:.1f}%", margin_color)

    if dcf.get('scenario_optimistic'):
        print(f"\n    Escenarios:")
        print(f"      Pesimista: ${dcf['scenario_pessimistic']:.2f}")
        print(f"      Base:      ${dcf['scenario_base']:.2f}")
        print(f"      Optimista: ${dcf['scenario_optimistic']:.2f}")

    print(f"\n  Múltiplos Comparables:")
    print(f"    Valor Intrínseco: ${multiples['intrinsic_value']:.2f}")
    print_colored(f"    Margen de Seguridad: {multiples['margin_of_safety_percentage']:.1f}%", margin_color)

    # Risk Analysis
    print_subheader("⚠️  Análisis de Riesgo")
    risk = analysis['risk_analysis']

    risk_color = Colors.GREEN if risk['overall_risk_level'] == 'LOW' else Colors.YELLOW if risk['overall_risk_level'] == 'MEDIUM' else Colors.RED
    print_colored(f"  Nivel de Riesgo: {risk['overall_risk_level']}", risk_color)
    print(f"  Volatilidad: {risk['volatility']*100:.1f}%")
    print(f"  Beta: {risk['beta']:.2f}")
    print(f"  Cobertura de Deuda: {risk['debt_coverage_ratio']:.2f}x" if risk['debt_coverage_ratio'] < 999 else "  Cobertura de Deuda: ∞")

    # Strengths and Weaknesses
    if analysis.get('strengths'):
        print_subheader("✅ Fortalezas")
        for strength in analysis['strengths'][:3]:
            print_colored(f"  • {strength}", Colors.GREEN)

    if analysis.get('weaknesses'):
        print_subheader("❌ Debilidades")
        for weakness in analysis['weaknesses'][:3]:
            print_colored(f"  • {weakness}", Colors.RED)

def print_metrics(analysis: Dict):
    """Print metrics in table format"""
    print_header(f"📊 Métricas de {analysis['company_name']} ({analysis['ticker']})")

    graham = analysis['graham_criteria']
    buffett = analysis['buffett_criteria']

    print_subheader("Graham Metrics")
    print(f"{'Métrica':<25} {'Valor':<15} {'Criterio':<15} {'Status':<10}")
    print("-" * 70)
    print(f"{'P/E Ratio':<25} {graham['pe_ratio']:<15.2f} {'< 15':<15} {get_status_symbol('PASS' if graham['pe_ratio_pass'] else 'FAIL')}")
    print(f"{'P/B Ratio':<25} {graham['pb_ratio']:<15.2f} {'< 1.5':<15} {get_status_symbol('PASS' if graham['pb_ratio_pass'] else 'FAIL')}")
    print(f"{'Deuda/Capital':<25} {graham['debt_to_equity']:<15.1f} {'< 50%':<15} {get_status_symbol('PASS' if graham['debt_to_equity_pass'] else 'FAIL')}")
    print(f"{'Current Ratio':<25} {graham['current_ratio']:<15.2f} {'> 2.0':<15} {get_status_symbol('PASS' if graham['current_ratio_pass'] else 'FAIL')}")

    print_subheader("Buffett Metrics")
    print(f"{'Métrica':<25} {'Valor':<15} {'Criterio':<15} {'Status':<10}")
    print("-" * 70)
    print(f"{'ROE':<25} {buffett['roe']*100:<15.1f} {'> 15%':<15} {get_status_symbol('PASS' if buffett['roe_pass'] else 'FAIL')}")
    print(f"{'Operating Margin':<25} {buffett['operating_margin']*100:<15.1f} {'Stable':<15} {get_status_symbol('PASS' if buffett['operating_margin_stable'] else 'FAIL')}")
    print(f"{'Free Cash Flow':<25} {format_currency(buffett['free_cash_flow']):<15} {'Positive':<15} {get_status_symbol('PASS' if buffett['fcf_positive'] else 'FAIL')}")

def print_json(analysis: Dict):
    """Print analysis as JSON"""
    # Convert to JSON-serializable format
    output = {
        'ticker': analysis['ticker'],
        'company_name': analysis['company_name'],
        'current_price': analysis['current_price'],
        'recommendation': analysis['recommendation'],
        'overall_score': analysis['overall_score'],
        'graham_criteria': dict(analysis['graham_criteria']),
        'buffett_criteria': dict(analysis['buffett_criteria']),
        'dcf_valuation': dict(analysis['dcf_valuation']),
        'multiples_valuation': dict(analysis['multiples_valuation']),
        'risk_analysis': dict(analysis['risk_analysis']),
        'strengths': analysis['strengths'],
        'weaknesses': analysis['weaknesses']
    }
    print(json.dumps(output, indent=2, default=str))

def search_stock(query: str):
    """Search for stocks"""
    print_header("🔍 Búsqueda de Acciones")
    results = FinancialDataService.search_stock(query)

    if not results:
        print_colored(f"No se encontraron resultados para: {query}", Colors.RED)
        return

    print(f"\nResultados para '{query}':\n")
    for result in results:
        print(f"  {Colors.BOLD}{result['ticker']}{Colors.ENDC} - {result['name']}")
        print(f"    Sector: {result.get('sector', 'N/A')}")
        print(f"    Industria: {result.get('industry', 'N/A')}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description='Value Investing Analyzer CLI - Analiza acciones con criterios de Graham y Buffett',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Análisis rápido (resumen)
  python cli.py AAPL

  # Análisis detallado
  python cli.py AAPL --detailed

  # Solo métricas en tabla
  python cli.py MSFT --metrics

  # Salida en formato JSON
  python cli.py KO --json

  # Buscar acciones
  python cli.py --search "coca cola"

  # Analizar múltiples acciones
  python cli.py AAPL MSFT KO --format summary

  # Análisis y guardar en archivo
  python cli.py AAPL --json > aapl_analysis.json
        """
    )

    parser.add_argument(
        'ticker',
        nargs='*',
        help='Ticker(s) de la acción a analizar (ej: AAPL, MSFT, KO)'
    )

    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Mostrar análisis detallado completo'
    )

    parser.add_argument(
        '-m', '--metrics',
        action='store_true',
        help='Mostrar solo tabla de métricas'
    )

    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Salida en formato JSON'
    )

    parser.add_argument(
        '-s', '--search',
        type=str,
        metavar='QUERY',
        help='Buscar acciones por ticker o nombre'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['summary', 'detailed', 'metrics', 'json'],
        default='summary',
        help='Formato de salida (default: summary)'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Desactivar colores en la salida'
    )

    args = parser.parse_args()

    # Disable colors if requested
    if args.no_color:
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')

    # Handle search
    if args.search:
        search_stock(args.search)
        return

    # Require ticker if not searching
    if not args.ticker:
        parser.print_help()
        return

    # Determine output format
    if args.json:
        output_format = 'json'
    elif args.detailed:
        output_format = 'detailed'
    elif args.metrics:
        output_format = 'metrics'
    else:
        output_format = args.format

    # Analyze each ticker
    for ticker in args.ticker:
        try:
            print_colored(f"\n🔄 Analizando {ticker.upper()}...", Colors.CYAN)

            # Perform analysis
            analysis = AnalysisService.analyze_stock(ticker)

            # Convert Pydantic models to dict
            analysis_dict = {
                'ticker': analysis.ticker,
                'company_name': analysis.company_name,
                'current_price': analysis.current_price,
                'recommendation': analysis.recommendation,
                'overall_score': analysis.overall_score,
                'graham_criteria': analysis.graham_criteria.dict(),
                'buffett_criteria': analysis.buffett_criteria.dict(),
                'dcf_valuation': analysis.dcf_valuation.dict(),
                'multiples_valuation': analysis.multiples_valuation.dict(),
                'risk_analysis': analysis.risk_analysis.dict(),
                'strengths': analysis.strengths,
                'weaknesses': analysis.weaknesses
            }

            # Print based on format
            if output_format == 'json':
                print_json(analysis_dict)
            elif output_format == 'detailed':
                print_detailed(analysis_dict)
            elif output_format == 'metrics':
                print_metrics(analysis_dict)
            else:  # summary
                print_summary(analysis_dict)

            print()  # Extra line between multiple tickers

        except ValueError as e:
            print_colored(f"\n❌ Error: {str(e)}", Colors.RED)
        except Exception as e:
            print_colored(f"\n❌ Error inesperado: {str(e)}", Colors.RED)
            if '--debug' in sys.argv:
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Análisis cancelado por el usuario", Colors.YELLOW)
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n❌ Error fatal: {str(e)}", Colors.RED)
        sys.exit(1)
