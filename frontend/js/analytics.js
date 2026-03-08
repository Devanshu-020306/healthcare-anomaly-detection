    const API_BASE = 'https://healthcare-anomaly-detection-5.onrender.com/api';
let hourlyChart = null;
let patientTrendsChart = null;

// Load System Analytics
async function loadSystemAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/analytics/system`);
        const data = await response.json();
        
        document.getElementById('totalPatients').textContent = data.total_patients;
        document.getElementById('totalReadings').textContent = data.total_readings_24h;
        document.getElementById('systemAnomalyRate').textContent = `${data.anomaly_rate_24h}%`;
        document.getElementById('highRiskPatients').textContent = data.high_risk_patients;
        
        // Update hourly chart
        updateHourlyChart(data.hourly_breakdown);
    } catch (error) {
        console.error('Error loading system analytics:', error);
    }
}

// Update Hourly Chart
function updateHourlyChart(hourlyData) {
    const ctx = document.getElementById('hourlyChart').getContext('2d');
    
    if (hourlyChart) {
        hourlyChart.destroy();
    }
    
    hourlyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hourlyData.map(h => h.hour),
            datasets: [
                {
                    label: 'Total Readings',
                    data: hourlyData.map(h => h.readings),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Anomalies',
                    data: hourlyData.map(h => h.anomalies),
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Readings and Anomalies by Hour'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Load Patients for Dropdowns
async function loadPatients() {
    try {
        const response = await fetch(`${API_BASE}/patients`);
        const patients = await response.json();
        
        const selects = ['analyticsPatientSelect', 'notePatientId'];
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">-- Select Patient --</option>';
            patients.forEach(patient => {
                const option = document.createElement('option');
                option.value = patient.patient_id;
                option.textContent = `${patient.patient_id} - ${patient.name} (${patient.age}y)`;
                select.appendChild(option);
            });
        });
    } catch (error) {
        console.error('Error loading patients:', error);
    }
}

// Load Patient Analytics
async function loadPatientAnalytics() {
    const patientId = document.getElementById('analyticsPatientSelect').value;
    if (!patientId) {
        document.getElementById('patientAnalytics').classList.add('hidden');
        return;
    }
    
    try {
        const [analyticsRes, historyRes] = await Promise.all([
            fetch(`${API_BASE}/analytics/patient/${patientId}`),
            fetch(`${API_BASE}/patient/${patientId}/vitals/history?hours=24`)
        ]);
        
        const analytics = await analyticsRes.json();
        const history = await historyRes.json();
        
        // Show analytics section
        document.getElementById('patientAnalytics').classList.remove('hidden');
        
        // Update patient header
        document.getElementById('patientName').textContent = 
            `${analytics.patient_name} (${analytics.age}y) - ${analytics.conditions.join(', ')}`;
        
        const riskBadge = document.getElementById('riskBadge');
        riskBadge.textContent = `${analytics.risk_level} RISK`;
        riskBadge.className = `risk-badge risk-${analytics.risk_level}`;
        
        // Update stats
        document.getElementById('patientAnomalyRate').textContent = `${analytics.anomaly_rate}%`;
        document.getElementById('patientReadings').textContent = analytics.total_readings;
        document.getElementById('riskPrediction').textContent = `${(analytics.risk_prediction * 100).toFixed(0)}%`;
        document.getElementById('patientAnomalies').textContent = analytics.anomaly_count;
        
        // Update vitals stats table
        updateVitalsStatsTable(analytics.vitals_stats, analytics.trends);
        
        // Update recommendations
        updateRecommendations(analytics.recommendations);
        
        // Update trends chart
        updatePatientTrendsChart(history.history);
        
    } catch (error) {
        console.error('Error loading patient analytics:', error);
    }
}

// Update Vitals Stats Table
function updateVitalsStatsTable(stats, trends) {
    const tbody = document.getElementById('vitalsStatsBody');
    tbody.innerHTML = '';
    
    const vitals = [
        { name: 'Heart Rate', key: 'heart_rate', unit: 'BPM', trend: trends.heart_rate },
        { name: 'SpO₂', key: 'spo2', unit: '%', trend: trends.spo2 },
        { name: 'Temperature', key: 'temperature', unit: '°C', trend: 'stable' },
        { name: 'BP Systolic', key: 'bp_systolic', unit: 'mmHg', trend: trends.bp }
    ];
    
    vitals.forEach(vital => {
        const stat = stats[vital.key];
        const trendIcon = vital.trend === 'increasing' ? '📈' : 
                         vital.trend === 'decreasing' ? '📉' : '➡️';
        const trendClass = vital.trend === 'increasing' ? 'trend-up' : 
                          vital.trend === 'decreasing' ? 'trend-down' : 'trend-stable';
        
        const row = tbody.insertRow();
        row.innerHTML = `
            <td><strong>${vital.name}</strong></td>
            <td>${stat.avg} ${vital.unit}</td>
            <td>${stat.min} ${vital.unit}</td>
            <td>${stat.max} ${vital.unit}</td>
            <td>${stat.std}</td>
            <td class="${trendClass}">${trendIcon} ${vital.trend}</td>
        `;
    });
}

// Update Recommendations
function updateRecommendations(recommendations) {
    const list = document.getElementById('aiRecommendations');
    list.innerHTML = '';
    
    if (recommendations.length === 0) {
        list.innerHTML = '<li>No specific recommendations at this time</li>';
        return;
    }
    
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        list.appendChild(li);
    });
}

// Update Patient Trends Chart
function updatePatientTrendsChart(history) {
    const ctx = document.getElementById('patientTrendsChart').getContext('2d');
    
    if (patientTrendsChart) {
        patientTrendsChart.destroy();
    }
    
    const labels = history.map(h => new Date(h.timestamp).toLocaleTimeString());
    
    patientTrendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Heart Rate (BPM)',
                    data: history.map(h => h.heart_rate),
                    borderColor: '#dc3545',
                    yAxisID: 'y'
                },
                {
                    label: 'SpO₂ (%)',
                    data: history.map(h => h.spo2),
                    borderColor: '#28a745',
                    yAxisID: 'y1'
                },
                {
                    label: 'Temperature (°C)',
                    data: history.map(h => h.temperature),
                    borderColor: '#ffc107',
                    yAxisID: 'y2'
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Heart Rate (BPM)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'SpO₂ (%)' },
                    grid: { drawOnChartArea: false }
                },
                y2: {
                    type: 'linear',
                    display: false,
                    position: 'right'
                }
            }
        }
    });
}

// Toggle Notes Form
function toggleNotesForm() {
    document.getElementById('notesForm').classList.toggle('hidden');
}

// Submit Note
async function submitNote(event) {
    event.preventDefault();
    
    const data = {
        patient_id: document.getElementById('notePatientId').value,
        doctor_name: document.getElementById('doctorName').value,
        note_type: document.getElementById('noteType').value,
        note_text: document.getElementById('noteText').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/notes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Note added successfully!');
            document.getElementById('notesForm').reset();
            toggleNotesForm();
            loadNotes();
        }
    } catch (error) {
        console.error('Error submitting note:', error);
        alert('Error adding note');
    }
}

// Load Notes
async function loadNotes() {
    try {
        const response = await fetch(`${API_BASE}/notes`);
        const data = await response.json();
        
        const notesList = document.getElementById('notesList');
        notesList.innerHTML = '';
        
        if (data.notes.length === 0) {
            notesList.innerHTML = '<p class="no-notes">No clinical notes yet</p>';
            return;
        }
        
        data.notes.forEach(note => {
            const noteDiv = document.createElement('div');
            noteDiv.className = `note-item note-${note.note_type.toLowerCase()}`;
            noteDiv.innerHTML = `
                <div class="note-header">
                    <span class="note-type">${note.note_type}</span>
                    <span class="note-patient">${note.patient_id}</span>
                    <span class="note-time">${new Date(note.timestamp).toLocaleString()}</span>
                </div>
                <div class="note-doctor">👨‍⚕️ ${note.doctor_name}</div>
                <div class="note-text">${note.note_text}</div>
            `;
            notesList.appendChild(noteDiv);
        });
    } catch (error) {
        console.error('Error loading notes:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSystemAnalytics();
    loadPatients();
    loadNotes();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadSystemAnalytics();
        const patientId = document.getElementById('analyticsPatientSelect').value;
        if (patientId) {
            loadPatientAnalytics();
        }
    }, 30000);
});
