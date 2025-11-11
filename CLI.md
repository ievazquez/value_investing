# 💻 CLI Guide - Value Investing Analyzer

Interfaz de línea de comandos para analizar acciones sin necesidad de ejecutar el servidor web.

## 🚀 Inicio Rápido

### Instalación

```bash
# Instalar dependencias del backend
cd backend
pip install -r requirements.txt
```

### Uso Básico

```bash
# Desde el directorio raíz (usando wrapper script)
./analyze.sh AAPL

# Desde el directorio backend
cd backend
python cli.py AAPL

# En Windows
analyze.bat AAPL
```

## 📋 Comandos y Opciones

### Sintaxis General

```bash
python cli.py [TICKER...] [OPCIONES]
```

### Opciones Disponibles

| Opción | Descripción |
|--------|-------------|
| `-d, --detailed` | Análisis detallado completo |
| `-m, --metrics` | Solo tabla de métricas |
| `-j, --json` | Salida en formato JSON |
| `-s, --search QUERY` | Buscar acciones por ticker o nombre |
| `-f, --format FORMAT` | Formato de salida: summary, detailed, metrics, json |
| `--no-color` | Desactivar colores en la salida |

## 📚 Ejemplos de Uso

### 1. Análisis Rápido (Resumen)

Análisis resumido con información clave:

```bash
./analyze.sh AAPL
```

**Salida:**
```
================================================================================
  📊 Apple Inc. (AAPL)
================================================================================

🎯 RECOMENDACIÓN: BUY
   Puntuación: 7.5/10
   Precio actual: $178.45

📈 Resumen Rápido
-----------------
  Criterios Graham:  4/5
  Criterios Buffett: 3/4
  Margen de Seguridad: 28.5%
  Riesgo General: MEDIUM
```

### 2. Análisis Detallado

Información completa con todos los criterios:

```bash
./analyze.sh AAPL --detailed
# o
./analyze.sh AAPL -d
```

**Salida incluye:**
- Resumen ejecutivo
- Criterios de Graham (P/E, P/B, Deuda, Current Ratio)
- Criterios de Buffett (ROE, Márgenes, FCF)
- Valoración intrínseca (DCF y múltiplos)
- Análisis de riesgo
- Top 3 fortalezas y debilidades

### 3. Solo Métricas en Tabla

Vista tabular de métricas principales:

```bash
./analyze.sh MSFT --metrics
# o
./analyze.sh MSFT -m
```

**Salida:**
```
Graham Metrics
-----------------
Métrica                   Valor           Criterio        Status
----------------------------------------------------------------------
P/E Ratio                 28.50           < 15            ✗
P/B Ratio                 10.20           < 1.5           ✗
Deuda/Capital             35.4            < 50%           ✓
Current Ratio             2.15            > 2.0           ✓

Buffett Metrics
-----------------
Métrica                   Valor           Criterio        Status
----------------------------------------------------------------------
ROE                       45.2            > 15%           ✓
Operating Margin          42.8            Stable          ✓
Free Cash Flow            $65.15B         Positive        ✓
```

### 4. Salida en JSON

Formato JSON para integración con otras herramientas:

```bash
./analyze.sh KO --json
# o
./analyze.sh KO -j
```

**Salida:**
```json
{
  "ticker": "KO",
  "company_name": "The Coca-Cola Company",
  "current_price": 58.75,
  "recommendation": "BUY",
  "overall_score": 7.2,
  "graham_criteria": {
    "pe_ratio": 24.5,
    "pe_ratio_pass": false,
    "pb_ratio": 10.8,
    ...
  },
  ...
}
```

### 5. Guardar Análisis en Archivo

```bash
# Guardar JSON
./analyze.sh AAPL --json > aapl_analysis.json

# Guardar análisis detallado
./analyze.sh AAPL --detailed > aapl_report.txt
```

### 6. Analizar Múltiples Acciones

```bash
# Analizar varias acciones en una sola ejecución
./analyze.sh AAPL MSFT KO

# Con formato específico
./analyze.sh AAPL MSFT KO --format summary
```

### 7. Buscar Acciones

Buscar por ticker o nombre de empresa:

```bash
./analyze.sh --search "coca cola"
# o
./analyze.sh -s "apple"
```

**Salida:**
```
================================================================================
  🔍 Búsqueda de Acciones
================================================================================

Resultados para 'coca cola':

  KO - The Coca-Cola Company
    Sector: Consumer Defensive
    Industria: Beverages—Non-Alcoholic
```

### 8. Sin Colores (para logs o scripts)

```bash
./analyze.sh AAPL --no-color > log.txt
```

## 🎯 Casos de Uso Prácticos

### Monitoreo Diario

Script para monitorear tu portafolio:

```bash
#!/bin/bash
# monitor_portfolio.sh

echo "=== Portfolio Analysis $(date) ===" > portfolio_report.txt
./analyze.sh AAPL MSFT GOOGL AMZN --format summary >> portfolio_report.txt
cat portfolio_report.txt
```

### Integración con Scripts

```bash
#!/bin/bash
# find_undervalued.sh

# Analizar acciones y filtrar las con margen > 30%
for ticker in AAPL MSFT KO JPM JNJ PG; do
    ./analyze.sh $ticker --json | jq -r \
        'select(.dcf_valuation.margin_of_safety_percentage > 30) | .ticker'
done
```

### Pipeline de Análisis

```bash
# Buscar, analizar y guardar
./analyze.sh --search "technology" | grep "TICKER" | \
while read -r ticker _; do
    ./analyze.sh $ticker --json >> tech_analysis.json
done
```

### Comparación de Múltiples Acciones

```bash
#!/bin/bash
# compare_stocks.sh

echo "Comparación de Tecnológicas"
echo "============================="

for ticker in AAPL MSFT GOOGL; do
    echo ""
    echo "--- $ticker ---"
    ./analyze.sh $ticker | grep -A 5 "Resumen Rápido"
done
```

### Alertas Automáticas

```bash
#!/bin/bash
# alert_opportunities.sh

# Analizar y enviar email si encuentra buena oportunidad
RESULT=$(./analyze.sh AAPL --json)
SCORE=$(echo $RESULT | jq -r '.overall_score')

if (( $(echo "$SCORE > 7.5" | bc -l) )); then
    echo "$RESULT" | mail -s "Investment Opportunity: AAPL" you@email.com
fi
```

## 📊 Formatos de Salida

### Summary (Resumen)
- **Uso:** Monitoreo rápido diario
- **Incluye:** Recomendación, score, métricas clave
- **Ideal para:** Terminal, quick checks

### Detailed (Detallado)
- **Uso:** Análisis profundo antes de invertir
- **Incluye:** Todos los criterios, valoraciones, riesgos
- **Ideal para:** Toma de decisiones, reportes

### Metrics (Métricas)
- **Uso:** Comparación rápida de múltiples acciones
- **Incluye:** Tablas de métricas Graham y Buffett
- **Ideal para:** Análisis comparativo, spreadsheets

### JSON
- **Uso:** Integración con otras herramientas
- **Incluye:** Todos los datos estructurados
- **Ideal para:** Automatización, APIs, bases de datos

## 🔧 Integración con Otras Herramientas

### Con jq (procesamiento JSON)

```bash
# Extraer solo el score
./analyze.sh AAPL --json | jq '.overall_score'

# Filtrar acciones con margen > 30%
./analyze.sh AAPL --json | jq 'select(.dcf_valuation.margin_of_safety_percentage > 30)'

# Obtener solo la recomendación
./analyze.sh AAPL --json | jq -r '.recommendation'
```

### Con csvkit (exportar a CSV)

```bash
# Convertir JSON a CSV
./analyze.sh AAPL MSFT KO --json | \
    jq -s '.' | \
    in2csv -f json > analysis.csv
```

### Con Python (procesamiento personalizado)

```python
import subprocess
import json

# Analizar acción desde Python
result = subprocess.run(
    ['python', 'cli.py', 'AAPL', '--json'],
    capture_output=True,
    text=True,
    cwd='backend'
)

analysis = json.loads(result.stdout)
print(f"Score: {analysis['overall_score']}")
```

### Con cron (análisis programado)

```bash
# Agregar a crontab
# Analizar portafolio diariamente a las 9 AM
0 9 * * 1-5 cd /path/to/value_investing && ./analyze.sh AAPL MSFT KO --detailed > daily_report.txt
```

## 🐳 Uso con Docker

### Ejecutar CLI en contenedor

```bash
# Método 1: Ejecutar comando directo
docker-compose run --rm backend python cli.py AAPL

# Método 2: Entrar al contenedor
docker-compose exec backend bash
python cli.py AAPL --detailed

# Método 3: Agregar al Makefile
# Agregar esto al Makefile:
analyze:
	docker-compose run --rm backend python cli.py $(TICKER)

# Luego usar:
make analyze TICKER=AAPL
```

### Dockerfile específico para CLI

```dockerfile
# Dockerfile.cli
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "cli.py"]

# Build y uso:
# docker build -f Dockerfile.cli -t value-investing-cli .
# docker run value-investing-cli AAPL --detailed
```

## 🎨 Personalización

### Desactivar Colores

```bash
# Para compatibilidad con logs o CI/CD
./analyze.sh AAPL --no-color
```

### Formato Personalizado

Edita `cli.py` para agregar tu propio formato:

```python
def print_custom(analysis: Dict):
    """Tu formato personalizado"""
    print(f"{analysis['ticker']}: {analysis['overall_score']}")

# Agregar en main():
elif output_format == 'custom':
    print_custom(analysis_dict)
```

## 🚨 Troubleshooting

### Error: Module not found

```bash
# Asegúrate de estar en el directorio correcto
cd backend
pip install -r requirements.txt
```

### Error: No data for ticker

```bash
# Verifica que el ticker sea válido
./analyze.sh --search "apple"  # Buscar primero
./analyze.sh AAPL              # Luego analizar
```

### Colores no funcionan en Windows

```bash
# En Windows, instala colorama
pip install colorama

# O desactiva colores
./analyze.sh AAPL --no-color
```

### Muy lento

```bash
# El primer análisis siempre es más lento (descarga de datos)
# Los siguientes son más rápidos gracias al cache de yfinance
```

## 📖 Ejemplos Completos

### Script de Screening

```bash
#!/bin/bash
# screen_stocks.sh - Encuentra oportunidades de value investing

echo "Value Investing Screener"
echo "========================"
echo ""

# Lista de acciones a analizar
STOCKS="AAPL MSFT GOOGL AMZN META TSLA NVDA JPM BAC WMT KO PG JNJ"

echo "Buscando acciones con:"
echo "  - Score > 7.0"
echo "  - Margen de seguridad > 25%"
echo "  - Riesgo LOW o MEDIUM"
echo ""

for ticker in $STOCKS; do
    # Analizar en JSON
    result=$(./analyze.sh $ticker --json 2>/dev/null)

    if [ $? -eq 0 ]; then
        score=$(echo $result | jq -r '.overall_score')
        margin=$(echo $result | jq -r '.dcf_valuation.margin_of_safety_percentage')
        risk=$(echo $result | jq -r '.risk_analysis.overall_risk_level')

        # Filtrar por criterios
        if (( $(echo "$score > 7.0" | bc -l) )) && \
           (( $(echo "$margin > 25" | bc -l) )) && \
           [[ "$risk" != "HIGH" ]]; then
            echo "✓ $ticker - Score: $score, Margen: ${margin}%, Riesgo: $risk"
        fi
    fi
done

echo ""
echo "Screening completado!"
```

### Dashboard Simple

```bash
#!/bin/bash
# dashboard.sh - Dashboard de terminal

clear
echo "╔═══════════════════════════════════════════════════╗"
echo "║     VALUE INVESTING ANALYZER - DASHBOARD          ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

./analyze.sh AAPL MSFT KO --format summary

echo ""
echo "Última actualización: $(date)"
```

## 💡 Tips y Mejores Prácticas

1. **Usa alias** para comandos frecuentes:
   ```bash
   alias va='./analyze.sh'
   alias vaj='./analyze.sh --json'
   alias vad='./analyze.sh --detailed'
   ```

2. **Combina con watch** para monitoreo en tiempo real:
   ```bash
   watch -n 300 './analyze.sh AAPL'  # Actualiza cada 5 minutos
   ```

3. **Guarda análisis históricos**:
   ```bash
   ./analyze.sh AAPL --json > "analysis_$(date +%Y%m%d).json"
   ```

4. **Usa grep para filtrar** salida:
   ```bash
   ./analyze.sh AAPL --detailed | grep -A 5 "Fortalezas"
   ```

5. **Combina con APIs externas**:
   ```bash
   # Enviar a Slack, Discord, etc.
   ./analyze.sh AAPL --json | \
       jq '{text: "Score: \(.overall_score)"}' | \
       curl -X POST -H 'Content-type: application/json' \
       --data @- YOUR_WEBHOOK_URL
   ```

## 📚 Recursos Adicionales

- [README.md](./README.md) - Documentación general
- [DOCKER.md](./DOCKER.md) - Uso con Docker
- [backend/cli.py](./backend/cli.py) - Código fuente del CLI

---

**Happy Analyzing! 📊📈**
