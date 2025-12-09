# Quick Start Guide

Get the Auto-Ops pipeline running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.9+)
python3 --version

# Check Docker (optional but recommended)
docker --version
docker-compose --version
```

## Step 1: Setup Environment

```bash
# Clone or navigate to project
cd Auto-Ops

# Run setup script
./scripts/setup.sh

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 2: Train Initial Model

```bash
# This downloads data and trains the baseline model
python src/train.py --month 2023-01
```

Expected output:
- Downloads ~100MB of NYC taxi data
- Preprocesses data
- Trains Random Forest model
- Logs to MLflow
- Saves model to `models/` directory

## Step 3: Start Model Serving

In a new terminal:

```bash
cd Auto-Ops
source venv/bin/activate
python src/serve.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 4: Test the API

In another terminal:

```bash
cd Auto-Ops
source venv/bin/activate
python src/example_usage.py
```

Or test manually:
```bash
curl http://localhost:8000/health
```

## Step 5: Monitor for Drift

```bash
# Monitor drift (this will sample predictions from the API)
python src/drift_detector.py --api-url http://localhost:8000 --samples 100
```

## Optional: Use Docker

```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up -d

# Check services
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f model-serving
```

## Next Steps

1. **View MLflow UI**: `mlflow ui --backend-store-uri file:./mlflow`
2. **Set up Airflow**: Follow Airflow setup in main README
3. **Configure CI/CD**: Set up GitHub Actions secrets
4. **Customize**: Edit `config.yaml` for your needs

## Common Issues

**Port 8000 already in use?**
```bash
# Change port in config.yaml or use:
python src/serve.py  # Edit serve.py to change port
```

**Data download fails?**
- Check internet connection
- Verify NYC taxi data URL is accessible
- Try a different month: `--month 2023-02`

**Model not found?**
- Ensure Step 2 completed successfully
- Check `models/` directory exists
- Verify MLflow tracking URI in config

## Success Indicators

✅ Model training completes with metrics logged  
✅ API responds to health checks  
✅ Predictions return reasonable values (5-60 minutes)  
✅ Drift detector runs without errors  

You're all set! 🎉

