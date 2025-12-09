"""
Airflow DAG for Automated Model Retraining
Triggers when drift is detected
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from pathlib import Path
import sys
import os

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from data_ingestion import ingest_data
from train import main as train_main
import logging

logger = logging.getLogger(__name__)

# Default arguments
default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'retrain_model_dag',
    default_args=default_args,
    description='Automated model retraining triggered by drift detection',
    schedule_interval='@daily',  # Check daily, but can be triggered manually
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['mlops', 'retraining', 'drift'],
)


def check_retrain_trigger(**context):
    """Check if retraining should be triggered"""
    trigger_file = Path(__file__).parent.parent.parent / "airflow" / "trigger_retrain.flag"
    
    if trigger_file.exists():
        logger.info("Retrain trigger file found. Proceeding with retraining...")
        trigger_file.unlink()  # Remove trigger file
        return True
    else:
        logger.info("No retrain trigger found. Skipping retraining.")
        return False


def get_latest_month(**context):
    """Get the latest month for retraining"""
    from datetime import datetime
    # Get current month or previous month
    now = datetime.now()
    # Use previous month to ensure data is available
    if now.month == 1:
        month = f"{now.year - 1}-12"
    else:
        month = f"{now.year}-{now.month - 1:02d}"
    
    logger.info(f"Using month for retraining: {month}")
    return month


def ingest_new_data(**context):
    """Ingest new data for retraining"""
    month = context['ti'].xcom_pull(task_ids='get_latest_month')
    logger.info(f"Ingesting data for month: {month}")
    
    df = ingest_data(month, save_processed=True)
    logger.info(f"Ingested {len(df)} samples")
    
    return month


def retrain_model(**context):
    """Retrain the model with new data"""
    month = context['ti'].xcom_pull(task_ids='ingest_new_data')
    logger.info(f"Retraining model with data from month: {month}")
    
    train_main(month)
    logger.info("Model retraining complete!")


def update_serving_model(**context):
    """Update the serving model (reload from MLflow)"""
    logger.info("Model updated in MLflow. Serving API will load latest version on next restart.")
    # In production, you might want to restart the serving container here
    return True


# Task definitions
check_trigger_task = PythonOperator(
    task_id='check_retrain_trigger',
    python_callable=check_retrain_trigger,
    dag=dag,
)

get_month_task = PythonOperator(
    task_id='get_latest_month',
    python_callable=get_latest_month,
    dag=dag,
)

ingest_task = PythonOperator(
    task_id='ingest_new_data',
    python_callable=ingest_new_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id='retrain_model',
    python_callable=retrain_model,
    dag=dag,
)

update_serving_task = PythonOperator(
    task_id='update_serving_model',
    python_callable=update_serving_model,
    dag=dag,
)

# Task dependencies
check_trigger_task >> get_month_task >> ingest_task >> train_task >> update_serving_task

