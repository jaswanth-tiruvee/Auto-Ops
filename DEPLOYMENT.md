# Deployment Guide for Auto-Ops

This guide covers different ways to deploy the Auto-Ops MLOps pipeline.

## 📋 Table of Contents

1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

---

## 🖥️ Local Deployment

### Option 1: Simple Local Setup (Current Setup)

**Already done!** Your app is running locally. To restart:

```bash
cd /Users/abc/Downloads/Auto-Ops
source venv/bin/activate
python src/serve.py
```

**Access:** `http://localhost:8000`

### Option 2: Using Docker Compose (Recommended for Local)

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Check status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

**Services available:**
- Model API: `http://localhost:8000`
- MLflow UI: `http://localhost:5000`
- Airflow UI: `http://localhost:8080` (user: airflow, password: airflow)

---

## 🐳 Docker Deployment

### Build and Run Single Container

```bash
# Build the Docker image
docker build -t auto-ops-model:latest -f docker/Dockerfile .

# Run the container
docker run -d \
  --name auto-ops-api \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/mlflow:/app/mlflow \
  -v $(pwd)/data:/app/data \
  auto-ops-model:latest

# Check if running
docker ps | grep auto-ops

# View logs
docker logs -f auto-ops-api

# Stop container
docker stop auto-ops-api
docker rm auto-ops-api
```

### Docker Compose (Full Stack)

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Scale services (if needed)
docker-compose -f docker/docker-compose.yml up -d --scale model-serving=3
```

---

## ☁️ Cloud Deployment

### AWS Deployment

#### Option 1: AWS ECS (Elastic Container Service)

**1. Push Docker image to ECR:**

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name auto-ops-model

# Tag and push
docker tag auto-ops-model:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/auto-ops-model:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/auto-ops-model:latest
```

**2. Create ECS Task Definition:**

```json
{
  "family": "auto-ops-model",
  "networkMode": "awsvpc",
  "containerDefinitions": [{
    "name": "auto-ops-api",
    "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/auto-ops-model:latest",
    "portMappings": [{
      "containerPort": 8000,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "MLFLOW_TRACKING_URI", "value": "s3://your-mlflow-bucket"}
    ],
    "memory": 2048,
    "cpu": 1024
  }]
}
```

**3. Create ECS Service:**

```bash
aws ecs create-service \
  --cluster your-cluster \
  --service-name auto-ops-api \
  --task-definition auto-ops-model \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

#### Option 2: AWS Lambda (Serverless)

**Note:** Requires modifications for serverless architecture. Consider using AWS Lambda with container images or API Gateway.

#### Option 3: AWS EC2

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Clone and run
git clone <your-repo>
cd Auto-Ops
docker-compose -f docker/docker-compose.yml up -d
```

**Security Group:** Open port 8000 for HTTP traffic

---

### Google Cloud Platform (GCP) Deployment

#### Option 1: Cloud Run (Serverless)

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/auto-ops-model

# Deploy to Cloud Run
gcloud run deploy auto-ops-api \
  --image gcr.io/PROJECT-ID/auto-ops-model \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --port 8000
```

#### Option 2: GKE (Google Kubernetes Engine)

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT-ID/auto-ops-model

# Create cluster
gcloud container clusters create auto-ops-cluster \
  --num-nodes=3 \
  --zone=us-central1-a

# Deploy
kubectl create deployment auto-ops-api \
  --image=gcr.io/PROJECT-ID/auto-ops-model

# Expose service
kubectl expose deployment auto-ops-api \
  --type=LoadBalancer \
  --port=80 \
  --target-port=8000
```

---

### Azure Deployment

#### Option 1: Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name auto-ops-rg --location eastus

# Create container
az container create \
  --resource-group auto-ops-rg \
  --name auto-ops-api \
  --image auto-ops-model:latest \
  --dns-name-label auto-ops-api \
  --ports 8000 \
  --memory 2 \
  --cpu 1
```

#### Option 2: Azure Kubernetes Service (AKS)

```bash
# Create AKS cluster
az aks create \
  --resource-group auto-ops-rg \
  --name auto-ops-cluster \
  --node-count 2 \
  --enable-addons monitoring

# Get credentials
az aks get-credentials --resource-group auto-ops-rg --name auto-ops-cluster

# Deploy
kubectl apply -f k8s-deployment.yaml
```

---

## 🚀 Kubernetes Deployment

### Create Kubernetes Manifests

**1. Create `k8s-deployment.yaml`:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auto-ops-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auto-ops-api
  template:
    metadata:
      labels:
        app: auto-ops-api
    spec:
      containers:
      - name: auto-ops-api
        image: auto-ops-model:latest
        ports:
        - containerPort: 8000
        env:
        - name: MLFLOW_TRACKING_URI
          value: "s3://your-mlflow-bucket"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: auto-ops-api-service
spec:
  selector:
    app: auto-ops-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**2. Deploy:**

```bash
kubectl apply -f k8s-deployment.yaml

# Check status
kubectl get pods
kubectl get services

# Get external IP
kubectl get service auto-ops-api-service
```

---

## 🔒 Production Considerations

### 1. Environment Variables

Create `.env` file for production:

```bash
# Production .env
MLFLOW_TRACKING_URI=s3://your-mlflow-bucket
MODEL_SERVING_HOST=0.0.0.0
MODEL_SERVING_PORT=8000
DRIFT_THRESHOLD=0.5
AIRFLOW_URL=https://your-airflow-instance.com
```

### 2. Database Backend for MLflow

Instead of file-based storage, use a database:

```python
# In config.yaml or environment
MLFLOW_TRACKING_URI=postgresql://user:password@host:5432/mlflow
```

### 3. Monitoring and Logging

**Add Prometheus metrics:**

```python
# In serve.py
from prometheus_client import Counter, Histogram, generate_latest

prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

**Add structured logging:**

```python
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)
```

### 4. Security

**Add authentication:**

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/predict")
async def predict(trip: TripRequest, credentials: HTTPAuthorizationCredentials = Security(security)):
    # Verify token
    if not verify_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")
    # ... rest of code
```

**Use HTTPS:**

- Deploy behind a reverse proxy (nginx, Traefik)
- Use SSL certificates (Let's Encrypt, AWS Certificate Manager)

### 5. Scaling

**Horizontal Scaling:**

```bash
# Docker Compose
docker-compose -f docker/docker-compose.yml up -d --scale model-serving=5

# Kubernetes
kubectl scale deployment auto-ops-api --replicas=5
```

**Load Balancing:**

- Use nginx, Traefik, or cloud load balancers
- Configure health checks

### 6. CI/CD Pipeline

Your GitHub Actions workflow (`.github/workflows/ci_cd.yml`) already includes:

- Linting and testing
- Docker image building
- Model training

**Add deployment step:**

```yaml
deploy:
  needs: [build-docker]
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to production
      run: |
        # Your deployment commands
        kubectl set image deployment/auto-ops-api \
          auto-ops-api=gcr.io/PROJECT-ID/auto-ops-model:${{ github.sha }}
```

---

## 📝 Quick Deployment Checklist

- [ ] Environment variables configured
- [ ] Docker image built and tested
- [ ] MLflow backend configured (database/S3)
- [ ] Security (authentication, HTTPS) implemented
- [ ] Monitoring and logging set up
- [ ] Health checks configured
- [ ] Load balancing configured
- [ ] Backup strategy for models
- [ ] CI/CD pipeline tested
- [ ] Documentation updated

---

## 🎯 Recommended Deployment Path

**For Learning/Demo:**
1. Local Docker Compose ✅ (Easiest)

**For Small Production:**
1. Cloud Run / AWS Fargate (Serverless, easy scaling)

**For Large Production:**
1. Kubernetes on GKE/EKS/AKS (Full control, scaling)

---

## 🆘 Troubleshooting

**Container won't start:**
```bash
docker logs auto-ops-api
```

**Port already in use:**
```bash
# Change port in config.yaml or use:
docker run -p 8001:8000 ...
```

**Model not found:**
- Ensure model is trained: `python src/train.py --month 2023-01`
- Check volume mounts in Docker
- Verify MLflow tracking URI

**Out of memory:**
- Increase container memory limits
- Reduce model complexity
- Use model quantization

---

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [MLflow Production Guide](https://www.mlflow.org/docs/latest/models.html#production)

---

## 💡 Next Steps

1. Choose your deployment target (local/cloud)
2. Set up environment variables
3. Build and test Docker image
4. Deploy to your chosen platform
5. Configure monitoring
6. Set up CI/CD for automated deployments

Good luck with your deployment! 🚀

