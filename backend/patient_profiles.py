import random

# Realistic patient profiles
PATIENT_PROFILES = {
    'P001': {
        'name': 'Rajesh Kumar',
        'age': 45,
        'gender': 'Male',
        'conditions': ['Hypertension', 'Type 2 Diabetes'],
        'medications': ['Metformin', 'Lisinopril'],
        'risk_level': 'HIGH',
        'normal_ranges': {
            'heart_rate': (65, 85),
            'spo2': (94, 98),
            'temperature': (36.5, 37.3),
            'bp_systolic': (130, 145),
            'bp_diastolic': (80, 90)
        }
    },
    'P002': {
        'name': 'Priya Sharma',
        'age': 32,
        'gender': 'Female',
        'conditions': ['Asthma'],
        'medications': ['Albuterol'],
        'risk_level': 'MEDIUM',
        'normal_ranges': {
            'heart_rate': (70, 90),
            'spo2': (95, 99),
            'temperature': (36.4, 37.2),
            'bp_systolic': (110, 130),
            'bp_diastolic': (70, 85)
        }
    },
    'P003': {
        'name': 'Amit Patel',
        'age': 58,
        'gender': 'Male',
        'conditions': ['Coronary Artery Disease', 'High Cholesterol'],
        'medications': ['Aspirin', 'Atorvastatin', 'Beta-blocker'],
        'risk_level': 'HIGH',
        'normal_ranges': {
            'heart_rate': (60, 75),
            'spo2': (94, 98),
            'temperature': (36.5, 37.2),
            'bp_systolic': (120, 140),
            'bp_diastolic': (75, 88)
        }
    },
    'P004': {
        'name': 'Sneha Reddy',
        'age': 28,
        'gender': 'Female',
        'conditions': ['Healthy'],
        'medications': [],
        'risk_level': 'LOW',
        'normal_ranges': {
            'heart_rate': (65, 85),
            'spo2': (96, 100),
            'temperature': (36.4, 37.1),
            'bp_systolic': (105, 125),
            'bp_diastolic': (65, 80)
        }
    },
    'P005': {
        'name': 'Vikram Singh',
        'age': 67,
        'gender': 'Male',
        'conditions': ['COPD', 'Hypertension'],
        'medications': ['Tiotropium', 'Amlodipine'],
        'risk_level': 'HIGH',
        'normal_ranges': {
            'heart_rate': (70, 90),
            'spo2': (88, 94),
            'temperature': (36.5, 37.4),
            'bp_systolic': (135, 150),
            'bp_diastolic': (80, 92)
        }
    },
    'P006': {
        'name': 'Anita Desai',
        'age': 41,
        'gender': 'Female',
        'conditions': ['Thyroid Disorder'],
        'medications': ['Levothyroxine'],
        'risk_level': 'MEDIUM',
        'normal_ranges': {
            'heart_rate': (68, 88),
            'spo2': (95, 99),
            'temperature': (36.3, 37.2),
            'bp_systolic': (110, 130),
            'bp_diastolic': (70, 85)
        }
    },
    'P007': {
        'name': 'Suresh Iyer',
        'age': 52,
        'gender': 'Male',
        'conditions': ['Sleep Apnea', 'Obesity'],
        'medications': ['CPAP therapy'],
        'risk_level': 'MEDIUM',
        'normal_ranges': {
            'heart_rate': (72, 92),
            'spo2': (90, 96),
            'temperature': (36.5, 37.3),
            'bp_systolic': (125, 145),
            'bp_diastolic': (78, 90)
        }
    },
    'P008': {
        'name': 'Meera Joshi',
        'age': 35,
        'gender': 'Female',
        'conditions': ['Pregnancy - 3rd Trimester'],
        'medications': ['Prenatal vitamins'],
        'risk_level': 'MEDIUM',
        'normal_ranges': {
            'heart_rate': (80, 100),
            'spo2': (95, 99),
            'temperature': (36.5, 37.4),
            'bp_systolic': (110, 135),
            'bp_diastolic': (70, 85)
        }
    },
    'P009': {
        'name': 'Karan Malhotra',
        'age': 24,
        'gender': 'Male',
        'conditions': ['Post-Surgery Recovery'],
        'medications': ['Antibiotics', 'Pain management'],
        'risk_level': 'MEDIUM',
        'normal_ranges': {
            'heart_rate': (70, 95),
            'spo2': (94, 99),
            'temperature': (36.8, 37.8),
            'bp_systolic': (110, 130),
            'bp_diastolic': (70, 85)
        }
    },
    'P010': {
        'name': 'Lakshmi Nair',
        'age': 72,
        'gender': 'Female',
        'conditions': ['Atrial Fibrillation', 'Osteoporosis'],
        'medications': ['Warfarin', 'Calcium supplements'],
        'risk_level': 'HIGH',
        'normal_ranges': {
            'heart_rate': (60, 100),
            'spo2': (92, 97),
            'temperature': (36.4, 37.2),
            'bp_systolic': (130, 150),
            'bp_diastolic': (75, 90)
        }
    }
}

def get_patient_info(patient_id):
    return PATIENT_PROFILES.get(patient_id, {
        'name': 'Unknown Patient',
        'age': 0,
        'gender': 'Unknown',
        'conditions': [],
        'medications': [],
        'risk_level': 'UNKNOWN',
        'normal_ranges': {
            'heart_rate': (60, 100),
            'spo2': (95, 100),
            'temperature': (36.5, 37.5),
            'bp_systolic': (110, 140),
            'bp_diastolic': (70, 90)
        }
    })

def generate_realistic_vitals(patient_id):
    """Generate vitals based on patient's medical profile"""
    profile = get_patient_info(patient_id)
    ranges = profile['normal_ranges']
    
    # 85% chance of normal vitals, 15% chance of anomaly
    is_anomaly = random.random() < 0.15
    
    if is_anomaly:
        # Generate anomalous vitals based on patient's conditions
        if 'Hypertension' in profile['conditions']:
            heart_rate = random.uniform(ranges['heart_rate'][0] - 10, ranges['heart_rate'][1] + 30)
            bp_systolic = random.uniform(ranges['bp_systolic'][1] + 10, 180)
            bp_diastolic = random.uniform(ranges['bp_diastolic'][1] + 5, 110)
        elif 'COPD' in profile['conditions'] or 'Asthma' in profile['conditions']:
            heart_rate = random.uniform(ranges['heart_rate'][1], ranges['heart_rate'][1] + 40)
            spo2 = random.uniform(ranges['spo2'][0] - 8, ranges['spo2'][0])
        elif 'Coronary Artery Disease' in profile['conditions']:
            heart_rate = random.choice([
                random.uniform(40, ranges['heart_rate'][0] - 5),
                random.uniform(ranges['heart_rate'][1] + 20, 140)
            ])
        else:
            # Generic anomaly
            heart_rate = random.choice([
                random.uniform(40, 55),
                random.uniform(110, 160)
            ])
        
        # Set other vitals
        if 'heart_rate' not in locals():
            heart_rate = random.uniform(ranges['heart_rate'][0], ranges['heart_rate'][1])
        if 'spo2' not in locals():
            spo2 = random.uniform(ranges['spo2'][0] - 5, ranges['spo2'][0])
        if 'bp_systolic' not in locals():
            bp_systolic = random.choice([
                random.uniform(85, 95),
                random.uniform(ranges['bp_systolic'][1] + 10, 180)
            ])
        if 'bp_diastolic' not in locals():
            bp_diastolic = random.choice([
                random.uniform(45, 60),
                random.uniform(ranges['bp_diastolic'][1] + 5, 105)
            ])
        
        temperature = random.choice([
            random.uniform(35.5, 36.2),
            random.uniform(37.8, 39.5)
        ])
    else:
        # Normal vitals within patient's range
        heart_rate = random.uniform(ranges['heart_rate'][0], ranges['heart_rate'][1])
        spo2 = random.uniform(ranges['spo2'][0], ranges['spo2'][1])
        temperature = random.uniform(ranges['temperature'][0], ranges['temperature'][1])
        bp_systolic = random.uniform(ranges['bp_systolic'][0], ranges['bp_systolic'][1])
        bp_diastolic = random.uniform(ranges['bp_diastolic'][0], ranges['bp_diastolic'][1])
    
    return {
        'patient_id': patient_id,
        'heart_rate': round(heart_rate, 1),
        'spo2': round(spo2, 1),
        'temperature': round(temperature, 1),
        'blood_pressure_systolic': round(bp_systolic, 1),
        'blood_pressure_diastolic': round(bp_diastolic, 1)
    }

def get_clinical_recommendation(patient_id, vitals, severity):
    """Generate clinical recommendations based on patient profile and vitals"""
    profile = get_patient_info(patient_id)
    recommendations = []
    
    if vitals['heart_rate'] > 120:
        recommendations.append("⚠️ Tachycardia detected - Check for cardiac issues")
        if 'Coronary Artery Disease' in profile['conditions']:
            recommendations.append("🔴 HIGH RISK: Patient has CAD history - Immediate ECG recommended")
    elif vitals['heart_rate'] < 50:
        recommendations.append("⚠️ Bradycardia detected - Monitor closely")
    
    if vitals['spo2'] < 90:
        recommendations.append("🔴 CRITICAL: Severe hypoxemia - Oxygen therapy required")
        if 'COPD' in profile['conditions']:
            recommendations.append("Patient has COPD - Check for exacerbation")
    elif vitals['spo2'] < 94:
        recommendations.append("⚠️ Low oxygen saturation - Supplemental oxygen may be needed")
    
    if vitals['temperature'] > 38.5:
        recommendations.append("🔴 Fever detected - Check for infection")
        if 'Post-Surgery Recovery' in profile['conditions']:
            recommendations.append("Post-op patient - Rule out surgical site infection")
    elif vitals['temperature'] < 36:
        recommendations.append("⚠️ Hypothermia - Warm patient, check for sepsis")
    
    if vitals['blood_pressure_systolic'] > 160:
        recommendations.append("🔴 Hypertensive crisis - Consider antihypertensive medication")
        if 'Hypertension' in profile['conditions']:
            recommendations.append("Known hypertensive - Check medication compliance")
    elif vitals['blood_pressure_systolic'] < 90:
        recommendations.append("⚠️ Hypotension - Check for shock, dehydration")
    
    if not recommendations:
        recommendations.append("✅ Vitals within acceptable range for patient profile")
    
    return recommendations
