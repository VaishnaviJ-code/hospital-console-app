from datetime import datetime, date
from typing import Dict, Optional
import pymysql

class TokenManager:
    """Manages appointment tokens (1-25) per doctor per day with database integration"""
    
    def __init__(self):
        self.token_counts = {}  # In-memory cache for performance
        self.current_date = date.today()
        self.max_tokens_per_doctor = 25
    
    def reset_if_new_day(self):
        """Reset token counts if it's a new day"""
        today = date.today()
        if today != self.current_date:
            print(f"🔄 Resetting token counts for new day: {today}")
            self.token_counts.clear()
            self.current_date = today
    
    def get_next_available_token(self, doctor_id: str, appointment_date: datetime) -> int:
        """Get next available token (1-25) for doctor on specific date from DATABASE"""
        try:
            from dao.receptionist_implementation import ReceptionistDaoImplementation
            dao = ReceptionistDaoImplementation()
            
            # Get date string
            if isinstance(appointment_date, datetime):
                date_str = appointment_date.strftime('%Y-%m-%d')
            else:
                date_str = str(appointment_date)[:10]
            
            # Query existing tokens for this doctor on this date
            cursor = dao.conn.cursor()
            cursor.execute("""
                SELECT token FROM appointments 
                WHERE doctor_id = %s 
                AND DATE(appointment_date) = %s
                AND status NOT IN ('Cancelled', 'No-show')
                ORDER BY token
            """, (doctor_id, date_str))
            
            used_tokens = {row[0] for row in cursor.fetchall()}
            cursor.close()
            
            # Find next available token (1-25)
            for token in range(1, self.max_tokens_per_doctor + 1):
                if token not in used_tokens:
                    return token
            
            # All tokens used
            return -1
            
        except Exception as e:
            print(f"Error getting next token: {e}")
            return -1
    
    def is_doctor_available(self, doctor_id: str, appointment_date: datetime) -> bool:
        """Check if doctor has available tokens for the date"""
        return self.get_next_available_token(doctor_id, appointment_date) != -1
    
    def get_current_token_count(self, doctor_id: str, appointment_date: datetime = None) -> int:
        """Get current number of tokens used for doctor on specific date"""
        try:
            from dao.receptionist_implementation import ReceptionistDaoImplementation
            dao = ReceptionistDaoImplementation()
            
            if appointment_date is None:
                appointment_date = datetime.now()
            
            date_str = appointment_date.strftime('%Y-%m-%d')
            
            cursor = dao.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as token_count
                FROM appointments 
                WHERE doctor_id = %s 
                AND DATE(appointment_date) = %s
                AND status NOT IN ('Cancelled', 'No-show')
            """, (doctor_id, date_str))
            
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result else 0
            
        except Exception as e:
            print(f"Error getting token count: {e}")
            return 0
    
    def get_availability_status(self, doctor_id: str, appointment_date: datetime = None) -> dict:
        """Get detailed availability status for a doctor on specific date"""
        if appointment_date is None:
            appointment_date = datetime.now()
        
        current_count = self.get_current_token_count(doctor_id, appointment_date)
        
        return {
            'doctor_id': doctor_id,
            'date': appointment_date.strftime('%Y-%m-%d'),
            'current_appointments': current_count,
            'max_appointments': self.max_tokens_per_doctor,
            'available_slots': self.max_tokens_per_doctor - current_count,
            'is_available': current_count < self.max_tokens_per_doctor,
            'availability_percentage': round((current_count / self.max_tokens_per_doctor) * 100, 1)
        }
    
    def sync_with_database(self):
        """Sync in-memory counts with database on startup"""
        try:
            from dao.receptionist_implementation import ReceptionistDaoImplementation
            dao = ReceptionistDaoImplementation()
            
            today = date.today().strftime('%Y-%m-%d')
            cursor = dao.conn.cursor(pymysql.cursors.DictCursor)
            
            # Get token counts for all doctors for today
            cursor.execute("""
                SELECT doctor_id, COUNT(*) as token_count
                FROM appointments 
                WHERE DATE(appointment_date) = %s
                AND status NOT IN ('Cancelled', 'No-show')
                GROUP BY doctor_id
            """, (today,))
            
            results = cursor.fetchall()
            cursor.close()
            
            # Update in-memory counts
            for row in results:
                self.token_counts[row['doctor_id']] = row['token_count']
            
            print(f"✅ Synced token counts with database for {len(results)} doctors")
            
        except Exception as e:
            print(f"❌ Error syncing tokens with database: {e}")
    
    def get_doctor_tokens_for_date(self, doctor_id: str, appointment_date: datetime) -> list:
        """Get list of all tokens assigned to doctor on specific date"""
        try:
            from dao.receptionist_implementation import ReceptionistDaoImplementation
            dao = ReceptionistDaoImplementation()
            
            date_str = appointment_date.strftime('%Y-%m-%d')
            cursor = dao.conn.cursor()
            cursor.execute("""
                SELECT token, patient_id, appointment_id 
                FROM appointments 
                WHERE doctor_id = %s 
                AND DATE(appointment_date) = %s
                AND status NOT IN ('Cancelled', 'No-show')
                ORDER BY token
            """, (doctor_id, date_str))
            
            tokens = cursor.fetchall()
            cursor.close()
            
            return [{'token': row[0], 'patient_id': row[1], 'appointment_id': row[2]} for row in tokens]
            
        except Exception as e:
            print(f"Error getting doctor tokens: {e}")
            return []

# Global instance
token_manager = TokenManager()
