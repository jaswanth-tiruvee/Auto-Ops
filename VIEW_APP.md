# How to View and Use the Auto-Ops App

## 🌐 Web Interface (FastAPI Interactive Docs)

The easiest way to interact with the app is through the **automatic API documentation**:

### 1. Open in Your Browser

**Swagger UI (Interactive):**
```
http://localhost:8000/docs
```

**ReDoc (Alternative Documentation):**
```
http://localhost:8000/redoc
```

### 2. What You Can Do in the Browser

- **View all API endpoints** - See all available endpoints
- **Test predictions** - Click "Try it out" on any endpoint
- **Make predictions** - Fill in the form and get real predictions
- **View request/response schemas** - Understand the data format
- **See example requests** - Copy-paste ready examples

### 3. Quick Test in Browser

1. Go to `http://localhost:8000/docs`
2. Click on `POST /predict` endpoint
3. Click "Try it out"
4. Fill in the example data:
   ```json
   {
     "trip_distance": 2.5,
     "passenger_count": 2,
     "hour": 14,
     "day_of_week": 1,
     "month": 6,
     "pickup_location_id": 161,
     "dropoff_location_id": 162
   }
   ```
5. Click "Execute"
6. See the prediction result!

## 📊 MLflow UI (Model Tracking)

View your trained models and experiments:

```bash
# Start MLflow UI
mlflow ui --backend-store-uri file:./mlflow

# Then open in browser:
# http://localhost:5000
```

In MLflow UI you can:
- View all model training runs
- Compare model metrics
- Download model artifacts
- View model parameters

## 🖥️ Command Line Interface

### Test the API
```bash
# Run the example script
python src/example_usage.py
```

### Make a Prediction via curl
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_distance": 2.5,
    "passenger_count": 2,
    "hour": 14,
    "day_of_week": 1,
    "month": 6,
    "pickup_location_id": 161,
    "dropoff_location_id": 162
  }'
```

### Check API Health
```bash
curl http://localhost:8000/health
```

### Get Model Info
```bash
curl http://localhost:8000/model/info
```

## 🚀 Starting the App

If the API is not running:

```bash
cd /Users/abc/Downloads/Auto-Ops
source venv/bin/activate
python src/serve.py
```

The API will start on `http://localhost:8000`

## 📱 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with service info |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI documentation |
| `/redoc` | GET | ReDoc documentation |
| `/predict` | POST | Single trip prediction |
| `/predict_batch` | POST | Batch predictions |
| `/model/info` | GET | Model information |

## 🎯 Quick Start

1. **Open browser**: Go to `http://localhost:8000/docs`
2. **Test prediction**: Use the interactive form
3. **View results**: See predicted trip duration in minutes

That's it! The FastAPI docs make it super easy to interact with the API.

