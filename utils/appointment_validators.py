from datetime import datetime, date, time
from typing import Dict, Any, List

class AppointmentValidator:
    """
    Validator class for appointment data validation.
    Handles all appointment-related validation logic.
    """
    
    # Valid appointment statuses
    VALID_STATUSES = ['scheduled', 'confirmed', 'completed', 'cancelled', 'no-show', 'rescheduled']
    
    # Working hours (24-hour format)
    WORKING_HOURS_START = 9  # 9:00 AM
    WORKING_HOURS_END = 18   # 6:00 PM
    
    @staticmethod
    def validate_appointment_data(appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate complete appointment data dictionary.
        
        :param appointment_data: Dictionary containing appointment information
        :return: Validation result with success status and error messages
        """
        errors = []
        
        # Check required fields
        required_fields = ['patient_id', 'doctor_id', 'appointment_date']
        for field in required_fields:
            if field not in appointment_data or appointment_data[field] is None:
                errors.append(f"{field.replace('_', ' ').title()} is required")
        
        if errors:
            return {
                "valid": False,
                "errors": errors
            }
        
        # Validate individual fields
        patient_id_validation = AppointmentValidator.validate_patient_id(appointment_data['patient_id'])
        if not patient_id_validation['valid']:
            errors.extend(patient_id_validation['errors'])
        
        doctor_id_validation = AppointmentValidator.validate_doctor_id(appointment_data['doctor_id'])
        if not doctor_id_validation['valid']:
            errors.extend(doctor_id_validation['errors'])
        
        date_validation = AppointmentValidator.validate_appointment_date(appointment_data['appointment_date'])
        if not date_validation['valid']:
            errors.extend(date_validation['errors'])
        
        # Validate optional fields if present
        if 'token' in appointment_data and appointment_data['token'] is not None:
            token_validation = AppointmentValidator.validate_token(appointment_data['token'])
            if not token_validation['valid']:
                errors.extend(token_validation['errors'])
        
        if 'status' in appointment_data and appointment_data['status']:
            status_validation = AppointmentValidator.validate_status(appointment_data['status'])
            if not status_validation['valid']:
                errors.extend(status_validation['errors'])
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_patient_id(patient_id: Any) -> Dict[str, Any]:
        """Validate patient ID."""
        errors = []
        
        if patient_id is None:
            errors.append("Patient ID is required")
        # elif not isinstance(patient_id, str):
        #     errors.append("Patient ID must be an integer")
        # else:
        #     errors.append("Invalid Patient ID")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_doctor_id(doctor_id: Any) -> Dict[str, Any]:
        """Validate doctor ID."""
        errors = []
        
        if doctor_id is None:
            errors.append("Doctor ID is required")
        # elif not isinstance(doctor_id, str):
        #     errors.append("Doctor ID must be an integer")
        # else:
        #     errors.append("Invalid doctor id")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_appointment_date(appointment_date: Any) -> Dict[str, Any]:
        """Validate appointment date and time."""
        errors = []
        
        if appointment_date is None:
            errors.append("Appointment date is required")
            return {"valid": False, "errors": errors}
        
        try:
            # Handle different input types
            if isinstance(appointment_date, str):
                # Try parsing different date formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']:
                    try:
                        parsed_date = datetime.strptime(appointment_date, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    errors.append("Invalid date format. Use YYYY-MM-DD HH:MM:SS or YYYY-MM-DD")
                    return {"valid": False, "errors": errors}
            elif isinstance(appointment_date, datetime):
                parsed_date = appointment_date
            else:
                errors.append("Invalid date type")
                return {"valid": False, "errors": errors}
            
            # Check if appointment is not in the past (allow same day)
            if parsed_date.date() < date.today():
                errors.append("Appointment date cannot be in the past")
            
            # Check if appointment is within reasonable future (1 year)
            days_ahead = (parsed_date.date() - date.today()).days
            if days_ahead > 365:
                errors.append("Appointment cannot be scheduled more than 1 year in advance")
            
            # Check working hours if time is specified
            if parsed_date.time() != time.min:  # If time is not 00:00:00
                hour = parsed_date.hour
                if hour < AppointmentValidator.WORKING_HOURS_START or hour >= AppointmentValidator.WORKING_HOURS_END:
                    errors.append(f"Appointment must be between {AppointmentValidator.WORKING_HOURS_START}:00 AM and {AppointmentValidator.WORKING_HOURS_END}:00 PM")
            
            # Check if it's not a weekend (assuming Saturday=5, Sunday=6)
            if parsed_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                errors.append("Appointments cannot be scheduled on weekends")
                
        except Exception as e:
            errors.append(f"Invalid appointment date: {str(e)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_token(token: Any) -> Dict[str, Any]:
        """Validate appointment token number."""
        errors = []
        
        if not isinstance(token, int):
            errors.append("Token must be an integer")
        elif token <= 0:
            errors.append("Token must be a positive integer")
        elif token > 999:
            errors.append("Token cannot exceed 999")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_status(status: str) -> Dict[str, Any]:
        """Validate appointment status."""
        errors = []
        
        if not status:
            errors.append("Status cannot be empty")
        elif status.lower().strip() not in AppointmentValidator.VALID_STATUSES:
            errors.append(f"Status must be one of: {', '.join(AppointmentValidator.VALID_STATUSES)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_appointment_time_slot(appointment_date: datetime, duration_minutes: int = 30) -> Dict[str, Any]:
        """
        Validate if appointment time slot is available (basic time slot validation).
        
        :param appointment_date: Appointment datetime
        :param duration_minutes: Appointment duration in minutes
        :return: Validation result
        """
        errors = []
        
        # Check if appointment starts on valid time slots (every 30 minutes)
        if appointment_date.minute not in [0, 30]:
            errors.append("Appointments must start at :00 or :30 minutes")
        
        # Check appointment duration
        if duration_minutes <= 0:
            errors.append("Appointment duration must be positive")
        elif duration_minutes > 240:  # 4 hours max
            errors.append("Appointment duration cannot exceed 4 hours")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
