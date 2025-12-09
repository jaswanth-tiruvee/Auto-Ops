#!/bin/bash

# Auto-Ops Setup Script

set -e

echo "=========================================="
echo "Auto-Ops MLOps Pipeline Setup"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p data models mlflow airflow/logs airflow/plugins

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created (please update with your configurations)"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Train initial model: python src/train.py --month 2023-01"
echo "3. Start serving API: python src/serve.py"
echo "4. Or use Docker: docker-compose up -d"
echo ""

