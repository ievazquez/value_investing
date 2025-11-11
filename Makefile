# Makefile for Value Investing Analyzer
# Simplifies Docker commands

.PHONY: help build up down logs restart clean dev prod test

# Default target
help:
	@echo "Value Investing Analyzer - Docker Commands"
	@echo ""
	@echo "Production:"
	@echo "  make build      - Build production containers"
	@echo "  make up         - Start production containers"
	@echo "  make down       - Stop production containers"
	@echo "  make restart    - Restart production containers"
	@echo "  make logs       - View production logs"
	@echo ""
	@echo "Development:"
	@echo "  make dev        - Start development environment with hot-reload"
	@echo "  make dev-down   - Stop development environment"
	@echo "  make dev-logs   - View development logs"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean      - Remove all containers, images, and volumes"
	@echo "  make test       - Run tests (when available)"
	@echo "  make shell-backend  - Open shell in backend container"
	@echo "  make shell-frontend - Open shell in frontend container"

# Production commands
build:
	@echo "Building production containers..."
	docker-compose build

up:
	@echo "Starting production environment..."
	docker-compose up -d
	@echo ""
	@echo "✓ Application is running!"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend API: http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"

down:
	@echo "Stopping production containers..."
	docker-compose down

restart: down up

logs:
	docker-compose logs -f

# Development commands
dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml up
	@echo ""
	@echo "✓ Development environment is running with hot-reload!"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend API: http://localhost:8000"

dev-down:
	@echo "Stopping development environment..."
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-build:
	@echo "Building development containers..."
	docker-compose -f docker-compose.dev.yml build

# Utility commands
clean:
	@echo "Cleaning up all Docker resources..."
	docker-compose down -v --rmi all --remove-orphans
	docker-compose -f docker-compose.dev.yml down -v --rmi all --remove-orphans
	@echo "✓ Cleanup complete!"

clean-volumes:
	@echo "Removing all volumes..."
	docker-compose down -v
	docker-compose -f docker-compose.dev.yml down -v

shell-backend:
	@echo "Opening shell in backend container..."
	docker-compose exec backend /bin/bash

shell-frontend:
	@echo "Opening shell in frontend container..."
	docker-compose exec frontend /bin/sh

# Individual service commands
backend-logs:
	docker-compose logs -f backend

frontend-logs:
	docker-compose logs -f frontend

backend-restart:
	docker-compose restart backend

frontend-restart:
	docker-compose restart frontend

# Health checks
health:
	@echo "Checking service health..."
	@echo ""
	@echo "Backend:"
	@curl -s http://localhost:8000/health || echo "Backend is not responding"
	@echo ""
	@echo "Frontend:"
	@curl -s http://localhost:3000 > /dev/null && echo "Frontend is running" || echo "Frontend is not responding"

# Installation helpers
install:
	@echo "Installing dependencies locally (for development without Docker)..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	@echo "✓ Dependencies installed!"

# Docker system info
info:
	@echo "Docker System Information:"
	@echo ""
	docker-compose ps
	@echo ""
	docker system df

# Rebuild everything from scratch
rebuild:
	@echo "Rebuilding everything from scratch..."
	make clean
	make build
	make up
	@echo "✓ Rebuild complete!"
