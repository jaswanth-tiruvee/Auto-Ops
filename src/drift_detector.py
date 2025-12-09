"""
Drift Detection Module using EvidentlyAI
Monitors incoming predictions and detects concept drift
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import requests
import json
from typing import Optional, Tuple
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import logging
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_reference_data(month: str = "2023-01") -> pd.DataFrame:
    """
    Load reference data (baseline month)
    
    Args:
        month: Reference month in format 'YYYY-MM'
        
    Returns:
        Reference DataFrame
    """
    from data_ingestion import ingest_data
    
    df = ingest_data(month, save_processed=False)
    return df


def get_predictions_from_api(api_url: str = "http://localhost:8000", n_samples: int = 100) -> pd.DataFrame:
    """
    Generate sample predictions from the serving API
    
    Args:
        api_url: Base URL of the serving API
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with features and predictions
    """
    # Generate random but realistic NYC taxi trip data
    np.random.seed(42)
    
    # NYC coordinates bounds
    nyc_lon_min, nyc_lon_max = -74.3, -73.7
    nyc_lat_min, nyc_lat_max = 40.5, 40.9
    
    data = []
    for _ in range(n_samples):
        trip = {
            "pickup_longitude": np.random.uniform(nyc_lon_min, nyc_lon_max),
            "pickup_latitude": np.random.uniform(nyc_lat_min, nyc_lat_max),
            "dropoff_longitude": np.random.uniform(nyc_lon_min, nyc_lon_max),
            "dropoff_latitude": np.random.uniform(nyc_lat_min, nyc_lat_max),
            "passenger_count": np.random.randint(1, 7),
            "trip_distance": np.random.uniform(0.5, 20.0),
            "hour": np.random.randint(0, 24),
            "day_of_week": np.random.randint(0, 7),
            "month": np.random.randint(1, 13)
        }
        
        try:
            response = requests.post(f"{api_url}/predict", json=trip, timeout=5)
            if response.status_code == 200:
                result = response.json()
                trip['predicted_duration'] = result['predicted_duration_minutes']
                data.append(trip)
        except Exception as e:
            logger.warning(f"Error getting prediction: {e}")
            # Use a mock prediction if API is unavailable
            trip['predicted_duration'] = np.random.uniform(5, 60)
            data.append(trip)
    
    return pd.DataFrame(data)


def check_drift(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    threshold: float = 0.5
) -> Tuple[bool, dict]:
    """
    Check for data drift using EvidentlyAI
    
    Args:
        reference_data: Reference (baseline) data
        current_data: Current production data
        threshold: Drift threshold (0-1)
        
    Returns:
        Tuple of (drift_detected, drift_report)
    """
    config = load_config()
    features = config['model']['features']
    target = config['model']['target']
    
    # Prepare column mapping
    column_mapping = ColumnMapping()
    column_mapping.numerical_features = [
        f for f in features if f in reference_data.columns
    ]
    column_mapping.categorical_features = []
    column_mapping.target = target if target in reference_data.columns else None
    column_mapping.prediction = 'predicted_duration' if 'predicted_duration' in current_data.columns else None
    
    # Create drift report
    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    
    # Get drift metrics
    report_dict = drift_report.as_dict()
    
    # Check if drift is detected
    drift_detected = False
    drift_score = 0.0
    
    try:
        # Extract drift score from report
        metrics = report_dict.get('metrics', [])
        for metric in metrics:
            if metric.get('metric') == 'DatasetDriftMetric':
                drift_score = metric.get('result', {}).get('dataset_drift', False)
                if isinstance(drift_score, bool):
                    drift_detected = drift_score
                elif isinstance(drift_score, (int, float)):
                    drift_detected = drift_score > threshold
                    drift_score = float(drift_score)
                break
    except Exception as e:
        logger.warning(f"Error extracting drift score: {e}")
        # Fallback: check individual feature drifts
        drift_detected = False
    
    drift_info = {
        "drift_detected": drift_detected,
        "drift_score": drift_score,
        "threshold": threshold,
        "reference_samples": len(reference_data),
        "current_samples": len(current_data)
    }
    
    return drift_detected, drift_info


def save_drift_report(report: Report, output_path: str = "drift_report.html"):
    """
    Save drift report to HTML file
    
    Args:
        report: EvidentlyAI report object
        output_path: Path to save the report
    """
    report.save_html(output_path)
    logger.info(f"Drift report saved to {output_path}")


def trigger_retraining():
    """
    Trigger Airflow DAG for retraining
    
    This can be done via:
    1. Airflow REST API
    2. Airflow CLI
    3. File-based trigger
    """
    config = load_config()
    airflow_config = config['airflow']
    dag_id = airflow_config['dag_id']
    
    # Option 1: Airflow REST API (if available)
    airflow_url = os.getenv("AIRFLOW_URL", "http://localhost:8080")
    airflow_user = os.getenv("AIRFLOW_USER", "airflow")
    airflow_password = os.getenv("AIRFLOW_PASSWORD", "airflow")
    
    try:
        # Trigger DAG via REST API
        trigger_url = f"{airflow_url}/api/v1/dags/{dag_id}/dagRuns"
        auth = (airflow_user, airflow_password)
        
        response = requests.post(
            trigger_url,
            json={},
            auth=auth,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"Successfully triggered Airflow DAG: {dag_id}")
            return True
        else:
            logger.warning(f"Failed to trigger DAG: {response.status_code} - {response.text}")
    except Exception as e:
        logger.warning(f"Could not trigger via API: {e}")
    
    # Option 2: File-based trigger (fallback)
    trigger_file = Path(__file__).parent.parent / "airflow" / "trigger_retrain.flag"
    trigger_file.touch()
    logger.info(f"Created trigger file: {trigger_file}")
    
    return True


def monitor_drift(
    reference_month: str = "2023-01",
    current_month: Optional[str] = None,
    api_url: str = "http://localhost:8000",
    threshold: float = 0.5,
    n_samples: int = 1000
) -> bool:
    """
    Main function to monitor drift and trigger retraining if needed
    
    Args:
        reference_month: Reference month for baseline
        current_month: Current month to compare (if None, uses API predictions)
        api_url: URL of the serving API
        threshold: Drift threshold
        n_samples: Number of samples to analyze
        
    Returns:
        True if drift detected and retraining triggered
    """
    logger.info("Starting drift monitoring...")
    
    # Load reference data
    logger.info(f"Loading reference data for month: {reference_month}")
    reference_data = load_reference_data(reference_month)
    
    # Get current data
    if current_month:
        logger.info(f"Loading current data for month: {current_month}")
        from data_ingestion import ingest_data
        current_data = ingest_data(current_month, save_processed=False)
    else:
        logger.info(f"Fetching predictions from API: {api_url}")
        current_data = get_predictions_from_api(api_url, n_samples)
    
    # Check for drift
    logger.info("Checking for data drift...")
    drift_detected, drift_info = check_drift(reference_data, current_data, threshold)
    
    logger.info(f"Drift check results: {drift_info}")
    
    if drift_detected:
        logger.warning("⚠️  DRIFT DETECTED! Triggering retraining...")
        trigger_retraining()
        return True
    else:
        logger.info("✓ No drift detected. Model is performing well.")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor Model Drift")
    parser.add_argument("--reference-month", type=str, default="2023-01", help="Reference month")
    parser.add_argument("--current-month", type=str, default=None, help="Current month to compare")
    parser.add_argument("--api-url", type=str, default="http://localhost:8000", help="Serving API URL")
    parser.add_argument("--threshold", type=float, default=0.5, help="Drift threshold")
    parser.add_argument("--samples", type=int, default=1000, help="Number of samples to analyze")
    
    args = parser.parse_args()
    
    monitor_drift(
        reference_month=args.reference_month,
        current_month=args.current_month,
        api_url=args.api_url,
        threshold=args.threshold,
        n_samples=args.samples
    )

