# 🚀 Deploy Backend on Render (FREE Forever)

## Why Render?
- ✅ Completely FREE (no trial, no credit card)
- ✅ 750 hours/month free
- ✅ Auto-deploy from GitHub
- ✅ Better than Railway for free tier

---

## Step-by-Step Deployment

### Step 1: Go to Render (2 minutes)

1. **Visit:** https://render.com
2. **Sign up** with GitHub (free account)
3. Click **"New +"** → **"Web Service"**

### Step 2: Connect Repository (1 minute)

1. Click **"Connect a repository"**
2. Select: `Devanshu-020306/healthcare-anomaly-detection`
3. Click **"Connect"**

### Step 3: Configure Service (2 minutes)

Fill in these details:

**Name:** `healthcare-backend`

**Region:** `Oregon (US West)` (or closest to you)

**Branch:** `main`

**Root Directory:** (leave empty)

**Runtime:** `Python 3`

**Build Command:**
```bash
pip install -r backend/requirements_simple.txt
```

**Start Command:**
```bash
python backend/app_simple.py
```

**Instance Type:** `Free`

### Step 4: Environment Variables (Optional)

Click **"Advanced"** → **"Add Environment Variable"**

Add these:
- `PORT` = `5000`
- `PYTHON_VERSION` = `3.11.0`

### Step 5: Deploy! (3-5 minutes)

1. Click **"Create Web Service"**
2. Wait for deployment (3-5 minutes)
3. **Copy your URL:** `https://healthcare-backend.onrender.com`

---

## ✅ Your Backend is LIVE!

Test it:
```
https://healthcare-backend.onrender.com/api/health
```

---

## Update Frontend with Render URL

Update these 3 files:

### File 1: `frontend/js/dashboard.js`
```javascript
const API_BASE = 'https://healthcare-backend.onrender.com/api';
```

### File 2: `frontend/js/analytics.js`
```javascript
const API_BASE = 'https://healthcare-backend.onrender.com/api';
```

### File 3: `frontend/emergency.html`
```javascript
const API_BASE = 'https://healthcare-backend.onrender.com/api';
```

---

## Push Changes

```bash
git add .
git commit -m "Updated API URLs for Render backend"
git push
```

Vercel will auto-redeploy! ✅

---

## 🎉 Done!

Your URLs:
- **Frontend:** https://healthcare-anomaly-detection.vercel.app
- **Backend:** https://healthcare-backend.onrender.com
- **Dashboard:** https://healthcare-anomaly-detection.vercel.app/dashboard.html

---

## ⚠️ Important Note

Render free tier:
- Spins down after 15 minutes of inactivity
- Takes 30-60 seconds to wake up on first request
- Perfect for demos and projects!

---

## 💡 Pro Tip

Keep backend awake by:
1. Opening dashboard before demo
2. Wait 1 minute for backend to wake up
3. Then show to teacher!

---

**Total Time:** 10 minutes
**Cost:** $0 (FREE forever)
**Perfect for:** College projects, demos, portfolios

Good luck! 🚀
