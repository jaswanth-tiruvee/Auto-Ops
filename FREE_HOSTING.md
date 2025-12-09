# Free Hosting Guide for Portfolio

Best free hosting options for your Auto-Ops portfolio project with GitHub integration.

## 🏆 Recommended: Render (Best for Portfolio)

**Why Render?**
- ✅ Free tier (with limitations)
- ✅ Automatic GitHub deployments
- ✅ Easy setup
- ✅ Professional URLs
- ✅ Supports Docker
- ✅ Free SSL certificates

### Setup Steps:

1. **Prepare your repo:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Render:**
   - Visit: https://render.com
   - Sign up with GitHub (free)

3. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select your Auto-Ops repository

4. **Configure:**
   - **Name:** `auto-ops-api` (or your choice)
   - **Environment:** `Docker`
   - **Dockerfile Path:** `docker/Dockerfile`
   - **Docker Context:** `.` (root)
   - **Plan:** Free
   - **Region:** Choose closest to you

5. **Environment Variables:**
   ```
   MLFLOW_TRACKING_URI=file:./mlflow
   MODEL_SERVING_HOST=0.0.0.0
   MODEL_SERVING_PORT=8000
   ```

6. **Deploy:**
   - Click "Create Web Service"
   - Wait for build (5-10 minutes)
   - Get your URL: `https://auto-ops-api.onrender.com`

**Free Tier Limits:**
- 750 hours/month (enough for 24/7)
- Spins down after 15 min inactivity (wakes on request)
- 512 MB RAM
- Perfect for portfolio!

---

## 🚂 Alternative: Railway (More Generous Free Tier)

**Why Railway?**
- ✅ $5 free credit monthly
- ✅ No sleep/spin-down
- ✅ GitHub integration
- ✅ Very easy setup

### Setup Steps:

1. **Go to Railway:**
   - Visit: https://railway.app
   - Sign up with GitHub

2. **New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your Auto-Ops repo

3. **Configure:**
   - Railway auto-detects Docker
   - Set root directory: `.`
   - Add environment variables (same as Render)

4. **Deploy:**
   - Railway builds automatically
   - Get URL: `https://auto-ops-api.up.railway.app`

**Free Tier:**
- $5 credit/month (usually enough)
- No forced sleep
- 512 MB RAM

---

## ✈️ Alternative: Fly.io (Good for Multiple Services)

**Why Fly.io?**
- ✅ Free tier available
- ✅ Great for Docker
- ✅ Multiple regions
- ✅ Good documentation

### Setup Steps:

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Initialize:**
   ```bash
   fly launch
   # Follow prompts
   ```

4. **Deploy:**
   ```bash
   fly deploy
   ```

---

## 🎯 Best Choice for Portfolio: Render

**I recommend Render because:**
1. Easiest setup (just connect GitHub)
2. Professional URLs
3. Free SSL automatically
4. Good for showcasing in portfolio
5. No credit card required

---

## 📝 Quick Setup Guide for Render

### Step 1: Prepare Your Repository

Make sure you have:
- ✅ `Dockerfile` in `docker/` directory
- ✅ `requirements.txt` in root
- ✅ All code committed to GitHub

### Step 2: Create `render.yaml` (Optional but Recommended)

Create `render.yaml` in your repo root:

```yaml
services:
  - type: web
    name: auto-ops-api
    env: docker
    dockerfilePath: ./docker/Dockerfile
    dockerContext: .
    envVars:
      - key: MLFLOW_TRACKING_URI
        value: file:./mlflow
      - key: MODEL_SERVING_HOST
        value: 0.0.0.0
      - key: MODEL_SERVING_PORT
        value: 8000
    plan: free
```

### Step 3: Deploy on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect GitHub account
4. Select your repository
5. Render will auto-detect `render.yaml` or you can configure manually
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)

### Step 4: Access Your App

Your app will be live at:
```
https://auto-ops-api.onrender.com
```

**Endpoints:**
- API Docs: `https://auto-ops-api.onrender.com/docs`
- Health: `https://auto-ops-api.onrender.com/health`
- Predict: `https://auto-ops-api.onrender.com/predict`

---

## 🔧 Important: Pre-train Model Before Deploying

Since Render's free tier has limited resources, train your model locally first:

```bash
# Train model locally
python src/train.py --month 2023-01

# Commit model files (or use MLflow)
git add models/ mlflow/
git commit -m "Add trained model"
git push
```

**Better Option:** Use MLflow with a free database (like Supabase PostgreSQL) for model storage.

---

## 🎨 Making It Portfolio-Ready

### 1. Add a Landing Page

Create a simple HTML page at the root endpoint:

```python
# In serve.py, update root endpoint:
@app.get("/")
async def root():
    return {
        "name": "Auto-Ops: Self-Healing MLOps Pipeline",
        "description": "Automated model retraining with drift detection",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict",
            "model_info": "/model/info"
        },
        "github": "https://github.com/yourusername/auto-ops"
    }
```

### 2. Update README with Live Link

Add to your README.md:

```markdown
## 🌐 Live Demo

**API:** https://auto-ops-api.onrender.com  
**Interactive Docs:** https://auto-ops-api.onrender.com/docs  
**Health Check:** https://auto-ops-api.onrender.com/health
```

### 3. Add Badge to README

```markdown
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-46E3B7?style=for-the-badge)](https://auto-ops-api.onrender.com)
```

---

## 🚨 Common Issues & Solutions

### Issue: App sleeps after 15 minutes (Render free tier)

**Solution:** 
- Use a monitoring service like UptimeRobot (free) to ping your app every 10 minutes
- Or upgrade to paid plan ($7/month)

### Issue: Build fails

**Solution:**
- Check Dockerfile path is correct
- Ensure all dependencies in requirements.txt
- Check build logs in Render dashboard

### Issue: Model not found

**Solution:**
- Train model locally and commit to repo
- Or use external storage (S3, etc.) for models
- Update MLFLOW_TRACKING_URI to use database

### Issue: Out of memory

**Solution:**
- Reduce model complexity
- Use smaller dataset for training
- Optimize Docker image size

---

## 📊 Comparison Table

| Platform | Free Tier | Sleep/Spin-down | GitHub Integration | Best For |
|----------|-----------|-----------------|-------------------|----------|
| **Render** | ✅ 750 hrs/month | ⚠️ 15 min | ✅ Yes | **Portfolio** |
| **Railway** | ✅ $5 credit | ❌ No | ✅ Yes | Development |
| **Fly.io** | ✅ Limited | ❌ No | ✅ Yes | Multiple services |
| **Heroku** | ❌ No longer free | - | ✅ Yes | Legacy |
| **Vercel** | ✅ Free | ⚠️ Yes | ✅ Yes | Frontend only |

---

## 🎯 Recommended Setup for Portfolio

1. **Host API on Render** (free, easy, professional)
2. **Use UptimeRobot** (free) to keep it awake
3. **Add live demo link** to README
4. **Document the deployment** in your portfolio

---

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Model trained and committed (or use MLflow)
- [ ] Dockerfile tested locally
- [ ] Environment variables configured
- [ ] Deployed to Render/Railway
- [ ] Tested live endpoints
- [ ] Added live demo link to README
- [ ] Added to portfolio/resume

---

## 🚀 Quick Start (Render)

```bash
# 1. Train model locally
python src/train.py --month 2023-01

# 2. Commit everything
git add .
git commit -m "Ready for deployment"
git push origin main

# 3. Go to Render.com
# 4. Connect GitHub
# 5. Deploy!
# 6. Add link to README
```

---

## 💡 Pro Tips

1. **Use Render's free PostgreSQL** for MLflow (better than file storage)
2. **Set up auto-deploy** from main branch
3. **Add monitoring** with UptimeRobot (free)
4. **Document your deployment** in README
5. **Show live demo** in your portfolio

---

## 🎓 For Your Resume/Portfolio

**Add this to your portfolio:**

> "Deployed self-healing MLOps pipeline to production using Render. API serves predictions at [your-url].onrender.com with automatic drift detection and retraining capabilities."

**Technologies to mention:**
- FastAPI (API framework)
- Docker (containerization)
- Render/Railway (cloud deployment)
- MLflow (model tracking)
- GitHub Actions (CI/CD)

---

Good luck with your portfolio deployment! 🚀

