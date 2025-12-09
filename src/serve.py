"""
Model Serving API using FastAPI
Serves the trained model for predictions
"""

import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import yaml
import mlflow
import mlflow.sklearn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NYC Taxi Trip Duration Prediction API", version="1.0.0")


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_model(model_version: str = "latest"):
    """
    Load model from MLflow or local file
    
    Args:
        model_version: Model version to load ('latest' or version number)
        
    Returns:
        Tuple of (model, features)
    """
    config = load_config()
    mlflow_config = config['mlflow']
    
    try:
        # Try loading from MLflow first
        mlflow.set_tracking_uri(mlflow_config['tracking_uri'])
        
        if model_version == "latest":
            model = mlflow.sklearn.load_model(
                model_uri=f"models:/nyc_taxi_trip_duration/latest"
            )
        else:
            model = mlflow.sklearn.load_model(
                model_uri=f"models:/nyc_taxi_trip_duration/{model_version}"
            )
        
        # Load features from config
        features = config['model']['features']
        logger.info(f"Loaded model from MLflow (version: {model_version})")
        
    except Exception as e:
        logger.warning(f"Could not load from MLflow: {e}. Trying local model...")
        
        # Fallback to local model
        model_dir = config['model']['model_dir']
        model_path = os.path.join(model_dir, "model.joblib")
        feature_path = os.path.join(model_dir, "features.joblib")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        model = joblib.load(model_path)
        features = joblib.load(feature_path) if os.path.exists(feature_path) else config['model']['features']
        logger.info("Loaded model from local file")
    
    return model, features


# Load model at startup
config = load_config()
serving_config = config['serving']
model, features = load_model(serving_config['model_version'])


class TripRequest(BaseModel):
    """Request model for trip prediction"""
    trip_distance: float = Field(..., gt=0, description="Trip distance in miles")
    passenger_count: int = Field(..., ge=1, le=6, description="Number of passengers")
    hour: int = Field(..., ge=0, le=23, description="Hour of day (0-23)")
    day_of_week: int = Field(..., ge=0, le=6, description="Day of week (0=Monday, 6=Sunday)")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    pickup_location_id: int = Field(..., ge=1, description="Pickup location ID")
    dropoff_location_id: int = Field(..., ge=1, description="Dropoff location ID")


class TripResponse(BaseModel):
    """Response model for trip prediction"""
    predicted_duration_minutes: float = Field(..., description="Predicted trip duration in minutes")
    model_version: str = Field(..., description="Model version used")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "NYC Taxi Trip Duration Prediction API",
        "model_loaded": model is not None
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/predict", response_model=TripResponse)
async def predict(trip: TripRequest):
    """
    Predict trip duration for a given trip
    
    Args:
        trip: TripRequest with trip details
        
    Returns:
        TripResponse with predicted duration
    """
    try:
        # Prepare features in correct order
        feature_values = [
            trip.trip_distance,
            trip.passenger_count,
            trip.hour,
            trip.day_of_week,
            trip.month,
            trip.pickup_location_id,
            trip.dropoff_location_id
        ]
        
        # Create DataFrame
        X = pd.DataFrame([feature_values], columns=features)
        
        # Make prediction
        prediction = model.predict(X)[0]
        
        return TripResponse(
            predicted_duration_minutes=float(prediction),
            model_version=serving_config['model_version']
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_batch")
async def predict_batch(trips: List[TripRequest]):
    """
    Predict trip duration for multiple trips
    
    Args:
        trips: List of TripRequest objects
        
    Returns:
        List of predictions
    """
    try:
        # Prepare features
        feature_values = []
        for trip in trips:
            feature_values.append([
                trip.trip_distance,
                trip.passenger_count,
                trip.hour,
                trip.day_of_week,
                trip.month,
                trip.pickup_location_id,
                trip.dropoff_location_id
            ])
        
        # Create DataFrame
        X = pd.DataFrame(feature_values, columns=features)
        
        # Make predictions
        predictions = model.predict(X)
        
        return [
            {
                "predicted_duration_minutes": float(pred),
                "model_version": serving_config['model_version']
            }
            for pred in predictions
        ]
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model/info")
async def model_info():
    """Get information about the loaded model"""
    return {
        "features": features,
        "model_type": type(model).__name__,
        "model_version": serving_config['model_version']
    }


if __name__ == "__main__":
    config = load_config()
    serving_config = config['serving']
    
    uvicorn.run(
        app,
        host=serving_config['host'],
        port=serving_config['port']
    )

