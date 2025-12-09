# 🚀 Deploy to Render - Step by Step Guide

Follow these steps to deploy your Auto-Ops app to Render (FREE hosting).

## ✅ Prerequisites

- ✅ Code pushed to GitHub: https://github.com/jaswanth-tiruvee/Auto-Ops
- ✅ `render.yaml` configured
- ✅ `Dockerfile` ready
- ✅ Model trained (optional, can train on Render)

## 📝 Step-by-Step Deployment

### Step 1: Sign Up for Render

1. Go to **https://render.com**
2. Click **"Get Started for Free"** (top right)
3. Choose **"Sign up with GitHub"** (recommended)
4. Authorize Render to access your GitHub account

### Step 2: Create New Web Service

1. Once logged in, click the **"New +"** button (top right)
2. Select **"Web Service"** from the dropdown

### Step 3: Connect Your Repository

1. In the "Connect a repository" section:
   - If you see your GitHub repos, find **"jaswanth-tiruvee/Auto-Ops"** and click **"Connect"**
   - If not, click **"Configure account"** and grant access
2. After connecting, select **"jaswanth-tiruvee/Auto-Ops"**

### Step 4: Configure the Service

Render will auto-detect `render.yaml`, but verify these settings:

**Basic Settings:**
- **Name:** `auto-ops-api` (or your choice)
- **Region:** Choose closest to you (e.g., `Oregon (US West)`)
- **Branch:** `main`
- **Root Directory:** Leave empty (`.`)
- **Runtime:** `Docker`
- **Dockerfile Path:** `docker/Dockerfile` (should auto-detect)
- **Docker Context:** Leave empty (`.`)
- **Plan:** `Free`

**Advanced Settings (Click "Advanced"):**

Add Environment Variables:
```
MLFLOW_TRACKING_URI = file:./mlflow
MODEL_SERVING_HOST = 0.0.0.0
MODEL_SERVING_PORT = 8000
```

**Note:** The `render.yaml` file should handle most of this automatically!

### Step 5: Deploy

1. Click **"Create Web Service"** (bottom of page)
2. Render will start building your Docker image
3. Watch the build logs (they'll appear automatically)
4. Build time: **5-10 minutes** (first time)

### Step 6: Get Your Live URL

Once deployment completes:
- Your app will be live at: `https://auto-ops-api.onrender.com`
- (Your actual URL will be: `https://[your-service-name].onrender.com`)

## 🧪 Test Your Deployment

After deployment, test these URLs:

```bash
# Health check
https://your-app-name.onrender.com/health

# API documentation (interactive)
https://your-app-name.onrender.com/docs

# Root endpoint
https://your-app-name.onrender.com/
```

## ⚠️ Important Notes

### Free Tier Limitations:

1. **Spins Down After 15 Minutes:**
   - Free tier services sleep after 15 min of inactivity
   - First request after sleep takes **30-60 seconds** to wake up
   - This is normal for free tier!

2. **Keep It Awake (Optional):**
   - Use **UptimeRobot** (free): https://uptimerobot.com
   - Set up monitoring to ping your URL every 10 minutes
   - This keeps your service awake 24/7

3. **Resource Limits:**
   - 512 MB RAM
   - 750 hours/month (enough for 24/7 if kept awake)
   - Perfect for portfolio projects!

### Model Training:

If your model isn't in the repo, Render will need to train it:
- This happens during the first build
- May take longer on first deployment
- Consider training locally and committing model files

## 🔧 Troubleshooting

### Build Fails:

1. **Check build logs** in Render dashboard
2. **Common issues:**
   - Dockerfile path incorrect → Should be `docker/Dockerfile`
   - Missing dependencies → Check `requirements.txt`
   - Port mismatch → Ensure app listens on `0.0.0.0:8000`

### App Won't Start:

1. Check **Runtime logs** in Render dashboard
2. Verify environment variables are set
3. Ensure model files exist (if needed)

### Slow First Request:

- Normal for free tier (waking from sleep)
- Use UptimeRobot to keep it awake

## 📊 After Deployment

### Update Your README:

Edit `README.md` and replace placeholder URLs:

```markdown
## 🌐 Live Demo

**API:** https://your-actual-url.onrender.com  
**Interactive Docs:** https://your-actual-url.onrender.com/docs  
**Health Check:** https://your-actual-url.onrender.com/health
```

Then commit and push:
```bash
git add README.md
git commit -m "Update README with live deployment URL"
git push
```

### Add to Portfolio:

- Include live demo link
- Mention in resume: "Deployed to production on Render"
- Show the interactive API docs

## 🎉 Success!

Once deployed, you'll have:
- ✅ Live API at your Render URL
- ✅ Interactive documentation
- ✅ Free hosting (no credit card needed)
- ✅ Professional portfolio project

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Check build/runtime logs in Render dashboard

Good luck with your deployment! 🚀

