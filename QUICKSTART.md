# 🏥 Healthcare Anomaly Detection System - Quick Start

## ✅ System Status: RUNNING

### Backend API
- **Status**: ✓ Running
- **URL**: http://localhost:5000
- **Endpoints**: 
  - `/api/stats` - System statistics
  - `/api/vitals` - Patient vitals
  - `/api/anomalies` - Detected anomalies
  - `/api/patients` - Patient list

### Frontend Dashboard
- **Status**: ✓ Running
- **Home**: http://localhost:8080/index.html
- **Dashboard**: http://localhost:8080/dashboard.html

### Data Processing
- **Producer**: ✓ Generating patient vitals every 5 seconds
- **Consumer**: ✓ Processing data with ML anomaly detection
- **Patients**: 10 patients (P001 - P010)
- **ML Model**: Isolation Forest (trained and active)

## 🎯 What's Happening

1. **Data Generation**: Simulating 10 patients with realistic vital signs
2. **Anomaly Detection**: ML model analyzing each reading in real-time
3. **Severity Classification**: LOW, MEDIUM, HIGH based on anomaly scores
4. **Database Storage**: All readings saved to SQLite database
5. **Dashboard Updates**: Auto-refresh every 10 seconds

## 📊 Access the Dashboard

Open your browser and visit:
**http://localhost:8080/dashboard.html**

You'll see:
- Real-time statistics
- Anomaly charts
- Latest anomaly alerts
- Patient vital signs

## 🛑 To Stop the System

Run in terminal:
```bash
# Stop both processes or press Ctrl+C in their terminals
```

## 📁 Project Files

- `backend/app_simple.py` - Flask API server
- `backend/simple_producer.py` - Data generator
- `backend/simple_consumer.py` - ML processor
- `backend/ml_models_simple.py` - Anomaly detection
- `frontend/dashboard.html` - Main dashboard
- `backend/healthcare.db` - SQLite database

Enjoy monitoring! 🏥
