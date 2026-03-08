from datetime import datetime, timedelta
from models import PatientVital
from patient_profiles import get_patient_info
import csv
import io

class ReportGenerator:
    
    @staticmethod
    def generate_patient_report_text(patient_id, hours=24):
        """Generate text report for a patient"""
        profile = get_patient_info(patient_id)
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        
        vitals = PatientVital.query.filter(
            PatientVital.patient_id == patient_id,
            PatientVital.timestamp >= time_threshold
        ).order_by(PatientVital.timestamp.desc()).all()
        
        if not vitals:
            return None
        
        # Calculate statistics
        hr_values = [v.heart_rate for v in vitals]
        spo2_values = [v.spo2 for v in vitals]
        temp_values = [v.temperature for v in vitals]
        bp_sys_values = [v.blood_pressure_systolic for v in vitals]
        bp_dia_values = [v.blood_pressure_diastolic for v in vitals]
        
        anomaly_count = sum(1 for v in vitals if v.is_anomaly)
        high_severity = sum(1 for v in vitals if v.severity == 'HIGH')
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          PATIENT HEALTH MONITORING REPORT                    ║
╚══════════════════════════════════════════════════════════════╝

PATIENT INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Patient ID:        {patient_id}
Name:              {profile['name']}
Age:               {profile['age']} years
Gender:            {profile['gender']}
Risk Level:        {profile['risk_level']}

Medical Conditions:
{chr(10).join(f'  • {cond}' for cond in profile['conditions'])}

Current Medications:
{chr(10).join(f'  • {med}' for med in profile['medications']) if profile['medications'] else '  • None'}

REPORT PERIOD:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
From:              {time_threshold.strftime('%Y-%m-%d %H:%M:%S')}
To:                {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
Duration:          {hours} hours

MONITORING SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Readings:    {len(vitals)}
Anomalies:         {anomaly_count} ({round(anomaly_count/len(vitals)*100, 1)}%)
High Severity:     {high_severity}
Status:            {'⚠️ REQUIRES ATTENTION' if anomaly_count > len(vitals)*0.3 else '✓ STABLE'}

VITAL SIGNS STATISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Heart Rate (BPM):
  Average:         {sum(hr_values)/len(hr_values):.1f}
  Minimum:         {min(hr_values):.1f}
  Maximum:         {max(hr_values):.1f}
  Normal Range:    {profile['normal_ranges']['heart_rate'][0]}-{profile['normal_ranges']['heart_rate'][1]}

Oxygen Saturation (SpO₂ %):
  Average:         {sum(spo2_values)/len(spo2_values):.1f}
  Minimum:         {min(spo2_values):.1f}
  Maximum:         {max(spo2_values):.1f}
  Normal Range:    {profile['normal_ranges']['spo2'][0]}-{profile['normal_ranges']['spo2'][1]}

Body Temperature (°C):
  Average:         {sum(temp_values)/len(temp_values):.2f}
  Minimum:         {min(temp_values):.2f}
  Maximum:         {max(temp_values):.2f}
  Normal Range:    {profile['normal_ranges']['temperature'][0]}-{profile['normal_ranges']['temperature'][1]}

Blood Pressure (mmHg):
  Systolic Avg:    {sum(bp_sys_values)/len(bp_sys_values):.1f}
  Diastolic Avg:   {sum(bp_dia_values)/len(bp_dia_values):.1f}
  Systolic Range:  {min(bp_sys_values):.1f} - {max(bp_sys_values):.1f}
  Diastolic Range: {min(bp_dia_values):.1f} - {max(bp_dia_values):.1f}

RECENT ANOMALIES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        recent_anomalies = [v for v in vitals[:10] if v.is_anomaly]
        if recent_anomalies:
            for i, v in enumerate(recent_anomalies, 1):
                report += f"""
{i}. {v.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {v.severity}
   HR: {v.heart_rate} | SpO₂: {v.spo2}% | Temp: {v.temperature}°C
   BP: {v.blood_pressure_systolic}/{v.blood_pressure_diastolic}
   Anomaly Score: {v.anomaly_score:.3f}
"""
        else:
            report += "\n  No recent anomalies detected.\n"
        
        report += f"""
RECOMMENDATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if anomaly_count > len(vitals) * 0.3:
            report += "  ⚠️ High anomaly rate - Increase monitoring frequency\n"
        if high_severity > 0:
            report += "  🔴 Critical alerts detected - Immediate medical review required\n"
        if max(hr_values) > 120:
            report += "  ⚠️ Tachycardia episodes detected - Cardiac evaluation recommended\n"
        if min(spo2_values) < 90:
            report += "  🔴 Severe hypoxemia detected - Oxygen therapy required\n"
        if not (anomaly_count > len(vitals) * 0.3 or high_severity > 0):
            report += "  ✓ Patient vitals within acceptable parameters\n"
            report += "  ✓ Continue routine monitoring\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
System: AI-Driven Healthcare Anomaly Detection System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return report
    
    @staticmethod
    def generate_csv_export(patient_id=None, hours=24):
        """Generate CSV export of patient data"""
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        
        query = PatientVital.query.filter(PatientVital.timestamp >= time_threshold)
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        
        vitals = query.order_by(PatientVital.timestamp.desc()).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Patient ID', 'Timestamp', 'Heart Rate', 'SpO2', 'Temperature',
            'BP Systolic', 'BP Diastolic', 'Anomaly Score', 'Severity',
            'Is Anomaly'
        ])
        
        # Write data
        for v in vitals:
            writer.writerow([
                v.patient_id,
                v.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                v.heart_rate,
                v.spo2,
                v.temperature,
                v.blood_pressure_systolic,
                v.blood_pressure_diastolic,
                round(v.anomaly_score, 4) if v.anomaly_score else '',
                v.severity or '',
                'Yes' if v.is_anomaly else 'No'
            ])
        
        return output.getvalue()

report_generator = ReportGenerator()
