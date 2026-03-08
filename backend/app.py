from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, PatientVital
from config import Config
from datetime import datetime, timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

@app.route('/api/vitals', methods=['GET'])
def get_vitals():
    patient_id = request.args.get('patient_id')
    limit = request.args.get('limit', 100, type=int)
    
    query = PatientVital.query
    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    
    vitals = query.order_by(PatientVital.timestamp.desc()).limit(limit).all()
    return jsonify([v.to_dict() for v in vitals])

@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    hours = request.args.get('hours', 24, type=int)
    severity = request.args.get('severity')
    
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    query = PatientVital.query.filter(
        PatientVital.is_anomaly == True,
        PatientVital.timestamp >= time_threshold
    )
    
    if severity:
        query = query.filter_by(severity=severity)
    
    anomalies = query.order_by(PatientVital.timestamp.desc()).all()
    return jsonify([a.to_dict() for a in anomalies])

@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = db.session.query(PatientVital.patient_id).distinct().all()
    return jsonify([p[0] for p in patients])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_records = PatientVital.query.count()
    total_anomalies = PatientVital.query.filter_by(is_anomaly=True).count()
    
    high_severity = PatientVital.query.filter_by(severity='HIGH', is_anomaly=True).count()
    medium_severity = PatientVital.query.filter_by(severity='MEDIUM', is_anomaly=True).count()
    low_severity = PatientVital.query.filter_by(severity='LOW', is_anomaly=True).count()
    
    return jsonify({
        'total_records': total_records,
        'total_anomalies': total_anomalies,
        'anomaly_rate': round(total_anomalies / total_records * 100, 2) if total_records > 0 else 0,
        'severity_breakdown': {
            'HIGH': high_severity,
            'MEDIUM': medium_severity,
            'LOW': low_severity
        }
    })

@app.route('/api/patient/<patient_id>/latest', methods=['GET'])
def get_patient_latest(patient_id):
    vital = PatientVital.query.filter_by(patient_id=patient_id).order_by(
        PatientVital.timestamp.desc()
    ).first()
    
    if vital:
        return jsonify(vital.to_dict())
    return jsonify({'error': 'Patient not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
