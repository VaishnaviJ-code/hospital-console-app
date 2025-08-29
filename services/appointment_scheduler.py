from datetime import datetime, date

import pymysql

class AppointmentScheduler:
    def __init__(self):
        self.appointment_counts = {}  # {doctor_id: count}
        self.last_reset_date = date.today()

    def sync_with_database(self):
        """Load existing appointment counts from database on startup"""
        from dao.receptionist_implementation import ReceptionistDaoImplementation
        dao = ReceptionistDaoImplementation()
        
        try:
            today = date.today().strftime('%Y-%m-%d')
            
            # Get all doctors
            cursor = dao.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT doctor_id FROM doctors")
            doctors = cursor.fetchall()
            cursor.close()
            
            # Load existing counts from database
            for doctor in doctors:
                doctor_id = doctor['doctor_id']
                db_count = dao.get_daily_appointment_count_from_db(doctor_id, today)
                self.appointment_counts[doctor_id] = db_count
            
            print(f"Loaded existing appointment counts from database")
            for doctor_id, count in self.appointment_counts.items():
                if count > 0:
                    print(f"   Dr. {doctor_id}: {count}/25 appointments")
            
        except Exception as e:
            print(f"Error syncing with database: {e}")

    def reset_if_new_day(self):
        """Reset appointment counts if it's a new day"""
        today = date.today()
        if self.last_reset_date != today:
            print(f"Resetting appointment counts for new day: {today}")
            self.appointment_counts.clear()
            self.last_reset_date = today
            self.sync_with_database()

    def get_appointment_count(self, doctor_id, appointment_date=None):
        """Get current appointment count for a doctor"""
        self.reset_if_new_day()
        if appointment_date is None:
            appointment_date = date.today()
        elif isinstance(appointment_date, datetime):
            appointment_date = appointment_date.date()
        
        # For today's appointments, return in-memory count
        if appointment_date == date.today():
            return self.appointment_counts.get(doctor_id, 0)
        else:
            return 0  # Future appointments don't count toward today's limit

    def can_book_appointment(self, doctor_id, appointment_date=None):
        """Check if doctor can take more appointments"""
        self.reset_if_new_day()
        
        # If appointment is for a different day, allow booking
        if appointment_date and isinstance(appointment_date, datetime):
            if appointment_date.date() != date.today():
                return True  # Future appointments are always allowed
        
        current_count = self.appointment_counts.get(doctor_id, 0)
        return current_count < 25

    def book_appointment(self, doctor_id, appointment_date=None):
        
        if not self.can_book_appointment(doctor_id, appointment_date):
            return False
        
        # Only count appointments for today
        if appointment_date and isinstance(appointment_date, datetime):
            if appointment_date.date() != date.today():
                return True  # Don't count future appointments in today's limit
        
        self.appointment_counts[doctor_id] = self.appointment_counts.get(doctor_id, 0) + 1
        return True

    def get_availability_status(self, doctor_id, appointment_date=None):
        """Get availability status directly from DATABASE"""
        from dao.receptionist_implementation import ReceptionistDaoImplementation
        
        # Always create fresh DAO instance
        dao = ReceptionistDaoImplementation()
        
        if appointment_date is None:
            appointment_date = date.today().strftime('%Y-%m-%d')
        elif isinstance(appointment_date, datetime):
            appointment_date = appointment_date.strftime('%Y-%m-%d')
        
        # get fresh count from database every time
        current_count = dao.get_daily_appointment_count_from_db(doctor_id, appointment_date)
        max_appointments = 25
        
        return {
            'doctor_id': doctor_id,
            'date': appointment_date,
            'current_appointments': current_count,
            'max_appointments': max_appointments,
            'available_slots': max_appointments - current_count,
            'is_available': current_count < max_appointments,
            'availability_percentage': round((current_count / max_appointments) * 100, 1)
        }

# Global instance
appointment_scheduler = AppointmentScheduler()
