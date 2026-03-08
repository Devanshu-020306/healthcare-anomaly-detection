const API_BASE = 'https://healthcare-anomaly-detection-5.onrender.com/api';
let anomalyChart = null;

// Toggle Manual Entry Form
function toggleManualEntry() {
    const form = document.getElementById('manualEntryForm');
    form.classList.toggle('hidden');
    document.getElementById('formResult').classList.add('hidden');
    document.getElementById('vitalsForm').reset();
}

// Toggle Notification Panel
function toggleNotifications() {
    const panel = document.getElementById('notificationPanel');
    panel.classList.toggle('hidden');
    if (!panel.classList.contains('hidden')) {
        fetchNotifications();
    }
}

// Submit Manual Vitals
async function submitVitals(event) {
    event.preventDefault();
    
    const data = {
        patient_id: document.getElementById('patientId').value,
        heart_rate: parseFloat(document.getElementById('heartRate').value),
        spo2: parseFloat(document.getElementById('spo2').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        blood_pressure_systolic: parseFloat(document.getElementById('bpSystolic').value),
        blood_pressure_diastolic: parseFloat(document.getElementById('bpDiastolic').value)
    };
    
    const resultDiv = document.getElementById('formResult');
    resultDiv.classList.remove('hidden');
    resultDiv.className = 'form-result';
    resultDiv.innerHTML = '<p>⏳ Processing...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/vitals/manual`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            const severityClass = result.severity === 'HIGH' ? 'alert-high' : 
                                 result.severity === 'MEDIUM' ? 'alert-medium' : 'alert-low';
            
            resultDiv.className = `form-result ${severityClass}`;
            resultDiv.innerHTML = `
                <h3>${result.is_anomaly ? '⚠️ Anomaly Detected!' : '✓ Normal Reading'}</h3>
                <p><strong>Patient:</strong> ${data.patient_id}</p>
                <p><strong>Severity:</strong> ${result.severity}</p>
                <p><strong>Anomaly Score:</strong> ${result.anomaly_score.toFixed(3)}</p>
                <p>${result.message}</p>
            `;
            
            // Refresh dashboard data
            setTimeout(() => {
                refreshData();
                fetchNotifications();
            }, 1000);
            
            // Reset form after 3 seconds
            setTimeout(() => {
                document.getElementById('vitalsForm').reset();
            }, 3000);
        } else {
            resultDiv.className = 'form-result alert-high';
            resultDiv.innerHTML = `<p>❌ Error: ${result.error}</p>`;
        }
    } catch (error) {
        console.error('Error submitting vitals:', error);
        resultDiv.className = 'form-result alert-high';
        resultDiv.innerHTML = `
            <p>❌ Connection Error: ${error.message}</p>
            <p style="font-size: 0.9em; margin-top: 10px;">
                Make sure the backend server is running at ${API_BASE}
            </p>
        `;
    }
}

// Fetch Notifications
async function fetchNotifications() {
    try {
        const response = await fetch(`${API_BASE}/notifications?limit=20`);
        const data = await response.json();
        
        updateNotificationBadge(data.unread_count);
        displayNotifications(data.notifications);
    } catch (error) {
        console.error('Error fetching notifications:', error);
    }
}

// Update Notification Badge
function updateNotificationBadge(count) {
    const badge = document.getElementById('notificationBadge');
    badge.textContent = count;
    badge.style.display = count > 0 ? 'inline-block' : 'none';
}

// Display Notifications
function displayNotifications(notifications) {
    const list = document.getElementById('notificationList');
    
    if (notifications.length === 0) {
        list.innerHTML = '<p class="no-notifications">No notifications</p>';
        return;
    }
    
    list.innerHTML = notifications.map(notif => {
        const severityClass = notif.severity === 'HIGH' ? 'notif-high' : 
                             notif.severity === 'MEDIUM' ? 'notif-medium' : 'notif-low';
        const readClass = notif.read ? 'read' : 'unread';
        
        const conditionsText = notif.conditions && notif.conditions.length > 0 
            ? notif.conditions.join(', ') 
            : 'No known conditions';
        
        const recommendationsHTML = notif.recommendations && notif.recommendations.length > 0
            ? `<div class="notif-recommendations">
                <strong>Recommendations:</strong>
                <ul>${notif.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>
               </div>`
            : '';
        
        return `
            <div class="notification-item ${severityClass} ${readClass}" onclick="markAsRead(${notif.id})">
                <div class="notif-header">
                    <span class="notif-severity">${notif.severity}</span>
                    <span class="notif-time">${new Date(notif.timestamp).toLocaleString()}</span>
                </div>
                <div class="notif-patient-info">
                    <strong>${notif.patient_name || notif.patient_id}</strong> 
                    (${notif.age || 'N/A'}y, ${notif.gender || 'N/A'})
                    ${notif.risk_level ? `<span class="risk-badge risk-${notif.risk_level}">${notif.risk_level} RISK</span>` : ''}
                </div>
                <p class="notif-message">${notif.message}</p>
                <div class="notif-conditions">
                    <strong>Conditions:</strong> ${conditionsText}
                </div>
                <div class="notif-vitals">
                    HR: ${notif.vitals.heart_rate} | SpO₂: ${notif.vitals.spo2}% | 
                    Temp: ${notif.vitals.temperature}°C | 
                    BP: ${notif.vitals.blood_pressure_systolic}/${notif.vitals.blood_pressure_diastolic}
                </div>
                ${recommendationsHTML}
            </div>
        `;
    }).join('');
}

// Mark Notification as Read
async function markAsRead(notificationId) {
    try {
        await fetch(`${API_BASE}/notifications/${notificationId}/read`, {
            method: 'POST'
        });
        fetchNotifications();
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

// Mark All Notifications as Read
async function markAllAsRead() {
    try {
        await fetch(`${API_BASE}/notifications/read-all`, {
            method: 'POST'
        });
        fetchNotifications();
    } catch (error) {
        console.error('Error marking all as read:', error);
    }
}

async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        document.getElementById('totalRecords').textContent = data.total_records;
        document.getElementById('totalAnomalies').textContent = data.total_anomalies;
        document.getElementById('anomalyRate').textContent = `${data.anomaly_rate}%`;
        document.getElementById('highSeverity').textContent = data.severity_breakdown.HIGH;
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

async function fetchPatients() {
    try {
        const response = await fetch(`${API_BASE}/patients`);
        const patients = await response.json();
        
        const select = document.getElementById('patientSelect');
        select.innerHTML = '<option value="">All Patients</option>';
        patients.forEach(patient => {
            const option = document.createElement('option');
            option.value = patient.patient_id;
            option.textContent = `${patient.patient_id} - ${patient.name} (${patient.age}y, ${patient.risk_level} Risk)`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching patients:', error);
    }
}

async function fetchAnomalies() {
    try {
        const response = await fetch(`${API_BASE}/anomalies?hours=24`);
        const anomalies = await response.json();
        
        updateTable(anomalies);
        updateChart(anomalies);
    } catch (error) {
        console.error('Error fetching anomalies:', error);
    }
}

function updateTable(anomalies) {
    const tbody = document.getElementById('anomalyTableBody');
    tbody.innerHTML = '';
    
    anomalies.slice(0, 20).forEach(anomaly => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${anomaly.patient_id}</td>
            <td>${new Date(anomaly.timestamp).toLocaleString()}</td>
            <td>${anomaly.heart_rate}</td>
            <td>${anomaly.spo2}%</td>
            <td>${anomaly.temperature}°C</td>
            <td>${anomaly.blood_pressure_systolic}/${anomaly.blood_pressure_diastolic}</td>
            <td class="severity-${anomaly.severity}">${anomaly.severity}</td>
            <td>${anomaly.anomaly_score.toFixed(3)}</td>
        `;
    });
}

function updateChart(anomalies) {
    const severityCounts = { HIGH: 0, MEDIUM: 0, LOW: 0 };
    anomalies.forEach(a => severityCounts[a.severity]++);
    
    const ctx = document.getElementById('anomalyChart').getContext('2d');
    
    if (anomalyChart) {
        anomalyChart.destroy();
    }
    
    anomalyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['HIGH', 'MEDIUM', 'LOW'],
            datasets: [{
                label: 'Anomaly Count by Severity',
                data: [severityCounts.HIGH, severityCounts.MEDIUM, severityCounts.LOW],
                backgroundColor: ['#dc3545', '#ffc107', '#28a745']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function refreshData() {
    fetchStats();
    fetchAnomalies();
    fetchNotifications();
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchPatients();
    fetchAnomalies();
    fetchNotifications();
    
    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
        document.getElementById('darkModeBtn').textContent = '☀️ Light Mode';
    }
    
    // Auto-refresh every 10 seconds
    setInterval(refreshData, 10000);
});

// Dark Mode Toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.getElementById('darkModeBtn').textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
}

// Download Report
async function downloadReport() {
    const patientId = document.getElementById('patientSelect').value;
    if (!patientId) {
        alert('Please select a patient first');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/report/patient/${patientId}?hours=24`);
        const report = await response.text();
        
        const blob = new Blob([report], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `patient_${patientId}_report_${new Date().toISOString().split('T')[0]}.txt`;
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error downloading report:', error);
        alert('Error downloading report');
    }
}

// Export CSV
async function exportCSV() {
    const patientId = document.getElementById('patientSelect').value;
    const url = patientId 
        ? `${API_BASE}/export/csv?patient_id=${patientId}&hours=24`
        : `${API_BASE}/export/csv?hours=24`;
    
    try {
        window.open(url, '_blank');
    } catch (error) {
        console.error('Error exporting CSV:', error);
        alert('Error exporting CSV');
    }
}
