import numpy as np
from sklearn.ensemble import IsolationForest
import pickle
import os

class AnomalyDetector:
    def __init__(self):
        self.isolation_forest = None
        self.scaler_mean = None
        self.scaler_std = None
        
    def train_models(self, data):
        # Normalize data
        self.scaler_mean = np.mean(data, axis=0)
        self.scaler_std = np.std(data, axis=0)
        normalized_data = (data - self.scaler_mean) / (self.scaler_std + 1e-8)
        
        # Train isolation forest
        self.isolation_forest = IsolationForest(contamination=0.15, random_state=42)
        self.isolation_forest.fit(normalized_data)
        
    def predict(self, vitals):
        # vitals: [heart_rate, spo2, temperature, bp_systolic, bp_diastolic]
        vitals_array = np.array(vitals).reshape(1, -1)
        
        if self.scaler_mean is None:
            return 0.5, 'MEDIUM'
        
        normalized = (vitals_array - self.scaler_mean) / (self.scaler_std + 1e-8)
        
        # Isolation forest score (convert to 0-1 range)
        if_score = self.isolation_forest.score_samples(normalized)[0]
        anomaly_score = float(np.clip(-if_score, 0, 1))
        
        # Determine severity
        if anomaly_score < 0.3:
            severity = 'LOW'
        elif anomaly_score < 0.6:
            severity = 'MEDIUM'
        else:
            severity = 'HIGH'
            
        return anomaly_score, severity
    
    def save_models(self, path='models'):
        os.makedirs(path, exist_ok=True)
        if self.isolation_forest:
            with open(f'{path}/isolation_forest.pkl', 'wb') as f:
                pickle.dump(self.isolation_forest, f)
        np.save(f'{path}/scaler_mean.npy', self.scaler_mean)
        np.save(f'{path}/scaler_std.npy', self.scaler_std)
    
    def load_models(self, path='models'):
        try:
            with open(f'{path}/isolation_forest.pkl', 'rb') as f:
                self.isolation_forest = pickle.load(f)
            self.scaler_mean = np.load(f'{path}/scaler_mean.npy')
            self.scaler_std = np.load(f'{path}/scaler_std.npy')
            return True
        except:
            return False
