# 🚀 Deploy to Streamlit Cloud - Super Easy!

Deploying your Auto-Ops app to Streamlit Cloud is the easiest way to get it live!

## ✅ Prerequisites

- ✅ Code pushed to GitHub
- ✅ `streamlit_app.py` in root directory
- ✅ `requirements.txt` with dependencies

## 📝 Step-by-Step (2 Minutes!)

### Step 1: Go to Streamlit Cloud

1. Visit: **https://streamlit.io/cloud**
2. Click **"Sign up"** (top right)
3. Choose **"Sign up with GitHub"**
4. Authorize Streamlit to access your GitHub

### Step 2: Create New App

1. Once logged in, click **"New app"** button
2. Fill in the form:
   - **Repository**: Select `jaswanth-tiruvee/Auto-Ops`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: `auto-ops` (or your choice)
3. Click **"Deploy"**

### Step 3: Wait for Deployment

- Streamlit will automatically:
  - Install dependencies from `requirements.txt`
  - Build your app
  - Deploy it
- Takes about **2-3 minutes**

### Step 4: Your App is Live! 🎉

Your app will be available at:
```
https://auto-ops.streamlit.app
```

(Or whatever URL you chose)

## 🎯 That's It!

No Docker, no configuration files, no complex setup. Just:
1. Push to GitHub ✅
2. Connect to Streamlit Cloud ✅
3. Deploy ✅

## 🔄 Auto-Deploy

Streamlit Cloud automatically redeploys when you push to GitHub!

## 📊 Features

- ✅ **Free forever**
- ✅ **Auto-deploys on git push**
- ✅ **Custom URLs**
- ✅ **No credit card needed**
- ✅ **Fast and reliable**

## 🛠️ Troubleshooting

### App won't start?

1. Check **Logs** in Streamlit Cloud dashboard
2. Verify `requirements.txt` has all dependencies
3. Ensure `streamlit_app.py` is in root directory

### Model not found?

- Train model locally first: `python src/train.py --month 2023-01`
- Commit model files to GitHub (if small)
- Or use MLflow with external storage

### Dependencies error?

- Check `requirements.txt` syntax
- Ensure all packages are available on PyPI
- Check Streamlit Cloud logs for specific errors

## 🎉 Success!

Once deployed, you'll have:
- ✅ Live app at your Streamlit Cloud URL
- ✅ Auto-updates on every git push
- ✅ Professional portfolio project
- ✅ Shareable link for your resume

**That's it! Super easy! 🚀**

