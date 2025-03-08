.PHONY: setup db-up db-down migrate-healthai migrate-travelai run-healthai run-travelai run-all clean help

help:
	@echo "Available commands:"
	@echo "  make setup           - Create virtual environment and install dependencies"
	@echo "  make db-up           - Start PostgreSQL database with Docker"
	@echo "  make db-down         - Stop PostgreSQL database"
	@echo "  make migrate-healthai - Setup HealthAI database"
	@echo "  make migrate-travelai - Setup TravelAI database"
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

migrate-healthai: db-up
	@echo "Setting up HealthAI database..."
	cd healthai && . ../venv/bin/activate && python setup_db.py
	@echo "HealthAI database setup complete"

migrate-travelai: db-up
	@echo "Setting up TravelAI database..."
	cd travelai && . ../venv/bin/activate && python setup_db.py
	@echo "TravelAI database setup complete"

run-healthai: migrate-healthai
	@echo "Starting HealthAI application..."
	cd healthai && . ../venv/bin/activate && uvicorn src.main:app --reload --port 8000

run-travelai: migrate-travelai
	@echo "Starting TravelAI application..."
	cd travelai && . ../venv/bin/activate && uvicorn src.main:app --reload --port 8001

run-all: migrate-healthai migrate-travelai
	@echo "Starting both applications..."
	cd healthai && . ../venv/bin/activate && uvicorn src.main:app --reload --port 8000 & \
	cd travelai && . ../venv/bin/activate && uvicorn src.main:app --reload --port 8001 &
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