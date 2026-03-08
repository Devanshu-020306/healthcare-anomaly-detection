# 🚀 Deployment Guide - Healthcare Anomaly Detection System

## ⚠️ Important Note

This system has **two components** that need different deployment strategies:

1. **Frontend** (HTML/CSS/JS) - Can deploy on Vercel
2. **Backend** (Python Flask + ML + Database) - Needs a server platform

---

## 🎯 Recommended Deployment Strategy

### **Option 1: Split Deployment (Best for Free Hosting)**

#### **Frontend → Vercel** (Static hosting)
#### **Backend → Railway/Render** (Python hosting)

---

## 📱 Frontend Deployment on Vercel

### Step 1: Prepare Frontend for Deployment

Create a `public` folder structure:

```bash
mkdir public
cp -r frontend/* public/
```

### Step 2: Update API URLs

Update all JavaScript files to use your backend URL:

```javascript
// In dashboard.js, analytics.js
const API_BASE = 'https://your-backend-url.railway.app/api';
```

### Step 3: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

**OR** use Vercel Dashboard:
1. Go to https://vercel.com
2. Import Git repository
3. Set root directory to `frontend`
4. Deploy

---

## 🖥️ Backend Deployment Options

### **Option A: Railway (Recommended - Easy)**

#### Step 1: Create `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python backend/app_simple.py",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

#### Step 2: Create `Procfile`
```
web: python backend/app_simple.py
```

#### Step 3: Update `requirements.txt`
```bash
cd backend
pip freeze > requirements.txt
```

#### Step 4: Deploy
1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your repository
5. Add environment variables:
   - `PORT=5000`
   - `DATABASE_URL=sqlite:///healthcare.db`
6. Deploy!

**Railway gives you a URL like:** `https://your-app.railway.app`

---

### **Option B: Render (Alternative)**

#### Step 1: Create `render.yaml`
```yaml
services:
  - type: web
    name: healthcare-backend
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "python backend/app_simple.py"
    envVars:
      - key: PORT
        value: 5000
```

#### Step 2: Deploy
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repository
4. Select Python environment
5. Build command: `pip install -r backend/requirements.txt`
6. Start command: `python backend/app_simple.py`
7. Deploy!

---

### **Option C: PythonAnywhere (Easiest for Beginners)**

1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Upload your backend files
4. Set up Flask app in Web tab
5. Configure WSGI file
6. Reload web app

---

## 🔧 Configuration Changes Needed

### 1. Update CORS Settings

In `backend/app_simple.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-frontend.vercel.app",
            "http://localhost:8080"
        ],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})
```

### 2. Update Frontend API URLs

Create `frontend/js/config.js`:

```javascript
const CONFIG = {
    API_BASE: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000/api'
        : 'https://your-backend.railway.app/api'
};
```

Then update all files:
```javascript
// Instead of: const API_BASE = 'http://localhost:5000/api';
// Use: const API_BASE = CONFIG.API_BASE;
```

### 3. Database Configuration

For production, use PostgreSQL instead of SQLite:

```python
# In config_simple.py
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'sqlite:///healthcare.db'  # fallback for local
)
```

Railway/Render provide PostgreSQL for free!

---

## 📦 Complete Deployment Steps

### **Quick Deploy (5 minutes)**

#### 1. Frontend on Vercel:
```bash
cd frontend
vercel --prod
```

#### 2. Backend on Railway:
```bash
# Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# Then on Railway dashboard:
# - New Project
# - Deploy from GitHub
# - Select repo
# - Done!
```

#### 3. Update Frontend with Backend URL:
```javascript
// In all JS files
const API_BASE = 'https://your-app.railway.app/api';
```

#### 4. Redeploy Frontend:
```bash
vercel --prod
```

---

## 🎯 Simpler Alternative: All-in-One Deployment

### **Deploy Everything on Render**

Create `render.yaml`:

```yaml
services:
  # Backend API
  - type: web
    name: healthcare-api
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "python backend/app_simple.py"
    
  # Frontend Static Site
  - type: web
    name: healthcare-frontend
    env: static
    buildCommand: "echo 'No build needed'"
    staticPublishPath: ./frontend
```

Then:
1. Push to GitHub
2. Connect to Render
3. Deploy!

Both frontend and backend will be on Render.

---

## 🆓 Free Hosting Comparison

| Platform | Frontend | Backend | Database | Limits |
|----------|----------|---------|----------|--------|
| **Vercel** | ✅ Free | ❌ No | ❌ No | 100GB bandwidth |
| **Railway** | ✅ Free | ✅ Free | ✅ Free | $5 credit/month |
| **Render** | ✅ Free | ✅ Free | ✅ Free | 750 hours/month |
| **PythonAnywhere** | ❌ No | ✅ Free | ✅ Free | Limited CPU |
| **Netlify** | ✅ Free | ❌ No | ❌ No | 100GB bandwidth |

---

## 🔒 Environment Variables

Set these on your hosting platform:

```bash
PORT=5000
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

---

## 📝 Post-Deployment Checklist

- [ ] Backend is running and accessible
- [ ] Frontend can connect to backend
- [ ] CORS is configured correctly
- [ ] Database is working
- [ ] ML models are loaded
- [ ] Notifications are working
- [ ] All API endpoints respond
- [ ] Dark mode persists
- [ ] CSV export works
- [ ] Reports generate correctly

---

## 🐛 Common Issues & Solutions

### Issue: CORS Error
**Solution:** Add frontend URL to CORS origins in backend

### Issue: Database not persisting
**Solution:** Use PostgreSQL instead of SQLite

### Issue: ML models not loading
**Solution:** Ensure scikit-learn version matches in requirements.txt

### Issue: 502 Bad Gateway
**Solution:** Check backend logs, ensure PORT is set correctly

---

## 🎓 Recommended for Your Project

**Best Free Option:**

1. **Frontend:** Vercel (https://vercel.com)
2. **Backend:** Railway (https://railway.app)
3. **Database:** Railway PostgreSQL (included)

**Total Cost:** $0 (Free tier)

**Deployment Time:** 10-15 minutes

---

## 📞 Quick Deploy Commands

```bash
# 1. Deploy Frontend to Vercel
cd frontend
vercel --prod

# 2. Deploy Backend to Railway
# (Use Railway dashboard - easier)
# Or use Railway CLI:
railway login
railway init
railway up

# 3. Update frontend config with backend URL
# Edit frontend/js/dashboard.js, analytics.js
# Replace API_BASE with your Railway URL

# 4. Redeploy frontend
vercel --prod
```

---

## 🎉 Your Live URLs

After deployment:
- **Frontend:** https://your-project.vercel.app
- **Backend:** https://your-project.railway.app
- **API:** https://your-project.railway.app/api

Share these URLs with your teacher! 🚀

---

## 💡 Pro Tips

1. **Use Environment Variables** - Never hardcode URLs
2. **Enable HTTPS** - Both platforms provide free SSL
3. **Monitor Logs** - Check Railway/Render logs for errors
4. **Test Locally First** - Ensure everything works before deploying
5. **Use Git** - Deploy from GitHub for easy updates

---

## 🆘 Need Help?

If deployment fails:
1. Check platform logs
2. Verify requirements.txt
3. Test API endpoints manually
4. Check CORS configuration
5. Ensure database connection

---

**Note:** For a college project demo, you can also just run locally and share your screen. Deployment is optional but impressive! 🎓
