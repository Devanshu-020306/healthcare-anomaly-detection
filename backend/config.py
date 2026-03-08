import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/healthcare_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_SERVERS', 'localhost:9092')
    KAFKA_TOPIC = 'patient-vitals'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Anomaly thresholds
    ANOMALY_THRESHOLDS = {
        'LOW': 0.3,
        'MEDIUM': 0.6,
        'HIGH': 0.8
    }
