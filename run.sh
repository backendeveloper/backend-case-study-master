#!/usr/bin/env bash

# Enable error handling
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
function print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

function print_success() {
    echo -e "${GREEN}==>${NC} $1"
}

function print_error() {
    echo -e "${RED}==>${NC} $1"
}

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    print_step "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
print_step "Installing dependencies..."
pip install -e .
print_success "Dependencies installed"

# Start PostgreSQL with Docker
print_step "Starting PostgreSQL with Docker..."
chmod +x docker-entrypoint-initdb.d/create-multiple-databases.sh
docker-compose up -d
print_success "PostgreSQL started"

# Wait for PostgreSQL to be ready
print_step "Waiting for PostgreSQL to be ready..."
sleep 5
print_success "PostgreSQL is ready"

# Setup HealthAI database
print_step "Setting up HealthAI database..."
cd healthai
python setup_db.py
cd ..
print_success "HealthAI database setup complete"

# Setup TravelAI database
print_step "Setting up TravelAI database..."
cd travelai
python setup_db.py
cd ..
print_success "TravelAI database setup complete"

# Start applications
print_step "Starting applications..."
cd healthai
uvicorn src.main:app --reload --port 8000 &
HEALTHAI_PID=$!
cd ..

cd travelai
uvicorn src.main:app --reload --port 8001 &
TRAVELAI_PID=$!
cd ..

print_success "Applications started successfully!"
echo -e "${GREEN}HealthAI:${NC} http://localhost:8000"
echo -e "${GREEN}TravelAI:${NC} http://localhost:8001"
echo -e "\nPress Ctrl+C to stop all applications"

# Handle cleanup on exit
function cleanup() {
    print_step "Stopping applications..."
    kill -9 $HEALTHAI_PID $TRAVELAI_PID 2>/dev/null || true
    print_success "Applications stopped"
}

trap cleanup EXIT

# Wait for both processes
wait $HEALTHAI_PID $TRAVELAI_PID