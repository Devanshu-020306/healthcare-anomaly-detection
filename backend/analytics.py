import numpy as np
from datetime import datetime, timedelta
from models import PatientVital
from patient_profiles import get_patient_info

class HealthcareAnalytics:
    
    @staticmethod
    def predict_risk_score(patient_id, recent_vitals):
        """Predict future health risk based on trends"""
        if len(recent_vitals) < 5:
            return 0.5
        
        profile = get_patient_info(patient_id)
        
        # Calculate trend scores
        hr_trend = np.polyfit(range(len(recent_vitals)), 
                              [v.heart_rate for v in recent_vitals], 1)[0]
        spo2_trend = np.polyfit(range(len(recent_vitals)), 
                                [v.spo2 for v in recent_vitals], 1)[0]
        bp_trend = np.polyfit(range(len(recent_vitals)), 
                              [v.blood_pressure_systolic for v in recent_vitals], 1)[0]
        
        # Risk factors
        risk_score = 0.0
        
        # Worsening trends
        if hr_trend > 2:  # Heart rate increasing
            risk_score += 0.2
        if spo2_trend < -0.5:  # Oxygen decreasing
            risk_score += 0.3
        if bp_trend > 3:  # BP increasing
            risk_score += 0.2
        
        # Recent anomalies
        recent_anomalies = sum(1 for v in recent_vitals if v.is_anomaly)
        risk_score += (recent_anomalies / len(recent_vitals)) * 0.3
        
        # Patient risk level
        if profile['risk_level'] == 'HIGH':
            risk_score += 0.2
        elif profile['risk_level'] == 'MEDIUM':
            risk_score += 0.1
        
        return min(risk_score, 1.0)
    
    @staticmethod
    def get_patient_insights(patient_id):
        """Generate insights for a patient"""
        from sqlalchemy import func
        
        # Get last 24 hours data
        time_threshold = datetime.utcnow() - timedelta(hours=24)
        vitals = PatientVital.query.filter(
            PatientVital.patient_id == patient_id,
            PatientVital.timestamp >= time_threshold
        ).order_by(PatientVital.timestamp.desc()).all()
        
        if not vitals:
            return None
        
        profile = get_patient_info(patient_id)
        
        # Calculate statistics
        hr_values = [v.heart_rate for v in vitals]
        spo2_values = [v.spo2 for v in vitals]
        temp_values = [v.temperature for v in vitals]
        bp_sys_values = [v.blood_pressure_systolic for v in vitals]
        
        insights = {
            'patient_id': patient_id,
            'patient_name': profile['name'],
            'age': profile['age'],
            'conditions': profile['conditions'],
            'risk_level': profile['risk_level'],
            'total_readings': len(vitals),
            'anomaly_count': sum(1 for v in vitals if v.is_anomaly),
            'anomaly_rate': round(sum(1 for v in vitals if v.is_anomaly) / len(vitals) * 100, 1),
            'vitals_stats': {
                'heart_rate': {
                    'avg': round(np.mean(hr_values), 1),
                    'min': round(min(hr_values), 1),
                    'max': round(max(hr_values), 1),
                    'std': round(np.std(hr_values), 1)
                },
                'spo2': {
                    'avg': round(np.mean(spo2_values), 1),
                    'min': round(min(spo2_values), 1),
                    'max': round(max(spo2_values), 1),
                    'std': round(np.std(spo2_values), 1)
                },
                'temperature': {
                    'avg': round(np.mean(temp_values), 2),
                    'min': round(min(temp_values), 2),
                    'max': round(max(temp_values), 2),
                    'std': round(np.std(temp_values), 2)
                },
                'bp_systolic': {
                    'avg': round(np.mean(bp_sys_values), 1),
                    'min': round(min(bp_sys_values), 1),
                    'max': round(max(bp_sys_values), 1),
                    'std': round(np.std(bp_sys_values), 1)
                }
            },
            'risk_prediction': round(HealthcareAnalytics.predict_risk_score(patient_id, vitals[:10]), 2),
            'trends': {
                'heart_rate': 'increasing' if np.polyfit(range(len(vitals[:10])), [v.heart_rate for v in vitals[:10]], 1)[0] > 1 else 'stable',
                'spo2': 'decreasing' if np.polyfit(range(len(vitals[:10])), [v.spo2 for v in vitals[:10]], 1)[0] < -0.5 else 'stable',
                'bp': 'increasing' if np.polyfit(range(len(vitals[:10])), [v.blood_pressure_systolic for v in vitals[:10]], 1)[0] > 2 else 'stable'
            },
            'latest_vital': vitals[0].to_dict() if vitals else None
        }
        
        # Generate recommendations
        recommendations = []
        if insights['anomaly_rate'] > 30:
            recommendations.append("⚠️ High anomaly rate - Requires immediate medical attention")
        if insights['trends']['spo2'] == 'decreasing':
            recommendations.append("📉 Oxygen saturation declining - Monitor respiratory function")
        if insights['trends']['heart_rate'] == 'increasing':
            recommendations.append("📈 Heart rate trending up - Check for cardiac stress")
        if insights['risk_prediction'] > 0.7:
            recommendations.append("🔴 HIGH RISK: Predictive model indicates elevated risk - Increase monitoring frequency")
        
        insights['recommendations'] = recommendations
        
        return insights
    
    @staticmethod
    def get_system_analytics():
        """Get overall system analytics"""
        from sqlalchemy import func
        
        # Last 24 hours
        time_threshold = datetime.utcnow() - timedelta(hours=24)
        
        total_patients = PatientVital.query.with_entities(
            func.count(func.distinct(PatientVital.patient_id))
        ).scalar()
        
        total_readings = PatientVital.query.filter(
            PatientVital.timestamp >= time_threshold
        ).count()
        
        total_anomalies = PatientVital.query.filter(
            PatientVital.timestamp >= time_threshold,
            PatientVital.is_anomaly == True
        ).count()
        
        high_risk_patients = PatientVital.query.filter(
            PatientVital.timestamp >= time_threshold,
            PatientVital.severity == 'HIGH'
        ).with_entities(func.count(func.distinct(PatientVital.patient_id))).scalar()
        
        # Hourly breakdown
        hourly_stats = []
        for i in range(24):
            hour_start = datetime.utcnow() - timedelta(hours=i+1)
            hour_end = datetime.utcnow() - timedelta(hours=i)
            
            hour_readings = PatientVital.query.filter(
                PatientVital.timestamp >= hour_start,
                PatientVital.timestamp < hour_end
            ).count()
            
            hour_anomalies = PatientVital.query.filter(
                PatientVital.timestamp >= hour_start,
                PatientVital.timestamp < hour_end,
                PatientVital.is_anomaly == True
            ).count()
            
            hourly_stats.append({
                'hour': hour_start.strftime('%H:00'),
                'readings': hour_readings,
                'anomalies': hour_anomalies
            })
        
        return {
            'total_patients': total_patients,
            'total_readings_24h': total_readings,
            'total_anomalies_24h': total_anomalies,
            'anomaly_rate_24h': round(total_anomalies / total_readings * 100, 1) if total_readings > 0 else 0,
            'high_risk_patients': high_risk_patients,
            'hourly_breakdown': list(reversed(hourly_stats)),
            'timestamp': datetime.utcnow().isoformat()
        }
