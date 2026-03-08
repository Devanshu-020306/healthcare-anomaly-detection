from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PatientVital(db.Model):
    __tablename__ = 'patient_vitals'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    heart_rate = db.Column(db.Float, nullable=False)
    spo2 = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    blood_pressure_systolic = db.Column(db.Float, nullable=False)
    blood_pressure_diastolic = db.Column(db.Float, nullable=False)
    anomaly_score = db.Column(db.Float)
    severity = db.Column(db.String(20))
    is_anomaly = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'timestamp': self.timestamp.isoformat(),
            'heart_rate': self.heart_rate,
            'spo2': self.spo2,
            'temperature': self.temperature,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'anomaly_score': self.anomaly_score,
            'severity': self.severity,
            'is_anomaly': self.is_anomaly
        }
