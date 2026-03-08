import json
import time
import random
from kafka import KafkaProducer
from config import Config

def generate_patient_vitals(patient_id):
    # Normal ranges with occasional anomalies
    is_anomaly = random.random() < 0.15
    
    if is_anomaly:
        heart_rate = random.choice([random.uniform(40, 50), random.uniform(120, 180)])
        spo2 = random.uniform(75, 92)
        temperature = random.choice([random.uniform(35, 36), random.uniform(39, 41)])
        bp_systolic = random.choice([random.uniform(80, 90), random.uniform(160, 200)])
        bp_diastolic = random.choice([random.uniform(40, 50), random.uniform(100, 130)])
    else:
        heart_rate = random.uniform(60, 100)
        spo2 = random.uniform(95, 100)
        temperature = random.uniform(36.5, 37.5)
        bp_systolic = random.uniform(110, 140)
        bp_diastolic = random.uniform(70, 90)
    
    return {
        'patient_id': patient_id,
        'heart_rate': round(heart_rate, 2),
        'spo2': round(spo2, 2),
        'temperature': round(temperature, 2),
        'blood_pressure_systolic': round(bp_systolic, 2),
        'blood_pressure_diastolic': round(bp_diastolic, 2),
        'timestamp': time.time()
    }

def start_producer():
    producer = KafkaProducer(
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    patient_ids = [f'P{str(i).zfill(3)}' for i in range(1, 11)]
    
    print("Starting Kafka producer...")
    try:
        while True:
            for patient_id in patient_ids:
                vitals = generate_patient_vitals(patient_id)
                producer.send(Config.KAFKA_TOPIC, value=vitals)
                print(f"Sent: {vitals}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Producer stopped")
    finally:
        producer.close()

if __name__ == '__main__':
    start_producer()
