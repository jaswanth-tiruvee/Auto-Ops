"""
Data Ingestion Module for NYC Green Taxi Trip Data
Downloads and preprocesses data for model training
"""

import os
import pandas as pd
import requests
from pathlib import Path
import yaml
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def download_nyc_taxi_data(month: str, data_dir: str = "data") -> str:
    """
    Download NYC Green Taxi trip data for a specific month
    
    Args:
        month: Month in format 'YYYY-MM' (e.g., '2023-01')
        data_dir: Directory to save the data
        
    Returns:
        Path to downloaded file
    """
    config = load_config()
    base_url = config['data']['source_url']
    
    # Create data directory if it doesn't exist
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # Format: green_tripdata_YYYY-MM.parquet
    filename = f"green_tripdata_{month}.parquet"
    url = f"{base_url}/{filename}"
    filepath = os.path.join(data_dir, filename)
    
    # Check if file already exists
    if os.path.exists(filepath):
        logger.info(f"File already exists: {filepath}")
        return filepath
    
    logger.info(f"Downloading data from {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Successfully downloaded {filename}")
        return filepath
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading data: {e}")
        raise


def preprocess_data(filepath: str) -> pd.DataFrame:
    """
    Preprocess NYC taxi data for model training
    
    Args:
        filepath: Path to the parquet file
        
    Returns:
        Preprocessed DataFrame
    """
    logger.info(f"Loading data from {filepath}")
    df = pd.read_parquet(filepath)
    
    logger.info(f"Original data shape: {df.shape}")
    
    # Filter out invalid data
    df = df[
        (df['trip_distance'] > 0) &
        (df['trip_distance'] < 100) &  # Reasonable max distance
        (df['passenger_count'] > 0) &
        (df['passenger_count'] <= 6) &
        (df['PULocationID'].notna()) &
        (df['DOLocationID'].notna())
    ].copy()
    
    # Convert pickup/dropoff datetime
    if 'lpep_pickup_datetime' in df.columns:
        df['pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    elif 'pickup_datetime' in df.columns:
        df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    
    if 'lpep_dropoff_datetime' in df.columns:
        df['dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    elif 'dropoff_datetime' in df.columns:
        df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    
    # Calculate trip duration in minutes
    df['trip_duration_minutes'] = (
        (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
    )
    
    # Filter out unrealistic trip durations (0-180 minutes)
    df = df[(df['trip_duration_minutes'] > 0) & (df['trip_duration_minutes'] <= 180)].copy()
    
    # Extract temporal features
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['month'] = df['pickup_datetime'].dt.month
    
    # Use location IDs as features (convert to numeric)
    df['pickup_location_id'] = df['PULocationID'].astype(int)
    df['dropoff_location_id'] = df['DOLocationID'].astype(int)
    
    # Select features - use available columns
    config = load_config()
    # Update feature list to match available data
    available_features = [
        'trip_distance',
        'passenger_count',
        'hour',
        'day_of_week',
        'month',
        'pickup_location_id',
        'dropoff_location_id'
    ]
    
    # Add target
    available_features.append(config['model']['target'])
    
    # Select only available columns
    df = df[[col for col in available_features if col in df.columns]].copy()
    
    # Remove rows with missing values
    df = df.dropna()
    
    logger.info(f"Preprocessed data shape: {df.shape}")
    logger.info(f"Features: {list(df.columns)}")
    
    return df


def ingest_data(month: str, save_processed: bool = True) -> pd.DataFrame:
    """
    Main function to ingest and preprocess data
    
    Args:
        month: Month in format 'YYYY-MM'
        save_processed: Whether to save processed data to CSV
        
    Returns:
        Preprocessed DataFrame
    """
    config = load_config()
    data_dir = config['data']['data_dir']
    
    # Download data
    filepath = download_nyc_taxi_data(month, data_dir)
    
    # Preprocess data
    df = preprocess_data(filepath)
    
    # Save processed data
    if save_processed:
        processed_path = os.path.join(data_dir, f"processed_{month}.csv")
        df.to_csv(processed_path, index=False)
        logger.info(f"Saved processed data to {processed_path}")
    
    return df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest NYC Taxi Trip Data")
    parser.add_argument("--month", type=str, default="2023-01", help="Month in YYYY-MM format")
    parser.add_argument("--save", action="store_true", help="Save processed data")
    
    args = parser.parse_args()
    
    df = ingest_data(args.month, save_processed=args.save)
    print(f"\nData ingestion complete!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())

