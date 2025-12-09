# 🚀 Deploy Now - Step by Step

Follow these steps to deploy your Auto-Ops app to Render (FREE).

## ✅ Pre-Deployment Checklist

- [x] Model trained
- [x] Dockerfile ready
- [x] render.yaml configured
- [x] All code ready

## 📝 Step-by-Step Deployment

### Step 1: Initialize Git (if not already done)

```bash
cd /Users/abc/Downloads/Auto-Ops

# Check if git is initialized
git status || git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Auto-Ops MLOps Pipeline"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `Auto-Ops` (or your choice)
3. Description: "Self-healing MLOps pipeline with automated drift detection"
4. Choose: Public (for portfolio)
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Add your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/Auto-Ops.git

# Or if you prefer SSH:
# git remote add origin git@github.com:YOUR_USERNAME/Auto-Ops.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Deploy on Render

1. **Go to Render:**
   - Visit: https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (recommended)

2. **Create New Web Service:**
   - Click "New +" button (top right)
   - Select "Web Service"

3. **Connect Repository:**
   - Click "Connect account" if needed
   - Find and select your `Auto-Ops` repository
   - Click "Connect"

4. **Configure Service:**
   - **Name:** `auto-ops-api` (or your choice)
   - **Region:** Choose closest to you (e.g., `Oregon (US West)`)
   - **Branch:** `main`
   - **Root Directory:** `.` (leave empty)
   - **Environment:** `Docker`
   - **Dockerfile Path:** `docker/Dockerfile`
   - **Docker Context:** `.` (leave empty)
   - **Plan:** `Free`

5. **Environment Variables:**
   Click "Advanced" → "Add Environment Variable" and add:
   ```
   MLFLOW_TRACKING_URI = file:./mlflow
   MODEL_SERVING_HOST = 0.0.0.0
   MODEL_SERVING_PORT = 8000
   ```

6. **Deploy:**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Watch the logs (they'll show in Render dashboard)

7. **Get Your URL:**
   - Once deployed, you'll see: `https://auto-ops-api.onrender.com`
   - (Your actual URL will be different based on your service name)

### Step 5: Test Your Deployment

Once deployed, test these URLs:

```bash
# Health check
curl https://your-app-name.onrender.com/health

# API docs
# Open in browser: https://your-app-name.onrender.com/docs
```

### Step 6: Update README with Live Link

Edit your README.md and replace the placeholder URLs with your actual Render URL:

```markdown
## 🌐 Live Demo

**API:** https://your-actual-url.onrender.com  
**Interactive Docs:** https://your-actual-url.onrender.com/docs  
**Health Check:** https://your-actual-url.onrender.com/health
```

Then commit and push:
```bash
git add README.md
git commit -m "Add live deployment link"
git push
```

## 🎯 Quick Commands Summary

```bash
# 1. Initialize and push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/Auto-Ops.git
git push -u origin main

# 2. Then go to render.com and follow steps above
```

## ⚠️ Important Notes

1. **First Request May Be Slow:**
   - Free tier spins down after 15 min inactivity
   - First request takes 30-60 seconds to wake up
   - This is normal for free tier!

2. **Keep It Awake (Optional):**
   - Use UptimeRobot (free): https://uptimerobot.com
   - Set up monitoring to ping your URL every 10 minutes
   - This keeps it awake 24/7

3. **Model Files:**
   - If model files are large, consider using Git LFS
   - Or use MLflow with external storage (S3, etc.)

## 🎉 You're Done!

Once deployed, you'll have:
- ✅ Live API at your Render URL
- ✅ Interactive docs at `/docs`
- ✅ Professional portfolio project
- ✅ GitHub repo with all code
- ✅ Free hosting (no credit card needed)

## 📊 Add to Your Portfolio

**For your resume/portfolio:**

> "Deployed self-healing MLOps pipeline to production using Render. API serves real-time predictions with automatic drift detection. Live demo: [your-url].onrender.com"

**Technologies:**
- FastAPI, Docker, MLflow, Render, GitHub Actions

Good luck! 🚀

