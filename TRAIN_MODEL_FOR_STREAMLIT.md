# Training Model for Streamlit Cloud

Your Streamlit app is deployed but needs a trained model. Here are options:

## Option 1: Train Model Locally & Commit (Recommended for Demo)

### Step 1: Train Model Locally

```bash
cd /Users/abc/Downloads/Auto-Ops
source venv/bin/activate
python src/train.py --month 2023-01
```

This will create:
- `models/model.joblib` - The trained model
- `models/features.joblib` - Feature names
- `mlflow/` - MLflow tracking data

### Step 2: Commit Model Files

```bash
# Add model files (if they're not too large)
git add models/model.joblib models/features.joblib
git commit -m "Add trained model for Streamlit deployment"
git push
```

**Note:** If model files are too large (>100MB), use Git LFS or Option 2.

### Step 3: Streamlit Cloud Will Auto-Deploy

Streamlit Cloud will automatically redeploy and the model will be available!

---

## Option 2: Train During Streamlit Cloud Build (Advanced)

You can modify the app to train the model on first load, but this is slower.

---

## Option 3: Use MLflow with External Storage

1. Set up MLflow with S3/PostgreSQL
2. Train model and register in MLflow
3. Update `streamlit_app.py` to load from MLflow URI
4. Add MLflow credentials to Streamlit Cloud secrets

---

## Quick Fix: Train Now

Run this locally:

```bash
cd /Users/abc/Downloads/Auto-Ops
source venv/bin/activate
python src/train.py --month 2023-01
```

Then check if model files are small enough to commit:

```bash
ls -lh models/
```

If `model.joblib` is < 50MB, commit it:

```bash
git add models/model.joblib models/features.joblib
git commit -m "Add trained model"
git push
```

---

## Current Status

Your app is **deployed and working** - it just needs a model file to make predictions!

The warning "Model not found" is expected until you add the model files.

