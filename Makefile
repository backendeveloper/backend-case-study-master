.PHONY: setup db-up db-down setup-healthai setup-travelai migrate-healthai migrate-travelai run-healthai run-travelai run-all clean help init-migrations

help:
	@echo "Available commands:"
	@echo "  make setup           - Create virtual environment and install dependencies"
	@echo "  make db-up           - Start PostgreSQL database with Docker"
	@echo "  make db-down         - Stop PostgreSQL database"
	@echo "  make setup-healthai  - Setup HealthAI application"
	@echo "  make setup-travelai  - Setup TravelAI application"
	@echo "  make init-migrations - Initialize Alembic migrations for both applications"
	@echo "  make migrate-healthai - Run database migrations for HealthAI"
	@echo "  make migrate-travelai - Run database migrations for TravelAI"
	@echo "  make run-healthai    - Run HealthAI application"
	@echo "  make run-travelai    - Run TravelAI application"
	@echo "  make run-all         - Run both applications (in background)"
	@echo "  make clean           - Remove virtual environment and cached files"

setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	. venv/bin/activate && pip install -e .
	@echo "Setup complete! Activate the environment with: source venv/bin/activate"

db-up:
	@echo "Starting PostgreSQL with Docker..."
	chmod +x docker-entrypoint-initdb.d/create-multiple-databases.sh
	docker-compose up -d
	@echo "Waiting for PostgreSQL to be ready..."
	sleep 5

db-down:
	@echo "Stopping PostgreSQL..."
	docker-compose down
	@echo "PostgreSQL stopped"

setup-healthai: db-up
	@echo "Setting up HealthAI application..."
	cd healthai && . ../venv/bin/activate && python setup_db.py
	@echo "HealthAI application setup complete"

setup-travelai: db-up
	@echo "Setting up TravelAI application..."
	cd travelai && . ../venv/bin/activate && python setup_db.py
	@echo "TravelAI application setup complete"

init-migrations: db-up
	@echo "Initializing Alembic migrations..."

	@echo "Setting up Alembic for HealthAI..."
	mkdir -p healthai/migrations
	cd healthai && . ../venv/bin/activate && \
		alembic init migrations && \
		sed -i'.bak' 's/sqlalchemy.url = driver:\/\/user:pass@localhost\/dbname/sqlalchemy.url = postgresql+asyncpg:\/\/postgres:postgres@localhost:5432\/healthai/' alembic.ini && \
		rm -f alembic.ini.bak

	@echo "Setting up Alembic for TravelAI..."
	mkdir -p travelai/migrations
	cd travelai && . ../venv/bin/activate && \
		alembic init migrations && \
		sed -i'.bak' 's/sqlalchemy.url = driver:\/\/user:pass@localhost\/dbname/sqlalchemy.url = postgresql+asyncpg:\/\/postgres:postgres@localhost:5432\/travelai/' alembic.ini && \
		rm -f alembic.ini.bak

	@echo "Alembic setup complete"

migrate-healthai: db-up
	@echo "Running HealthAI database migrations..."
	cd healthai && . ../venv/bin/activate && alembic revision --autogenerate -m "Create ledger tables" && alembic upgrade head
	@echo "HealthAI database migration complete"

migrate-travelai: db-up
	@echo "Running TravelAI database migrations..."
	cd travelai && . ../venv/bin/activate && alembic revision --autogenerate -m "Create ledger tables" && alembic upgrade head
	@echo "TravelAI database migration complete"

run-healthai: setup-healthai
	@echo "Starting HealthAI application..."
	cd healthai && . ../venv/bin/activate && PYTHONPATH="$(PWD)" uvicorn src.main:app --reload --port 8000

run-travelai: setup-travelai
	@echo "Starting TravelAI application..."
	cd travelai && . ../venv/bin/activate && PYTHONPATH="$(PWD)" uvicorn src.main:app --reload --port 8001

run-all: setup-healthai setup-travelai
	@echo "Starting both applications..."
	cd healthai && . ../venv/bin/activate && PYTHONPATH="$(PWD)" uvicorn src.main:app --reload --port 8000 & \
	cd travelai && . ../venv/bin/activate && PYTHONPATH="$(PWD)" uvicorn src.main:app --reload --port 8001 &
	@echo "Applications running at:"
	@echo "  - HealthAI: http://localhost:8000"
	@echo "  - TravelAI: http://localhost:8001"
	@echo "To stop, use Ctrl+C and then run: kill %1 %2"

clean:
	@echo "Cleaning up..."
	rm -rf venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete"