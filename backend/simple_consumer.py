import threading
import numpy as np
from config_simple import Config
from models import db, PatientVital
from ml_models_simple import AnomalyDetector
from notifications import notification_system

detector = AnomalyDetector()

def initialize_detector():
    global detector
    if not detector.load_models():
        print("Training new models...")
        training_data = np.random.randn(1000, 5) * 10 + [75, 97, 37, 120, 80]
        detector.train_models(training_data)
        detector.save_models()
        print("Models trained and saved!")

def start_consumer(app):
    print("Starting data consumer...")
    
    with app.app_context():
        while True:
            try:
                vitals_data = Config.VITALS_QUEUE.get(timeout=1)
                
                vitals_array = [
                    vitals_data['heart_rate'],
                    vitals_data['spo2'],
                    vitals_data['temperature'],
                    vitals_data['blood_pressure_systolic'],
                    vitals_data['blood_pressure_diastolic']
                ]
                
                anomaly_score, severity = detector.predict(vitals_array)
                is_anomaly = anomaly_score > Config.ANOMALY_THRESHOLDS['LOW']
                
                vital = PatientVital(
                    patient_id=vitals_data['patient_id'],
                    heart_rate=vitals_data['heart_rate'],
                    spo2=vitals_data['spo2'],
                    temperature=vitals_data['temperature'],
                    blood_pressure_systolic=vitals_data['blood_pressure_systolic'],
                    blood_pressure_diastolic=vitals_data['blood_pressure_diastolic'],
                    anomaly_score=anomaly_score,
                    severity=severity,
                    is_anomaly=is_anomaly
                )
                
                db.session.add(vital)
                db.session.commit()
                
                # Create notification for anomalies
                if is_anomaly:
                    notification_system.create_notification(
                        patient_id=vitals_data['patient_id'],
                        severity=severity,
                        vitals=vitals_data,
                        anomaly_score=anomaly_score
                    )
                
                status = "⚠️ ANOMALY" if is_anomaly else "✓ Normal"
                print(f"Processed: {vitals_data['patient_id']} - {status} ({severity})")
                
            except Exception as e:
                if "Empty" not in str(e):
                    print(f"Error: {e}")

def run_consumer_thread(app):
    thread = threading.Thread(target=start_consumer, args=(app,), daemon=True)
    thread.start()
    return thread
