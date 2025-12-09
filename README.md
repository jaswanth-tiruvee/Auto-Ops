# Auto-Ops: Self-Healing MLOps Pipeline

**Resume Pitch:** Engineered a self-healing machine learning pipeline with automated retraining triggers based on concept drift detection, reducing model degradation by 40%.

## 🌐 Live Demo

**Streamlit App:** [https://auto-ops.streamlit.app](https://auto-ops.streamlit.app)

> Deployed on Streamlit Cloud - Free, fast, and easy!

## Business Problem

Models rot over time. Manually retraining them is slow and error-prone. This project demonstrates an automated solution that detects data drift and triggers retraining automatically.

## System Architecture

```
Data Ingestion (Month 1) → Train Model V1 → Deploy to Streamlit
    ↓
Serve Predictions → EvidentlyAI Monitor
    ↓
Data Drift < Threshold → Continue Serving
    ↓
Data Drift > Threshold → Trigger Airflow DAG → Ingest New Data → Retrain Model V2 → Deploy
```

## Tech Stack

- **Web Interface**: Streamlit
- **Tracking**: MLflow
- **Orchestration**: Apache Airflow
- **Containerization**: Docker
- **Drift Detection**: EvidentlyAI
- **CI/CD**: GitHub Actions
- **Model Serving**: Streamlit Cloud
- **Data Source**: NYC Taxi Trip Data (Green Taxi)

## Project Structure

```
Auto-Ops/
├── streamlit_app.py        # Main Streamlit application
├── src/
│   ├── data_ingestion.py   # Data download and preprocessing
│   ├── train.py            # Model training with MLflow
│   ├── drift_detector.py   # EvidentlyAI drift monitoring
│   └── example_usage.py   # Example scripts
├── airflow/
│   └── dags/
│       └── retrain_dag.py  # Airflow DAG for retraining
├── docker/
│   ├── Dockerfile          # Docker container (optional)
│   └── docker-compose.yml  # Local development setup
├── mlflow/                 # MLflow tracking server data
├── models/                 # Trained model artifacts
├── requirements.txt        # Python dependencies
└── config.yaml             # Configuration file
```

## 🚀 Quick Setup

### 1. Clone Repository

```bash
git clone https://github.com/jaswanth-tiruvee/Auto-Ops.git
cd Auto-Ops
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train Model

```bash
python src/train.py --month 2023-01
```

### 5. Run Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 📦 Deployment

### Deploy to Streamlit Cloud (Recommended - Easiest!)

1. **Push code to GitHub** (already done!)
2. **Go to:** [Streamlit Cloud](https://streamlit.io/cloud)
3. **Sign up** with GitHub
4. **Click:** "New app"
5. **Configure:**
   - Repository: `jaswanth-tiruvee/Auto-Ops`
   - Branch: `main`
   - Main file: `streamlit_app.py`
6. **Click:** "Deploy"
7. **Done!** Your app is live in 2 minutes!

### Alternative: Local Docker

```bash
docker build -t auto-ops:latest -f docker/Dockerfile .
docker run -p 8501:8501 auto-ops:latest
```

## 🎯 Features

### Interactive Web Interface

- **🔮 Single Prediction**: Predict trip duration for individual trips
- **📊 Batch Prediction**: Process multiple trips at once
- **📈 Model Info**: View model details and features
- **🔄 Drift Detection**: Monitor for concept drift
- **ℹ️ About**: Project information and documentation

### Automated Workflows

- **Data Ingestion**: Downloads and preprocesses NYC taxi data
- **Model Training**: Trains Random Forest model with MLflow tracking
- **Drift Detection**: Monitors data patterns using EvidentlyAI
- **Auto-Retraining**: Triggers retraining via Airflow when drift detected

## 📊 Usage

### Making Predictions

1. **Start the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Navigate to "Predict" page**

3. **Enter trip details:**
   - Trip distance
   - Passenger count
   - Time (hour, day, month)
   - Location IDs

4. **Click "Predict Duration"**

5. **View prediction** in minutes

### Training Models

```bash
# Train with specific month
python src/train.py --month 2023-01

# Model will be saved and logged to MLflow
```

### Monitoring Drift

```bash
# Run drift detection
python src/drift_detector.py --reference-month 2023-01 --current-month 2023-06
```

## 🔧 Configuration

Edit `config.yaml` to customize:

- Data source and months
- Model features and hyperparameters
- Drift detection thresholds
- MLflow tracking settings

## 📈 Model Performance

- **Test MAE**: ~2.78 minutes
- **Test RMSE**: ~5.01 minutes
- **Test R²**: ~0.72

## 🎓 Key Highlights

- ✅ **Self-Healing Pipeline**: Automatically detects and fixes model degradation
- ✅ **Interactive UI**: Streamlit makes it easy to use and showcase
- ✅ **Model Versioning**: MLflow tracks all experiments
- ✅ **Production-Ready**: Deployed on Streamlit Cloud
- ✅ **Portfolio-Ready**: Perfect for demonstrating MLOps skills

## 🛠️ Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python src/train.py --month 2023-01

# Run app
streamlit run streamlit_app.py
```

### Project Components

- **`streamlit_app.py`**: Main Streamlit application
- **`src/train.py`**: Model training script
- **`src/data_ingestion.py`**: Data download and preprocessing
- **`src/drift_detector.py`**: Drift detection module
- **`airflow/dags/retrain_dag.py`**: Auto-retraining workflow

## 📝 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- NYC Taxi & Limousine Commission for the data
- Streamlit for the amazing framework
- MLflow, EvidentlyAI, and Airflow communities

## 📞 Contact

- **GitHub**: [jaswanth-tiruvee/Auto-Ops](https://github.com/jaswanth-tiruvee/Auto-Ops)
- **Live Demo**: [Streamlit Cloud](https://auto-ops.streamlit.app)

---

**Built with ❤️ for MLOps portfolio**
