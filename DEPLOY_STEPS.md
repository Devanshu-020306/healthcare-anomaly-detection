# 🚀 Quick Deployment Steps

## Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Healthcare Anomaly Detection System - Ready for deployment"

# Create GitHub repo and push
git remote add origin https://github.com/Devanshu-020306/healthcare-anomaly-detection.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend on Railway (5 minutes)

### Option A: Using Railway Dashboard (Easiest)

1. **Go to:** https://railway.app
2. **Sign up** with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway will auto-detect Python and deploy!
7. **Copy the URL** (e.g., `https://your-app.railway.app`)

### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

### Set Environment Variables (Optional)
In Railway dashboard:
- `PORT` = 5000
- `PYTHON_VERSION` = 3.11.0

## Step 3: Deploy Frontend on Vercel (3 minutes)

### Option A: Using Vercel Dashboard (Easiest)

1. **Go to:** https://vercel.com
2. **Sign up** with GitHub
3. Click **"Add New Project"**
4. Import your GitHub repository
5. **Configure:**
   - Framework Preset: Other
   - Root Directory: `frontend`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
6. Click **"Deploy"**
7. **Copy the URL** (e.g., `https://your-app.vercel.app`)

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy frontend
cd frontend
vercel --prod
```

## Step 4: Update Frontend with Backend URL

After Railway deployment, update these files:

### File: `frontend/js/dashboard.js`
```javascript
// Line 1: Change this
const API_BASE = 'https://YOUR-RAILWAY-URL.railway.app/api';
```

### File: `frontend/js/analytics.js`
```javascript
// Line 1: Change this
const API_BASE = 'https://YOUR-RAILWAY-URL.railway.app/api';
```

### File: `frontend/emergency.html`
```javascript
// Around line 100: Change this
const API_BASE = 'https://YOUR-RAILWAY-URL.railway.app/api';
```

## Step 5: Redeploy Frontend

```bash
# Commit changes
git add .
git commit -m "Update API URLs for production"
git push

# Vercel will auto-deploy!
# Or manually: vercel --prod
```

## ✅ Done! Your URLs:

- **Frontend:** https://your-project.vercel.app
- **Backend API:** https://your-project.railway.app
- **Dashboard:** https://your-project.vercel.app/dashboard.html
- **Analytics:** https://your-project.vercel.app/analytics.html
- **Emergency:** https://your-project.vercel.app/emergency.html

---

## 🐛 Troubleshooting

### Backend not starting?
- Check Railway logs
- Verify `requirements_simple.txt` exists
- Check Python version

### Frontend can't connect to backend?
- Verify API_BASE URLs are correct
- Check CORS is enabled (already done)
- Test backend URL directly: `https://your-app.railway.app/api/health`

### Database not working?
- Railway provides persistent storage automatically
- SQLite will work fine for demo

---

## 🎯 Quick Test

After deployment, test these URLs:

1. **Backend Health:**
   ```
   https://your-app.railway.app/api/health
   ```

2. **Get Patients:**
   ```
   https://your-app.railway.app/api/patients
   ```

3. **Frontend Home:**
   ```
   https://your-project.vercel.app/index.html
   ```

---

## 💡 Pro Tips

1. **Railway gives $5 free credit** - enough for 1 month
2. **Vercel is completely free** for frontend
3. **Auto-deploys** on every git push
4. **Custom domains** available (optional)
5. **HTTPS** enabled by default

---

## 📞 Share with Teacher

Send these links:
- 🏠 Home: https://your-project.vercel.app
- 📊 Dashboard: https://your-project.vercel.app/dashboard.html
- 📈 Analytics: https://your-project.vercel.app/analytics.html
- 🚨 Emergency: https://your-project.vercel.app/emergency.html

---

**Total Time:** 10-15 minutes
**Cost:** $0 (Free tier)
**Difficulty:** Easy 😊

Good luck! 🚀
