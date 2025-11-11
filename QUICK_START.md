# 🚀 Quick Start Guide

Guía rápida para poner en marcha la aplicación Value Investing Analyzer.

## 🐳 Opción 1: Docker (Recomendado - Más Fácil)

### Un solo comando:

```bash
# Construir y ejecutar
docker-compose up --build

# O usando Make
make build && make up
```

✅ **¡Listo!** Accede a:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Comandos útiles:

```bash
make logs      # Ver logs
make down      # Detener todo
make restart   # Reiniciar
make dev       # Modo desarrollo con hot-reload
```

---

## 💻 Opción 2: Instalación Manual (Sin Docker)

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

---

## 🐳 Troubleshooting Docker

### Docker no inicia
```bash
# Verificar que Docker está corriendo
docker ps

# Ver logs de errores
docker-compose logs

# Reconstruir desde cero
make clean
make build
make up
```

### Puerto ya en uso
```bash
# Ver qué usa el puerto
lsof -i :8000
lsof -i :3000

# O detener todos los contenedores
docker-compose down
```

### Más ayuda con Docker
Ver [DOCKER.md](./DOCKER.md) para guía completa de Docker.

---

## 💻 Troubleshooting Instalación Manual

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
