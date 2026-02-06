.PHONY: help install dev db-up db-down db-migrate db-upgrade db-downgrade db-init db-setup run test clean kill-port

help:
	@echo "Elenchos - Comandos disponibles:"
	@echo "  make install       - Instalar dependencias"
	@echo "  make dev           - Instalar dependencias de desarrollo"
	@echo "  make db-up         - Iniciar servicios de base de datos"
	@echo "  make db-down       - Detener servicios de base de datos"
	@echo "  make db-setup      - Configurar base de datos (crear tablas)"
	@echo "  make db-migrate    - Crear nueva migración"
	@echo "  make db-upgrade    - Aplicar migraciones"
	@echo "  make db-downgrade  - Revertir última migración"
	@echo "  make db-init       - Inicializar base de datos (legacy)"
	@echo "  make run           - Iniciar servidor de desarrollo"
	@echo "  make test          - Ejecutar tests"
	@echo "  make test-cov      - Ejecutar tests con cobertura"
	@echo "  make kill-port     - Matar proceso en puerto 8000"
	@echo "  make clean         - Limpiar archivos temporales y puerto 8000"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install black ruff pytest-cov

db-up:
	docker compose up -d

db-down:
	docker compose down

db-setup:
	python scripts/setup_database.py

db-migrate:
	alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-init:
	python scripts/init_db.py

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html

kill-port:
	@echo "Matando proceso en puerto 8000..."
	@lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "Puerto 8000 ya está libre"

clean: kill-port
	@echo "Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".hypothesis" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "Limpieza completada"
