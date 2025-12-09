"""
Model Training Module with MLflow Tracking
Trains a regression model to predict NYC taxi trip duration
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging
from datetime import datetime

from data_ingestion import ingest_data, load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_model(df: pd.DataFrame, model_dir: str = "models") -> tuple:
    """
    Train a Random Forest model to predict trip duration
    
    Args:
        df: Preprocessed DataFrame
        model_dir: Directory to save the model
        
    Returns:
        Tuple of (model, metrics)
    """
    config = load_config()
    target = config['model']['target']
    features = config['model']['features']
    
    # Prepare features and target
    X = df[features].copy()
    y = df[target].copy()
    
    logger.info(f"Training on {len(X)} samples with {len(features)} features")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model (smaller for GitHub compatibility)
    model = RandomForestRegressor(
        n_estimators=50,  # Reduced from 100 for smaller file size
        max_depth=15,     # Reduced from 20
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    logger.info("Training Random Forest model...")
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'train_mae': mean_absolute_error(y_train, y_pred_train),
        'test_mae': mean_absolute_error(y_test, y_pred_test),
        'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
        'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
        'train_r2': r2_score(y_train, y_pred_train),
        'test_r2': r2_score(y_test, y_pred_test),
    }
    
    logger.info("Model training complete!")
    logger.info(f"Test MAE: {metrics['test_mae']:.2f} minutes")
    logger.info(f"Test RMSE: {metrics['test_rmse']:.2f} minutes")
    logger.info(f"Test R²: {metrics['test_r2']:.3f}")
    
    # Save model locally
    Path(model_dir).mkdir(parents=True, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Save feature names for serving
    feature_path = os.path.join(model_dir, "features.joblib")
    joblib.dump(features, feature_path)
    
    return model, metrics, features


def log_to_mlflow(model, metrics: dict, features: list, month: str):
    """
    Log model and metrics to MLflow
    
    Args:
        model: Trained model
        metrics: Dictionary of metrics
        features: List of feature names
        month: Month identifier for the training data
    """
    config = load_config()
    mlflow_config = config['mlflow']
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri(mlflow_config['tracking_uri'])
    mlflow.set_experiment(mlflow_config['experiment_name'])
    
    with mlflow.start_run(run_name=f"model_v1_{month}"):
        # Log parameters
        mlflow.log_param("month", month)
        mlflow.log_param("n_features", len(features))
        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 20)
        
        # Log metrics
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
        
        # Log model
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="nyc_taxi_trip_duration"
        )
        
        # Log features
        mlflow.log_param("features", ",".join(features))
        
        run_id = mlflow.active_run().info.run_id
        logger.info(f"Logged to MLflow with run_id: {run_id}")


def main(month: str = "2023-01"):
    """
    Main training function
    
    Args:
        month: Month in format 'YYYY-MM'
    """
    logger.info(f"Starting model training for month: {month}")
    
    # Ingest data
    df = ingest_data(month, save_processed=False)
    
    # Train model
    model, metrics, features = train_model(df)
    
    # Log to MLflow
    log_to_mlflow(model, metrics, features, month)
    
    logger.info("Training pipeline complete!")
    return model, metrics


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train NYC Taxi Trip Duration Model")
    parser.add_argument("--month", type=str, default="2023-01", help="Month in YYYY-MM format")
    
    args = parser.parse_args()
    
    main(args.month)

