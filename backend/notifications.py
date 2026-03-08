import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
from patient_profiles import get_patient_info, get_clinical_recommendation

class NotificationSystem:
    def __init__(self):
        self.notifications = []
        self.max_notifications = 100
        
    def create_notification(self, patient_id, severity, vitals, anomaly_score):
        profile = get_patient_info(patient_id)
        recommendations = get_clinical_recommendation(patient_id, vitals, severity)
        
        notification = {
            'id': len(self.notifications) + 1,
            'patient_id': patient_id,
            'patient_name': profile['name'],
            'age': profile['age'],
            'gender': profile['gender'],
            'conditions': profile['conditions'],
            'risk_level': profile['risk_level'],
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat(),
            'message': self._generate_message(patient_id, profile, severity, vitals, anomaly_score),
            'vitals': vitals,
            'anomaly_score': anomaly_score,
            'recommendations': recommendations,
            'read': False
        }
        
        self.notifications.insert(0, notification)
        
        # Keep only recent notifications
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[:self.max_notifications]
        
        # Print to console with patient info
        icon = '🔴' if severity == 'HIGH' else '🟡' if severity == 'MEDIUM' else '🟢'
        print(f"\n{icon} ALERT: {profile['name']} ({patient_id}) - {severity}")
        print(f"   Age: {profile['age']}, Conditions: {', '.join(profile['conditions'])}")
        print(f"   {notification['message']}")
        if recommendations:
            print(f"   Recommendation: {recommendations[0]}")
        
        return notification
    
    def _generate_message(self, patient_id, profile, severity, vitals, anomaly_score):
        messages = {
            'HIGH': f"🔴 CRITICAL ALERT: {profile['name']} showing severe anomaly",
            'MEDIUM': f"🟡 WARNING: {profile['name']} showing moderate anomaly",
            'LOW': f"🟢 NOTICE: {profile['name']} showing minor anomaly"
        }
        
        # Add specific vital concerns
        concerns = []
        if vitals.get('heart_rate', 0) > 120:
            concerns.append(f"Tachycardia: {vitals['heart_rate']} BPM")
        elif vitals.get('heart_rate', 0) < 50:
            concerns.append(f"Bradycardia: {vitals['heart_rate']} BPM")
            
        if vitals.get('spo2', 100) < 90:
            concerns.append(f"Critical SpO2: {vitals['spo2']}%")
        elif vitals.get('spo2', 100) < 94:
            concerns.append(f"Low SpO2: {vitals['spo2']}%")
            
        if vitals.get('temperature', 37) > 38.5:
            concerns.append(f"Fever: {vitals['temperature']}°C")
        elif vitals.get('temperature', 37) < 36:
            concerns.append(f"Hypothermia: {vitals['temperature']}°C")
            
        if vitals.get('blood_pressure_systolic', 120) > 160:
            concerns.append(f"Hypertensive: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']}")
        elif vitals.get('blood_pressure_systolic', 120) < 90:
            concerns.append(f"Hypotensive: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']}")
        
        message = messages.get(severity, "Anomaly detected")
        if concerns:
            message += " - " + ", ".join(concerns)
        
        # Add patient context
        if profile['conditions']:
            message += f" | Known conditions: {', '.join(profile['conditions'][:2])}"
        
        return message
    
    def get_notifications(self, unread_only=False, severity=None, limit=50):
        filtered = self.notifications
        
        if unread_only:
            filtered = [n for n in filtered if not n['read']]
        
        if severity:
            filtered = [n for n in filtered if n['severity'] == severity]
        
        return filtered[:limit]
    
    def mark_as_read(self, notification_id):
        for notification in self.notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                return True
        return False
    
    def mark_all_as_read(self):
        for notification in self.notifications:
            notification['read'] = False
        return len(self.notifications)
    
    def get_unread_count(self):
        return sum(1 for n in self.notifications if not n['read'])

# Global notification system instance
notification_system = NotificationSystem()
