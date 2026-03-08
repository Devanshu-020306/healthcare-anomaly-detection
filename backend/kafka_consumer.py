import json
from kafka import KafkaConsumer
from config import Config
from models import db, PatientVital
from ml_models import AnomalyDetector
from app import create_app
import numpy as np

def start_consumer():
    app = create_app()
    detector = AnomalyDetector()
    
    # Try to load pre-trained models
    if not detector.load_models():
        print("Training new models with synthetic data...")
        training_data = np.random.randn(1000, 5) * 10 + [75, 97, 37, 120, 80]
        detector.train_models(training_data)
        detector.save_models()
    
    consumer = KafkaConsumer(
        Config.KAFKA_TOPIC,
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest'
    )
    
    print("Starting Kafka consumer...")
    
    with app.app_context():
        for message in consumer:
            vitals_data = message.value
            
            # Extract vitals for ML prediction
            vitals_array = [
                vitals_data['heart_rate'],
                vitals_data['spo2'],
                vitals_data['temperature'],
                vitals_data['blood_pressure_systolic'],
                vitals_data['blood_pressure_diastolic']
            ]
            
            # Detect anomaly
            anomaly_score, severity = detector.predict(vitals_array)
            is_anomaly = anomaly_score > Config.ANOMALY_THRESHOLDS['LOW']
            
            # Save to database
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
            
            print(f"Processed: Patient {vitals_data['patient_id']} - Anomaly: {is_anomaly} ({severity})")

if __name__ == '__main__':
    start_consumer()
