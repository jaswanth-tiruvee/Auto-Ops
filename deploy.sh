#!/bin/bash

# Auto-Ops Deployment Script
# Usage: ./deploy.sh [local|docker|cloud]

set -e

DEPLOYMENT_TYPE=${1:-local}

echo "=========================================="
echo "Auto-Ops Deployment Script"
echo "Deployment Type: $DEPLOYMENT_TYPE"
echo "=========================================="

case $DEPLOYMENT_TYPE in
  local)
    echo "Deploying locally..."
    source venv/bin/activate
    python src/serve.py
    ;;
    
  docker)
    echo "Building Docker image..."
    docker build -t auto-ops-model:latest -f docker/Dockerfile .
    
    echo "Stopping existing containers..."
    docker stop auto-ops-api 2>/dev/null || true
    docker rm auto-ops-api 2>/dev/null || true
    
    echo "Starting container..."
    docker run -d \
      --name auto-ops-api \
      -p 8000:8000 \
      -v $(pwd)/models:/app/models \
      -v $(pwd)/mlflow:/app/mlflow \
      -v $(pwd)/data:/app/data \
      auto-ops-model:latest
    
    echo "Waiting for API to start..."
    sleep 5
    
    echo "Checking health..."
    curl -f http://localhost:8000/health || echo "Health check failed"
    
    echo "✅ Deployment complete!"
    echo "API available at: http://localhost:8000"
    echo "View logs: docker logs -f auto-ops-api"
    ;;
    
  docker-compose)
    echo "Starting with Docker Compose..."
    docker-compose -f docker/docker-compose.yml up -d
    
    echo "Waiting for services..."
    sleep 10
    
    echo "✅ Services started!"
    echo "Model API: http://localhost:8000"
    echo "MLflow UI: http://localhost:5000"
    echo "Airflow UI: http://localhost:8080"
    ;;
    
  cloud)
    echo "Cloud deployment requires manual configuration."
    echo "See DEPLOYMENT.md for cloud-specific instructions."
    echo ""
    echo "Options:"
    echo "  - AWS: ECS, EC2, Lambda"
    echo "  - GCP: Cloud Run, GKE"
    echo "  - Azure: Container Instances, AKS"
    ;;
    
  *)
    echo "Unknown deployment type: $DEPLOYMENT_TYPE"
    echo "Usage: ./deploy.sh [local|docker|docker-compose|cloud]"
    exit 1
    ;;
esac

