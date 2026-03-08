import os
from queue import Queue

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///healthcare.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # In-memory queue instead of Kafka
    VITALS_QUEUE = Queue()
    
    # Anomaly thresholds
    ANOMALY_THRESHOLDS = {
        'LOW': 0.3,
        'MEDIUM': 0.6,
        'HIGH': 0.8
    }
