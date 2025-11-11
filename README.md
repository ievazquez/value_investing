# 📊 Value Investing Analyzer

Una aplicación web educativa completa para analizar acciones desde la perspectiva del value investing, basada en los principios de **Benjamin Graham** y **Warren Buffett**.

## 🎯 Objetivo

Crear una herramienta educativa y práctica que capacite a inversores principiantes para:
- Identificar valores subvalorados con precisión
- Valorar empresas usando métodos profesionales (DCF, múltiplos)
- Aplicar los criterios específicos de Graham y Buffett
- Entender y calcular el margen de seguridad (mínimo 30%)
- Desarrollar estrategias de gestión de riesgo
- Aprender conceptos complejos con explicaciones simples y ejemplos concretos

## ✨ Características Principales

### 📈 Análisis Fundamental Completo
- **Búsqueda de acciones** por ticker o nombre de empresa
- **Datos financieros históricos** de los últimos 5 años
- **Cálculo automático** de todas las métricas clave

### 📖 Criterios de Benjamin Graham
- P/E Ratio (debe ser < 15)
- P/B Ratio (debe ser < 1.5)
- Ratio Deuda/Capital (debe ser < 50%)
- Current Ratio (debe ser > 2.0)
- Consistencia de ganancias

### 💼 Criterios de Warren Buffett
- ROE (debe ser > 15%)
- Márgenes operativos estables
- Free Cash Flow positivo y creciente
- Evaluación de ventaja competitiva (economic moat)

### 💰 Valoración Intrínseca
- **DCF (Discounted Cash Flow)** con tres escenarios (optimista, base, pesimista)
- **Múltiplos comparables** del sector
- **Margen de seguridad** calculado con umbral mínimo del 30%
- Identificación clara de acciones subvaloradas

### ⚠️ Análisis de Riesgo
- Volatilidad histórica y Beta
- Análisis de endeudamiento y cobertura de intereses
- Identificación de riesgos de pérdida permanente de capital
- Evaluación de concentración y calidad de activos

### 🎓 Explicaciones Educativas
Cada métrica incluye:
- **Definición simple** en lenguaje cotidiano
- **Por qué es importante** para value investing
- **Cómo se calcula** con la fórmula explicada
- **Ejemplo numérico detallado** con números reales
- **Comparación con el sector**
- **Interpretación** para la decisión de inversión
- **Señal visual** (verde/amarillo/rojo)

### 📊 Recomendación Final
- Clasificación clara: COMPRA FUERTE / BUENA COMPRA / MANTENER / EVITAR
- Puntuación de 0-10 basada en criterios Graham/Buffett
- Lista de fortalezas y debilidades
- Justificación detallada con datos concretos
- Explicación del razonamiento de forma educativa

## 🏗️ Arquitectura Técnica

### Backend
- **Framework**: FastAPI (Python)
- **Datos financieros**: yfinance (Yahoo Finance API)
- **Cálculos**: NumPy, Pandas, SciPy
- **API REST**: Endpoints para búsqueda y análisis

### Frontend
- **Framework**: React 18 con Hooks
- **Styling**: CSS personalizado (responsive)
- **API calls**: Axios
- **Componentes**: Modulares y reutilizables

### Estructura del Proyecto
```
value_investing/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints REST
│   │   │   └── stock_routes.py
│   │   ├── services/         # Lógica de negocio
│   │   │   ├── financial_data_service.py
│   │   │   └── analysis_service.py
│   │   ├── calculators/      # Cálculos financieros
│   │   │   ├── graham_calculator.py
│   │   │   ├── buffett_calculator.py
│   │   │   ├── valuation_calculator.py
│   │   │   └── risk_calculator.py
│   │   ├── models/           # Modelos Pydantic
│   │   │   └── schemas.py
│   │   └── utils/            # Utilidades
│   │       └── explanation_generator.py
│   ├── main.py               # App principal
│   └── requirements.txt      # Dependencias
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── SearchBar.js
│   │   │   ├── RecommendationBanner.js
│   │   │   ├── MetricCard.js
│   │   │   ├── ExpandableSection.js
│   │   │   ├── ExplanationCard.js
│   │   │   ├── GrahamCriteriaSection.js
│   │   │   ├── BuffettCriteriaSection.js
│   │   │   ├── ValuationSection.js
│   │   │   └── RiskSection.js
│   │   ├── services/         # API calls
│   │   │   └── api.js
│   │   ├── App.js            # Componente principal
│   │   ├── App.css           # Estilos
│   │   └── index.js          # Entry point
│   ├── public/
│   │   └── index.html
│   └── package.json          # Dependencias
│
└── README.md                 # Este archivo
```

## 🐳 Instalación con Docker (Recomendado)

La forma más rápida y sencilla de ejecutar la aplicación es usando Docker.

### Requisitos
- Docker 20.10+
- Docker Compose 2.0+

### Inicio Rápido

```bash
# Clonar el repositorio
git clone <repository-url>
cd value_investing

# Opción 1: Usando Make (recomendado)
make build
make up

# Opción 2: Usando Docker Compose directamente
docker-compose build
docker-compose up -d
```

✅ **¡Listo!** La aplicación estará disponible en:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Comandos Docker Útiles

```bash
# Ver logs
make logs                    # o: docker-compose logs -f

# Detener la aplicación
make down                    # o: docker-compose down

# Reiniciar servicios
make restart                 # o: docker-compose restart

# Modo desarrollo con hot-reload
make dev                     # o: docker-compose -f docker-compose.dev.yml up

# Limpiar todo
make clean
```

### Ver documentación completa de Docker
Consulta [DOCKER.md](./DOCKER.md) para instrucciones detalladas, troubleshooting y configuración avanzada.

---

## 🚀 Instalación Manual (Sin Docker)

### Requisitos Previos
- Python 3.8 o superior
- Node.js 14 o superior
- npm o yarn

### Instalación del Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor
python main.py
```

El backend estará disponible en `http://localhost:8000`

### Instalación del Frontend

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar la aplicación
npm start
```

La aplicación estará disponible en `http://localhost:3000`

---

## 💻 Uso desde CLI (Línea de Comandos)

### Análisis Rápido sin Servidor Web

Puedes analizar acciones directamente desde la terminal sin necesidad de ejecutar el servidor web:

```bash
# Desde el directorio raíz
./analyze.sh AAPL

# En Windows
analyze.bat AAPL

# Desde backend
cd backend
python cli.py AAPL
```

### Ejemplos de CLI

```bash
# Análisis rápido (resumen)
./analyze.sh AAPL

# Análisis detallado completo
./analyze.sh AAPL --detailed

# Solo métricas en tabla
./analyze.sh MSFT --metrics

# Salida en JSON (para scripts)
./analyze.sh KO --json

# Analizar múltiples acciones
./analyze.sh AAPL MSFT KO GOOGL

# Buscar acciones
./analyze.sh --search "coca cola"

# Guardar resultado en archivo
./analyze.sh AAPL --json > aapl_analysis.json
```

### Ventajas del CLI

- ⚡ **Más rápido** - No necesitas ejecutar el servidor web
- 🔄 **Automatizable** - Integra con scripts y cron jobs
- 📊 **Múltiples formatos** - Summary, detailed, metrics, JSON
- 🎯 **Monitoreo** - Analiza tu portafolio automáticamente
- 🐳 **Compatible con Docker** - `docker-compose run --rm backend python cli.py AAPL`

### Ver documentación completa del CLI
Consulta [CLI.md](./CLI.md) para guía completa, ejemplos avanzados y scripts de automatización.

---

## 📚 Uso de la Aplicación Web

1. **Buscar una acción**: Ingresa el ticker (ej: AAPL, MSFT, KO)
2. **Espera el análisis**: La app obtiene datos y realiza todos los cálculos
3. **Revisa la recomendación**: Ve la puntuación general y recomendación
4. **Explora las secciones**:
   - **Lo Básico**: Métricas principales con explicaciones detalladas
   - **Criterios de Graham**: Evaluación según Benjamin Graham
   - **Criterios de Buffett**: Evaluación según Warren Buffett
   - **Valoración**: DCF y múltiplos con margen de seguridad
   - **Riesgo**: Análisis completo de riesgos
   - **Fortalezas/Debilidades**: Resumen de pros y contras
   - **Recomendación Final**: Conclusión detallada

## 📊 Métricas Calculadas

### Métricas Prioritarias de Graham
- **P/E Ratio**: Precio/Ganancias (< 15)
- **P/B Ratio**: Precio/Valor en Libros (< 1.5)
- **Ratio Deuda/Capital**: (< 50%)
- **Current Ratio**: Liquidez (> 2.0)
- **Margen de Seguridad**: Mínimo 30%

### Métricas Prioritarias de Buffett
- **ROE**: Return on Equity (> 15%)
- **Márgenes Operativos**: Estables o crecientes
- **Free Cash Flow**: Positivo y creciente
- **Ventaja Competitiva**: Economic moat

### Otras Métricas Importantes
- PEG Ratio
- ROA (Return on Assets)
- Quick Ratio
- Earnings Growth
- Beta y Volatilidad
- Cobertura de Intereses

## 🎓 Conceptos Educativos

### Margen de Seguridad
El concepto MÁS IMPORTANTE de Benjamin Graham:
```
Margen de Seguridad = (Valor Intrínseco - Precio Actual) / Valor Intrínseco × 100
```

Un margen del 30% o más te protege contra:
- Errores en tu análisis
- Problemas imprevistos de la empresa
- Caídas generales del mercado

### Valoración DCF (Discounted Cash Flow)
Calcula el valor presente de los flujos de caja futuros:
1. Proyecta flujos de caja (5 años)
2. Calcula valor terminal (perpetuidad)
3. Descuenta al presente usando WACC
4. Ajusta por efectivo y deuda

### Riesgo de Pérdida Permanente
No confundir volatilidad con riesgo real:
- **Volatilidad**: Fluctuaciones temporales de precio
- **Pérdida Permanente**: Deterioro fundamental irreversible

## ⚠️ Advertencias Importantes

- Esta herramienta es **solo para fines educativos**
- **NO es asesoría financiera profesional**
- Los datos de Yahoo Finance pueden tener retrasos o inexactitudes
- Las valoraciones son estimaciones basadas en supuestos
- Siempre realiza tu propia investigación (due diligence)
- Consulta con un asesor financiero antes de invertir
- El rendimiento pasado no garantiza resultados futuros

## 🔧 Configuración Avanzada

### Variables de Entorno (Backend)

Crea un archivo `.env` en el directorio `backend/`:

```env
PORT=8000
HOST=0.0.0.0
FRONTEND_URL=http://localhost:3000
```

### Variables de Entorno (Frontend)

Crea un archivo `.env` en el directorio `frontend/`:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🤝 Contribuciones

Este es un proyecto educativo. Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📖 Recursos de Aprendizaje

### Libros Recomendados
- **"The Intelligent Investor"** - Benjamin Graham
- **"Security Analysis"** - Benjamin Graham & David Dodd
- **"The Essays of Warren Buffett"** - Warren Buffett

### Conceptos Clave
- Value Investing vs Growth Investing
- Análisis Fundamental vs Análisis Técnico
- Margen de Seguridad (Margin of Safety)
- Economic Moat (Ventaja Competitiva)
- Discounted Cash Flow (DCF)
- Círculo de Competencia

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como herramienta educativa para aprender value investing.

---

**Recuerda**: "El precio es lo que pagas. El valor es lo que obtienes." - Warren Buffett

**Principio de Graham**: "La inversión inteligente es más una cuestión de gestión de riesgos que de gestión de rentabilidad. El margen de seguridad es el secreto."
