import time
import random
from config_simple import Config
from patient_profiles import generate_realistic_vitals
import threading

def start_producer():
    patient_ids = [f'P{str(i).zfill(3)}' for i in range(1, 11)]
    
    print("Starting realistic patient data producer...")
    cycle_count = 0
    
    while True:
        cycle_count += 1
        
        for patient_id in patient_ids:
            # Every 3rd cycle, increase chance of critical anomalies for emergency demo
            if cycle_count % 3 == 0:
                # Force some critical cases for emergency dashboard
                if random.random() < 0.3:  # 30% chance of critical
                    vitals = generate_critical_vitals(patient_id)
                else:
                    vitals = generate_realistic_vitals(patient_id)
            else:
                vitals = generate_realistic_vitals(patient_id)
            
            vitals['timestamp'] = time.time()
            Config.VITALS_QUEUE.put(vitals)
            print(f"Generated: {patient_id}")
        time.sleep(5)

def generate_critical_vitals(patient_id):
    """Generate critical vitals for emergency scenarios"""
    from patient_profiles import get_patient_info
    
    profile = get_patient_info(patient_id)
    
    # Generate severe anomalies based on conditions
    if 'Hypertension' in profile['conditions'] or 'Coronary Artery Disease' in profile['conditions']:
        # Cardiac emergency
        return {
            'patient_id': patient_id,
            'heart_rate': round(random.choice([random.uniform(35, 45), random.uniform(140, 180)]), 1),
            'spo2': round(random.uniform(82, 91), 1),
            'temperature': round(random.uniform(38.5, 40), 1),
            'blood_pressure_systolic': round(random.uniform(170, 200), 1),
            'blood_pressure_diastolic': round(random.uniform(100, 120), 1)
        }
    elif 'COPD' in profile['conditions'] or 'Asthma' in profile['conditions']:
        # Respiratory emergency
        return {
            'patient_id': patient_id,
            'heart_rate': round(random.uniform(110, 150), 1),
            'spo2': round(random.uniform(75, 88), 1),
            'temperature': round(random.uniform(37.5, 39.5), 1),
            'blood_pressure_systolic': round(random.uniform(140, 170), 1),
            'blood_pressure_diastolic': round(random.uniform(85, 105), 1)
        }
    elif 'Pregnancy' in str(profile['conditions']):
        # Pre-eclampsia scenario
        return {
            'patient_id': patient_id,
            'heart_rate': round(random.uniform(110, 140), 1),
            'spo2': round(random.uniform(90, 94), 1),
            'temperature': round(random.uniform(37.8, 39), 1),
            'blood_pressure_systolic': round(random.uniform(160, 180), 1),
            'blood_pressure_diastolic': round(random.uniform(100, 115), 1)
        }
    else:
        # General critical condition
        return {
            'patient_id': patient_id,
            'heart_rate': round(random.choice([random.uniform(40, 50), random.uniform(130, 170)]), 1),
            'spo2': round(random.uniform(80, 90), 1),
            'temperature': round(random.choice([random.uniform(35, 36), random.uniform(39, 40.5)]), 1),
            'blood_pressure_systolic': round(random.choice([random.uniform(80, 95), random.uniform(165, 190)]), 1),
            'blood_pressure_diastolic': round(random.choice([random.uniform(45, 60), random.uniform(100, 120)]), 1)
        }

def run_producer_thread():
    thread = threading.Thread(target=start_producer, daemon=True)
    thread.start()
    return thread
