# 🐳 Docker Guide - Value Investing Analyzer

Guía completa para ejecutar la aplicación usando Docker.

## 📋 Requisitos

- Docker 20.10 o superior
- Docker Compose 2.0 o superior
- (Opcional) Make para usar comandos simplificados

### Verificar instalación

```bash
docker --version
docker-compose --version
```

## 🚀 Inicio Rápido

### Opción 1: Usando Make (Recomendado)

```bash
# Ver todos los comandos disponibles
make help

# Construir y ejecutar en modo producción
make build
make up

# O en un solo comando
make rebuild
```

### Opción 2: Usando Docker Compose directamente

```bash
# Construir las imágenes
docker-compose build

# Iniciar los contenedores
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Acceso a la Aplicación

Después de iniciar los contenedores:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 🔧 Modos de Ejecución

### Modo Producción (Optimizado)

Usa `docker-compose.yml` - Imágenes optimizadas sin hot-reload.

```bash
# Usando Make
make up

# Usando Docker Compose
docker-compose up -d
```

**Características:**
- Frontend: Build optimizado servido por Nginx
- Backend: Python slim con dependencias mínimas
- Sin volúmenes montados (cambios requieren rebuild)
- Ideal para producción o testing

### Modo Desarrollo (Hot-Reload)

Usa `docker-compose.dev.yml` - Con hot-reload para desarrollo.

```bash
# Usando Make
make dev

# Usando Docker Compose
docker-compose -f docker-compose.dev.yml up
```

**Características:**
- Frontend: React Dev Server con hot-reload
- Backend: Código montado con auto-reload
- Cambios en código se reflejan automáticamente
- Ideal para desarrollo activo

## 📝 Comandos Principales (Make)

### Producción

```bash
make build          # Construir imágenes
make up             # Iniciar contenedores
make down           # Detener contenedores
make restart        # Reiniciar contenedores
make logs           # Ver logs en tiempo real
```

### Desarrollo

```bash
make dev            # Iniciar modo desarrollo
make dev-down       # Detener modo desarrollo
make dev-logs       # Ver logs de desarrollo
make dev-build      # Reconstruir imágenes dev
```

### Utilidades

```bash
make clean          # Limpiar todo (contenedores, imágenes, volúmenes)
make health         # Verificar estado de servicios
make info           # Ver información de Docker
make shell-backend  # Abrir shell en contenedor backend
make shell-frontend # Abrir shell en contenedor frontend
```

### Servicios Individuales

```bash
make backend-logs      # Ver logs solo del backend
make frontend-logs     # Ver logs solo del frontend
make backend-restart   # Reiniciar solo backend
make frontend-restart  # Reiniciar solo frontend
```

## 🔍 Comandos Docker Compose

### Gestión Básica

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Construcción

```bash
# Construir sin caché
docker-compose build --no-cache

# Construir solo un servicio
docker-compose build backend
docker-compose build frontend

# Reconstruir y reiniciar
docker-compose up -d --build
```

### Debugging

```bash
# Acceder a shell del contenedor
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh

# Ver logs con timestamps
docker-compose logs -f -t

# Ejecutar comando en contenedor
docker-compose exec backend python -c "import sys; print(sys.version)"
```

### Limpieza

```bash
# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar contenedores + volúmenes
docker-compose down -v

# Detener y eliminar contenedores + volúmenes + imágenes
docker-compose down -v --rmi all

# Limpiar sistema completo de Docker
docker system prune -a --volumes
```

## 🏗️ Arquitectura Docker

### Servicios

```yaml
backend:
  - Puerto: 8000
  - Imagen: Python 3.10-slim
  - Framework: FastAPI
  - Health check: /health endpoint

frontend:
  - Puerto: 3000 (80 en producción)
  - Imagen: Node 18 (build) + Nginx (serve)
  - Framework: React
  - Proxy API: /api -> backend:8000
```

### Networking

Los servicios se comunican en una red privada `value-investing-network`:
- Frontend puede acceder a Backend usando `http://backend:8000`
- Nginx hace proxy de `/api` al backend automáticamente

### Volúmenes (Desarrollo)

En modo desarrollo, se montan volúmenes para hot-reload:
```
./backend -> /app (backend)
./frontend -> /app (frontend)
```

## 🔒 Variables de Entorno

### Backend

Configuradas en `docker-compose.yml`:

```yaml
PORT=8000
HOST=0.0.0.0
FRONTEND_URL=http://localhost:3000
```

### Frontend

Configuradas en `docker-compose.dev.yml`:

```yaml
REACT_APP_API_URL=http://localhost:8000/api
CHOKIDAR_USEPOLLING=true  # Para hot-reload en Docker
```

## 🧪 Testing

```bash
# Ejecutar tests en backend (cuando estén disponibles)
docker-compose exec backend pytest

# Ejecutar tests en frontend
docker-compose exec frontend npm test
```

## 🚨 Troubleshooting

### Problema: Puerto ya en uso

```bash
# Ver qué está usando el puerto
sudo lsof -i :8000
sudo lsof -i :3000

# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 en lugar de 8000
```

### Problema: Contenedores no inician

```bash
# Ver logs detallados
docker-compose logs

# Verificar estado
docker-compose ps

# Reconstruir desde cero
make clean
make build
make up
```

### Problema: Hot-reload no funciona en desarrollo

```bash
# Asegurar que estás usando docker-compose.dev.yml
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up

# Verificar que los volúmenes están montados
docker-compose -f docker-compose.dev.yml exec backend ls -la
```

### Problema: Error de permisos

```bash
# En Linux, puede ser necesario ajustar permisos
sudo chown -R $USER:$USER ./backend
sudo chown -R $USER:$USER ./frontend
```

### Problema: Imágenes muy grandes

```bash
# Ver tamaño de imágenes
docker images

# Limpiar imágenes no usadas
docker image prune -a

# Ver uso de espacio
docker system df
```

### Problema: Backend no puede conectar a APIs externas

```bash
# Verificar conectividad desde el contenedor
docker-compose exec backend ping google.com
docker-compose exec backend curl https://query1.finance.yahoo.com

# Si hay problemas de DNS, agregar DNS en docker-compose.yml:
services:
  backend:
    dns:
      - 8.8.8.8
      - 8.8.4.4
```

## 📊 Monitoreo

### Ver uso de recursos

```bash
# Uso en tiempo real
docker stats

# Ver solo contenedores de la app
docker stats value-investing-backend value-investing-frontend
```

### Health Checks

```bash
# Verificar salud de servicios
docker-compose ps

# Health check manual
curl http://localhost:8000/health
curl http://localhost:3000
```

## 🔄 Actualizaciones

### Actualizar código sin rebuild completo

```bash
# En modo desarrollo (auto-reload)
# Solo edita el código, los cambios se reflejan automáticamente

# En modo producción
docker-compose restart backend   # Si solo cambiaste backend
docker-compose restart frontend  # Si solo cambiaste frontend
```

### Actualizar dependencias

```bash
# Backend: Después de modificar requirements.txt
docker-compose build backend
docker-compose up -d backend

# Frontend: Después de modificar package.json
docker-compose build frontend
docker-compose up -d frontend
```

## 🌐 Despliegue en Producción

### Consideraciones

1. **Variables de Entorno**: Usar archivo `.env` para producción
2. **Volumes**: No montar código fuente en producción
3. **Logs**: Configurar log rotation
4. **SSL/TLS**: Usar reverse proxy (Nginx, Traefik) con SSL
5. **Escalabilidad**: Usar orquestadores (Docker Swarm, Kubernetes)

### Ejemplo con reverse proxy

```yaml
# Agregar a docker-compose.yml para producción
services:
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-proxy.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
```

## 📚 Recursos

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [React Docker Best Practices](https://create-react-app.dev/docs/deployment/)

## 💡 Tips

1. **Desarrollo rápido**: Usa `make dev` para hot-reload
2. **Limpieza regular**: Ejecuta `docker system prune` periódicamente
3. **Logs**: Usa `docker-compose logs -f --tail=100` para ver últimas líneas
4. **Debugging**: Usa `docker-compose exec backend python` para REPL interactivo
5. **Performance**: En Windows/Mac, considera usar volúmenes nombrados para mejor performance

## 🆘 Soporte

Si tienes problemas:

1. Verifica que Docker está corriendo: `docker ps`
2. Revisa los logs: `docker-compose logs`
3. Verifica health checks: `docker-compose ps`
4. Intenta rebuild: `make clean && make rebuild`
5. Verifica puertos disponibles: `netstat -an | grep LISTEN`

---

**Nota**: Esta configuración Docker está optimizada para desarrollo y testing. Para producción, considera usar orquestadores como Kubernetes o servicios cloud como AWS ECS, Google Cloud Run, etc.
