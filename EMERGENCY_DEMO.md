# 🚨 Emergency Dashboard Demo Guide

## Quick Start

### Method 1: Wait for Auto-Generation (Realistic)
System automatically generates critical cases every 3rd cycle (15 seconds).
Just wait and refresh the emergency dashboard.

### Method 2: Instant Demo (For Presentation)
Run this command to immediately create 5 critical patients:

```bash
cd backend
python test_emergency.py
```

This will create:
- **P001 (Rajesh Kumar)** - Cardiac emergency (HR: 165, BP: 185/115)
- **P003 (Amit Patel)** - Bradycardia + Hypertension (HR: 42, BP: 175/105)
- **P005 (Vikram Singh)** - Respiratory crisis (SpO2: 78%, HR: 145)
- **P008 (Meera Joshi)** - Pre-eclampsia (BP: 175/110, HR: 135)
- **P010 (Lakshmi Nair)** - Critical hypoxemia (SpO2: 83%, HR: 155)

## Emergency Dashboard Features

### 🔊 Audio Alerts
1. Click "🔊 Sound ON" button
2. Alert sound plays continuously when critical patients present
3. Click "🔇 Sound OFF" to mute

### 📊 Real-Time Updates
- Auto-refreshes every 5 seconds
- Shows latest critical alerts
- Alert count per patient
- Latest vitals display

### 🎨 Visual Features
- Pulsing red header (emergency mode)
- Dark theme for focus
- Slide-in animations
- Color-coded severity

## Demo Script for Teacher

### Step 1: Show Empty State
"Initially, when all patients are stable, the dashboard shows a green message."

### Step 2: Generate Critical Cases
```bash
python backend/test_emergency.py
```
"Now I'll simulate 5 critical emergency scenarios..."

### Step 3: Show Emergency Dashboard
"Within seconds, the system detects these critical conditions and displays them here."

### Step 4: Enable Audio
"In a real hospital, audio alerts would notify staff immediately."
*Click Sound ON button*

### Step 5: Explain Each Patient
Point to each critical patient card:
- "Rajesh Kumar has severe tachycardia and hypertensive crisis"
- "Vikram Singh is experiencing respiratory failure with SpO2 at 78%"
- "Meera Joshi shows signs of pre-eclampsia - critical for pregnancy"

### Step 6: Show Auto-Refresh
"The system updates every 5 seconds automatically, ensuring no critical case is missed."

### Step 7: Explain Real-World Use
"In a real ICU, this dashboard would be displayed on a large monitor, with audio alerts ensuring immediate response to critical patients."

## Technical Details

### Critical Thresholds (HIGH Severity):
- Heart Rate: <45 or >130 BPM
- SpO2: <90%
- Temperature: <36°C or >39°C
- BP Systolic: <90 or >165 mmHg
- BP Diastolic: <50 or >100 mmHg

### System Response:
1. ML model detects anomaly (score >0.6)
2. Classified as HIGH severity
3. Stored in database
4. Appears in emergency dashboard within 5 seconds
5. Audio alert triggers (if enabled)
6. Notification created with recommendations

## Tips for Impressive Demo

1. **Start with empty dashboard** - Shows system intelligence
2. **Run test script** - Instant critical cases
3. **Enable audio** - Full hospital experience
4. **Explain patient context** - Show medical knowledge
5. **Highlight auto-refresh** - Real-time capability
6. **Show recommendations** - Clinical decision support

## Troubleshooting

### No patients showing?
- Wait 15 seconds for auto-generation, OR
- Run: `python backend/test_emergency.py`

### Audio not working?
- Click "Sound ON" button
- Check browser audio permissions
- Refresh page and try again

### Dashboard not updating?
- Check backend is running
- Refresh browser (F5)
- Check console for errors

## Production Deployment Notes

In a real hospital deployment:
- Audio alerts would be louder/different tones
- Multiple monitors in different locations
- SMS/Email alerts to doctors
- Integration with nurse call systems
- Escalation protocols
- Automatic documentation

---

**Emergency Dashboard URL:** http://localhost:8080/emergency.html

**Test Script:** `python backend/test_emergency.py`

**Auto-Generation:** Every 15 seconds (30% chance per cycle)

---

🚨 Perfect for demonstrating real-world healthcare monitoring! 🏥
