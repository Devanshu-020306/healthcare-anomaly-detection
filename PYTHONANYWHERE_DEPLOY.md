# 🚀 Deploy on PythonAnywhere (Easiest & Free)

## Why PythonAnywhere?
- ✅ **100% FREE** (no credit card needed)
- ✅ **Easiest to deploy** (just upload files)
- ✅ **No trial expiry**
- ✅ **Perfect for demos**
- ✅ **Works forever**

---

## 📱 Step-by-Step Deployment (10 minutes)

### Step 1: Create Account (2 minutes)

1. Go to: **https://www.pythonanywhere.com**
2. Click **"Start running Python online in less than a minute!"**
3. Click **"Create a Beginner account"** (FREE)
4. Sign up with email
5. Verify email

### Step 2: Upload Files (3 minutes)

1. Click **"Files"** tab
2. Click **"Upload a file"**
3. Upload these files from `backend` folder:
   - `app_simple.py`
   - `models.py`
   - `config_simple.py`
   - `ml_models_simple.py`
   - `patient_profiles.py`
   - `notifications.py`
   - `analytics.py`
   - `doctor_notes.py`
   - `report_generator.py`
   - `simple_producer.py`
   - `simple_consumer.py`
   - `requirements_simple.txt`

### Step 3: Install Dependencies (2 minutes)

1. Click **"Consoles"** tab
2. Click **"Bash"**
3. Run these commands:

```bash
pip3 install --user flask flask-cors flask-sqlalchemy scikit-learn numpy pandas
```

### Step 4: Create Web App (2 minutes)

1. Click **"Web"** tab
2. Click **"Add a new web app"**
3. Click **"Next"**
4. Select **"Flask"**
5. Select **"Python 3.10"**
6. Path: `/home/YOUR_USERNAME/app_simple.py`
7. Click **"Next"**

### Step 5: Configure WSGI (1 minute)

1. Click on **"WSGI configuration file"** link
2. Replace content with:

```python
import sys
path = '/home/YOUR_USERNAME'
if path not in sys.path:
    sys.path.append(path)

from app_simple import app as application
```

3. Click **"Save"**

### Step 6: Reload Web App

1. Go back to **"Web"** tab
2. Click **"Reload YOUR_USERNAME.pythonanywhere.com"**
3. Wait 30 seconds

### Step 7: Get Your URL

Your backend is now live at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

Test it:
```
https://YOUR_USERNAME.pythonanywhere.com/api/health
```

---

## ✅ Update Frontend

Update these 3 files with your PythonAnywhere URL:

### File 1: `frontend/js/dashboard.js`
```javascript
const API_BASE = 'https://YOUR_USERNAME.pythonanywhere.com/api';
```

### File 2: `frontend/js/analytics.js`
```javascript
const API_BASE = 'https://YOUR_USERNAME.pythonanywhere.com/api';
```

### File 3: `frontend/emergency.html`
```javascript
const API_BASE = 'https://YOUR_USERNAME.pythonanywhere.com/api';
```

---

## 🔄 Push to GitHub

```bash
git add .
git commit -m "Updated API URLs for PythonAnywhere"
git push
```

Vercel will auto-redeploy!

---

## 🎉 Your Live URLs

- **Frontend:** https://healthcare-anomaly-detection.vercel.app
- **Backend:** https://YOUR_USERNAME.pythonanywhere.com
- **Dashboard:** https://healthcare-anomaly-detection.vercel.app/dashboard.html
- **Analytics:** https://healthcare-anomaly-detection.vercel.app/analytics.html
- **Emergency:** https://healthcare-anomaly-detection.vercel.app/emergency.html

---

## 💡 Important Notes

1. **Free tier limits:**
   - 1 web app
   - 512 MB storage
   - Perfect for demos!

2. **Keep alive:**
   - Free apps sleep after inactivity
   - First request takes 5-10 seconds to wake up
   - After that, works normally

3. **For demo:**
   - Open dashboard 1 minute before showing
   - Let it load completely
   - Then show to teacher!

---

## 🐛 Troubleshooting

### App not loading?
- Check error logs in PythonAnywhere dashboard
- Verify all files uploaded correctly
- Check WSGI configuration

### Import errors?
- Install missing packages in Bash console
- Use: `pip3 install --user PACKAGE_NAME`

### Database errors?
- SQLite works automatically
- No configuration needed

---

## 🎯 Alternative: Use Replit

If PythonAnywhere doesn't work, try **Replit**:

1. Go to: https://replit.com
2. Import from GitHub
3. Click "Run"
4. Done!

---

**Total Time:** 10 minutes
**Cost:** $0 (FREE forever)
**Perfect for:** Demos, projects, portfolios

Good luck! 🚀
