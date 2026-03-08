"""
Quick script to generate critical patients for emergency dashboard testing
Run this to immediately see patients in emergency dashboard
"""

import requests
import random

API_BASE = 'http://localhost:5000/api'

# Critical vital signs that will trigger HIGH severity
critical_scenarios = [
    {
        'patient_id': 'P001',
        'heart_rate': 165.0,
        'spo2': 85.0,
        'temperature': 39.5,
        'blood_pressure_systolic': 185.0,
        'blood_pressure_diastolic': 115.0
    },
    {
        'patient_id': 'P003',
        'heart_rate': 42.0,
        'spo2': 88.0,
        'temperature': 35.5,
        'blood_pressure_systolic': 175.0,
        'blood_pressure_diastolic': 105.0
    },
    {
        'patient_id': 'P005',
        'heart_rate': 145.0,
        'spo2': 78.0,
        'temperature': 39.8,
        'blood_pressure_systolic': 170.0,
        'blood_pressure_diastolic': 100.0
    },
    {
        'patient_id': 'P008',
        'heart_rate': 135.0,
        'spo2': 90.0,
        'temperature': 38.9,
        'blood_pressure_systolic': 175.0,
        'blood_pressure_diastolic': 110.0
    },
    {
        'patient_id': 'P010',
        'heart_rate': 155.0,
        'spo2': 83.0,
        'temperature': 40.2,
        'blood_pressure_systolic': 180.0,
        'blood_pressure_diastolic': 108.0
    }
]

print("🚨 Generating Critical Patient Scenarios for Emergency Dashboard...")
print("=" * 60)

for scenario in critical_scenarios:
    try:
        response = requests.post(
            f'{API_BASE}/vitals/manual',
            json=scenario,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ {scenario['patient_id']}: {result['severity']} - Score: {result['anomaly_score']:.3f}")
        else:
            print(f"❌ {scenario['patient_id']}: Error - {response.text}")
    except Exception as e:
        print(f"❌ {scenario['patient_id']}: {str(e)}")

print("=" * 60)
print("🎯 Critical patients generated!")
print("📱 Open Emergency Dashboard: http://localhost:8080/emergency.html")
print("🔊 Enable sound alerts for full experience!")
