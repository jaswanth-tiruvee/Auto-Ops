"""
Example usage script demonstrating the Auto-Ops pipeline
"""

import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:8000"


def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ API is healthy")
            return True
        else:
            print(f"✗ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ API is not accessible: {e}")
        return False


def make_prediction():
    """Make a sample prediction"""
    trip_data = {
        "trip_distance": 2.5,
        "passenger_count": 2,
        "hour": 14,
        "day_of_week": 1,
        "month": 6,
        "pickup_location_id": 161,
        "dropoff_location_id": 162
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=trip_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Prediction successful!")
            print(f"  Predicted duration: {result['predicted_duration_minutes']:.2f} minutes")
            print(f"  Model version: {result['model_version']}")
            return result
        else:
            print(f"✗ Prediction failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"✗ Prediction error: {e}")
        return None


def make_batch_predictions(n=5):
    """Make multiple predictions"""
    trips = []
    for i in range(n):
        trips.append({
            "trip_distance": 1.0 + (i * 0.5),
            "passenger_count": (i % 5) + 1,
            "hour": (i * 3) % 24,
            "day_of_week": i % 7,
            "month": (i % 12) + 1,
            "pickup_location_id": 161 + (i % 50),
            "dropoff_location_id": 162 + (i % 50)
        })
    
    try:
        response = requests.post(f"{API_URL}/predict_batch", json=trips, timeout=10)
        if response.status_code == 200:
            results = response.json()
            print(f"\n✓ Batch prediction successful! ({len(results)} predictions)")
            for i, result in enumerate(results[:3]):  # Show first 3
                print(f"  Trip {i+1}: {result['predicted_duration_minutes']:.2f} minutes")
            return results
        else:
            print(f"✗ Batch prediction failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Batch prediction error: {e}")
        return None


def get_model_info():
    """Get model information"""
    try:
        response = requests.get(f"{API_URL}/model/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print("\n✓ Model Information:")
            print(f"  Model type: {info['model_type']}")
            print(f"  Model version: {info['model_version']}")
            print(f"  Features: {', '.join(info['features'])}")
            return info
        else:
            print(f"✗ Failed to get model info: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error getting model info: {e}")
        return None


def main():
    """Main example function"""
    print("=" * 60)
    print("Auto-Ops Pipeline - Example Usage")
    print("=" * 60)
    
    # Test API health
    print("\n1. Testing API health...")
    if not test_api_health():
        print("\n⚠️  API is not running. Please start it with:")
        print("   python src/serve.py")
        print("   or")
        print("   docker-compose up model-serving")
        return
    
    # Get model info
    print("\n2. Getting model information...")
    get_model_info()
    
    # Make a prediction
    print("\n3. Making a single prediction...")
    make_prediction()
    
    # Make batch predictions
    print("\n4. Making batch predictions...")
    make_batch_predictions(5)
    
    print("\n" + "=" * 60)
    print("Example usage complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

