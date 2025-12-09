#!/bin/bash

# Quick Deploy Script for Auto-Ops
# This prepares your repo for GitHub and deployment

set -e

echo "=========================================="
echo "Auto-Ops - Quick Deploy Preparation"
echo "=========================================="

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
fi

# Check if model exists
if [ ! -f "models/model.joblib" ]; then
    echo "⚠️  Model not found. Training model..."
    source venv/bin/activate
    python src/train.py --month 2023-01
    echo "✅ Model trained!"
fi

# Create .gitkeep files
echo "Creating directory structure..."
mkdir -p data models mlflow
touch data/.gitkeep models/.gitkeep mlflow/.gitkeep

# Show git status
echo ""
echo "Current git status:"
git status --short | head -20

echo ""
echo "=========================================="
echo "✅ Ready for deployment!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create GitHub repo at: https://github.com/new"
echo "2. Run these commands:"
echo ""
echo "   git add ."
echo "   git commit -m 'Initial commit: Auto-Ops MLOps Pipeline'"
echo "   git remote add origin https://github.com/YOUR_USERNAME/Auto-Ops.git"
echo "   git push -u origin main"
echo ""
echo "3. Go to https://render.com and deploy!"
echo ""
echo "See DEPLOY_NOW.md for detailed instructions."
echo ""

