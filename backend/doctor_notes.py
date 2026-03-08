from datetime import datetime

class DoctorNotesSystem:
    def __init__(self):
        self.notes = []
        self.note_id_counter = 1
    
    def add_note(self, patient_id, doctor_name, note_text, note_type='OBSERVATION'):
        """Add a clinical note"""
        note = {
            'id': self.note_id_counter,
            'patient_id': patient_id,
            'doctor_name': doctor_name,
            'note_text': note_text,
            'note_type': note_type,  # OBSERVATION, DIAGNOSIS, TREATMENT, FOLLOW_UP
            'timestamp': datetime.utcnow().isoformat(),
            'edited': False
        }
        
        self.notes.insert(0, note)
        self.note_id_counter += 1
        
        print(f"📝 Note added by Dr. {doctor_name} for {patient_id}: {note_text[:50]}...")
        
        return note
    
    def get_patient_notes(self, patient_id, limit=20):
        """Get notes for a specific patient"""
        patient_notes = [n for n in self.notes if n['patient_id'] == patient_id]
        return patient_notes[:limit]
    
    def get_all_notes(self, limit=50):
        """Get all recent notes"""
        return self.notes[:limit]
    
    def update_note(self, note_id, new_text):
        """Update an existing note"""
        for note in self.notes:
            if note['id'] == note_id:
                note['note_text'] = new_text
                note['edited'] = True
                note['last_edited'] = datetime.utcnow().isoformat()
                return True
        return False

# Global instance
doctor_notes_system = DoctorNotesSystem()
