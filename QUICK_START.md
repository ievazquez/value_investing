# 🚀 Quick Start Guide

Guía rápida para poner en marcha la aplicación Value Investing Analyzer.

## Inicio Rápido (2 pasos)

### 1️⃣ Backend (Terminal 1)

```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

✅ Backend corriendo en `http://localhost:8000`

### 2️⃣ Frontend (Terminal 2)

```bash
# Instalar dependencias
cd frontend
npm install

# Iniciar aplicación
npm start
```

✅ App abierta automáticamente en `http://localhost:3000`

## Primeros Pasos

1. **Buscar**: Ingresa un ticker (ej: `AAPL`, `MSFT`, `KO`)
2. **Analizar**: Espera unos segundos mientras se obtienen los datos
3. **Explorar**: Navega por las secciones expandibles
4. **Aprender**: Lee las explicaciones detalladas de cada métrica

## Ejemplos de Tickers para Probar

- `AAPL` - Apple (Tecnología)
- `MSFT` - Microsoft (Tecnología)
- `KO` - Coca-Cola (Consumo)
- `JPM` - JPMorgan Chase (Finanzas)
- `JNJ` - Johnson & Johnson (Salud)
- `PG` - Procter & Gamble (Consumo)
- `WMT` - Walmart (Retail)
- `BAC` - Bank of America (Finanzas)

## Troubleshooting

### El backend no inicia
```bash
# Verificar versión de Python (necesitas 3.8+)
python --version

# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

### El frontend no inicia
```bash
# Limpiar caché
rm -rf node_modules package-lock.json
npm install

# Verificar versión de Node (necesitas 14+)
node --version
```

### Error al analizar una acción
- Verifica que el ticker sea válido
- Algunos tickers pueden no tener datos completos
- Intenta con acciones de empresas grandes (large-cap)

## Documentación Completa

Ver `README.md` para documentación completa de la aplicación.
