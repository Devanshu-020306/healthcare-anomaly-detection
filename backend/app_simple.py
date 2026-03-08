from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from models import db, PatientVital
from config_simple import Config
from datetime import datetime, timedelta
from simple_producer import run_producer_thread
from simple_consumer import run_consumer_thread, initialize_detector
from notifications import notification_system
from patient_profiles import get_patient_info, PATIENT_PROFILES
from analytics import HealthcareAnalytics
from doctor_notes import doctor_notes_system
from report_generator import report_generator
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Allow all origins for deployment
    CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        initialize_detector()
    
    return app

app = create_app()

# Start background threads
producer_thread = run_producer_thread()
consumer_thread = run_consumer_thread(app)

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'Healthcare Anomaly Detection API',
        'endpoints': [
            '/api/health',
            '/api/vitals',
            '/api/vitals/manual',
            '/api/anomalies',
            '/api/patients',
            '/api/stats',
            '/api/patient/<id>/latest',
            '/api/notifications',
            '/api/notifications/unread',
            '/api/notifications/<id>/read',
            '/api/notifications/read-all'
        ]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API is running',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/vitals', methods=['GET'])
def get_vitals():
    patient_id = request.args.get('patient_id')
    limit = request.args.get('limit', 100, type=int)
    
    query = PatientVital.query
    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    
    vitals = query.order_by(PatientVital.timestamp.desc()).limit(limit).all()
    return jsonify([v.to_dict() for v in vitals])

@app.route('/api/vitals/manual', methods=['POST'])
def add_manual_vitals():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['patient_id', 'heart_rate', 'spo2', 'temperature', 
                          'blood_pressure_systolic', 'blood_pressure_diastolic']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare vitals for ML prediction
        vitals_array = [
            float(data['heart_rate']),
            float(data['spo2']),
            float(data['temperature']),
            float(data['blood_pressure_systolic']),
            float(data['blood_pressure_diastolic'])
        ]
        
        # Get detector from consumer module
        from simple_consumer import detector
        
        # Detect anomaly
        anomaly_score, severity = detector.predict(vitals_array)
        is_anomaly = anomaly_score > Config.ANOMALY_THRESHOLDS['LOW']
        
        # Save to database
        vital = PatientVital(
            patient_id=data['patient_id'],
            heart_rate=data['heart_rate'],
            spo2=data['spo2'],
            temperature=data['temperature'],
            blood_pressure_systolic=data['blood_pressure_systolic'],
            blood_pressure_diastolic=data['blood_pressure_diastolic'],
            anomaly_score=anomaly_score,
            severity=severity,
            is_anomaly=is_anomaly
        )
        
        db.session.add(vital)
        db.session.commit()
        
        # Create notification if anomaly detected
        if is_anomaly:
            notification = notification_system.create_notification(
                patient_id=data['patient_id'],
                severity=severity,
                vitals=data,
                anomaly_score=anomaly_score
            )
        
        return jsonify({
            'success': True,
            'message': 'Vitals added successfully',
            'data': vital.to_dict(),
            'is_anomaly': is_anomaly,
            'severity': severity,
            'anomaly_score': anomaly_score
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    patient_list = []
    for p in patients:
        patient_id = p[0]
        profile = get_patient_info(patient_id)
        patient_list.append({
            'patient_id': patient_id,
            'name': profile['name'],
            'age': profile['age'],
            'gender': profile['gender'],
            'conditions': profile['conditions'],
            'risk_level': profile['risk_level']
        })
    return jsonify(patient_list)

@app.route('/api/patient/<patient_id>/profile', methods=['GET'])
def get_patient_profile(patient_id):
    profile = get_patient_info(patient_id)
    
    # Get latest vitals
    latest_vital = PatientVital.query.filter_by(patient_id=patient_id).order_by(
        PatientVital.timestamp.desc()
    ).first()
    
    # Get anomaly count
    anomaly_count = PatientVital.query.filter_by(
        patient_id=patient_id,
        is_anomaly=True
    ).count()
    
    # Get recent history
    recent_vitals = PatientVital.query.filter_by(patient_id=patient_id).order_by(
        PatientVital.timestamp.desc()
    ).limit(10).all()
    
    return jsonify({
        'profile': profile,
        'latest_vital': latest_vital.to_dict() if latest_vital else None,
        'total_anomalies': anomaly_count,
        'recent_history': [v.to_dict() for v in recent_vitals]
    })

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

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    severity = request.args.get('severity')
    limit = request.args.get('limit', 50, type=int)
    
    notifications = notification_system.get_notifications(
        unread_only=unread_only,
        severity=severity,
        limit=limit
    )
    
    return jsonify({
        'notifications': notifications,
        'unread_count': notification_system.get_unread_count(),
        'total': len(notifications)
    })

@app.route('/api/notifications/unread', methods=['GET'])
def get_unread_count():
    return jsonify({
        'unread_count': notification_system.get_unread_count()
    })

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    success = notification_system.mark_as_read(notification_id)
    if success:
        return jsonify({'success': True, 'message': 'Notification marked as read'})
    return jsonify({'error': 'Notification not found'}), 404

@app.route('/api/notifications/read-all', methods=['POST'])
def mark_all_notifications_read():
    count = notification_system.mark_all_as_read()
    return jsonify({'success': True, 'message': f'{count} notifications marked as read'})

@app.route('/api/analytics/patient/<patient_id>', methods=['GET'])
def get_patient_analytics(patient_id):
    insights = HealthcareAnalytics.get_patient_insights(patient_id)
    if insights:
        return jsonify(insights)
    return jsonify({'error': 'No data available for patient'}), 404

@app.route('/api/analytics/system', methods=['GET'])
def get_system_analytics():
    analytics = HealthcareAnalytics.get_system_analytics()
    return jsonify(analytics)

@app.route('/api/patient/<patient_id>/vitals/history', methods=['GET'])
def get_patient_vitals_history(patient_id):
    hours = request.args.get('hours', 24, type=int)
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    vitals = PatientVital.query.filter(
        PatientVital.patient_id == patient_id,
        PatientVital.timestamp >= time_threshold
    ).order_by(PatientVital.timestamp.asc()).all()
    
    return jsonify({
        'patient_id': patient_id,
        'history': [v.to_dict() for v in vitals],
        'count': len(vitals)
    })

@app.route('/api/notes', methods=['POST'])
def add_doctor_note():
    try:
        data = request.json
        note = doctor_notes_system.add_note(
            patient_id=data['patient_id'],
            doctor_name=data.get('doctor_name', 'Dr. Unknown'),
            note_text=data['note_text'],
            note_type=data.get('note_type', 'OBSERVATION')
        )
        return jsonify({'success': True, 'note': note}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/patient/<patient_id>', methods=['GET'])
def get_patient_notes(patient_id):
    notes = doctor_notes_system.get_patient_notes(patient_id)
    return jsonify({'notes': notes, 'count': len(notes)})

@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    notes = doctor_notes_system.get_all_notes()
    return jsonify({'notes': notes, 'count': len(notes)})

@app.route('/api/report/patient/<patient_id>', methods=['GET'])
def get_patient_report(patient_id):
    hours = request.args.get('hours', 24, type=int)
    report = report_generator.generate_patient_report_text(patient_id, hours)
    
    if report:
        return Response(report, mimetype='text/plain')
    return jsonify({'error': 'No data available'}), 404

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    patient_id = request.args.get('patient_id')
    hours = request.args.get('hours', 24, type=int)
    
    csv_data = report_generator.generate_csv_export(patient_id, hours)
    
    filename = f"patient_{patient_id}_data.csv" if patient_id else "all_patients_data.csv"
    
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

@app.route('/api/emergency/dashboard', methods=['GET'])
def get_emergency_dashboard():
    """Get critical patients requiring immediate attention"""
    time_threshold = datetime.utcnow() - timedelta(hours=1)
    
    # Get recent high severity anomalies
    critical_alerts = PatientVital.query.filter(
        PatientVital.timestamp >= time_threshold,
        PatientVital.severity == 'HIGH',
        PatientVital.is_anomaly == True
    ).order_by(PatientVital.timestamp.desc()).limit(20).all()
    
    # Group by patient
    critical_patients = {}
    for alert in critical_alerts:
        if alert.patient_id not in critical_patients:
            profile = get_patient_info(alert.patient_id)
            critical_patients[alert.patient_id] = {
                'patient_id': alert.patient_id,
                'patient_name': profile['name'],
                'age': profile['age'],
                'conditions': profile['conditions'],
                'risk_level': profile['risk_level'],
                'alerts': [],
                'latest_alert': alert.timestamp.isoformat()
            }
        critical_patients[alert.patient_id]['alerts'].append(alert.to_dict())
    
    return jsonify({
        'critical_patients': list(critical_patients.values()),
        'total_critical': len(critical_patients),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print("🏥 Healthcare Anomaly Detection System Starting...")
    print("=" * 60)
    print("✓ Producer thread started")
    print("✓ Consumer thread started")
    print(f"✓ Flask API starting on port {port}")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
