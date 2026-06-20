#!/bin/bash
# Start FertilityPro Backend Application
# Usage: bash start.sh [environment] or ./start.sh [environment]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default environment
ENV=${1:-development}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     FertilityPro Backend Service       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"

# Check Python
echo -e "\n${YELLOW}▶ Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 tidak ditemukan${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION}${NC}"

# Check virtual environment
echo -e "\n${YELLOW}▶ Checking Virtual Environment...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment tidak ditemukan, membuat...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "\n${YELLOW}▶ Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check model files
echo -e "\n${YELLOW}▶ Checking model files...${NC}"
MODEL_DIR="../model"
REQUIRED_FILES=("best_model.pkl" "preprocessor.pkl" "label_encoder.pkl" "feature_names.pkl")

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$MODEL_DIR/$file" ]; then
        echo -e "${RED}✗ Model file not found: $MODEL_DIR/$file${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ All model files present${NC}"

# Create logs directory
mkdir -p logs

# Export environment variables
export FLASK_ENV=$ENV
export FLASK_DEBUG=$([ "$ENV" = "development" ] && echo "True" || echo "False")

# Start application
echo -e "\n${YELLOW}▶ Starting FertilityPro Backend (${ENV})...${NC}"
echo -e "${YELLOW}▶ Server akan berjalan di: http://0.0.0.0:5000${NC}"
echo -e "${YELLOW}▶ Tekan Ctrl+C untuk menghentikan${NC}\n"

# Choose start method based on environment
if [ "$ENV" = "production" ]; then
    echo -e "${YELLOW}▶ Using Gunicorn (Production)${NC}"
    if ! command -v gunicorn &> /dev/null; then
        pip install -q gunicorn
    fi
    gunicorn -c gunicorn_config.py app:app
else
    echo -e "${YELLOW}▶ Using Flask Development Server${NC}"
    python3 run.py
fi
