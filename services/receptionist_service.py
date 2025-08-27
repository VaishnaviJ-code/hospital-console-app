# Business logic / core features like "book appointment", "dispense medicine"
# create files according to your role and push

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from dao.abstract_receptionist import ReceptionistBase
from dao.receptionist_implementation import ReceptionistDaoImplementation
from models.patient import Patient
from models.appointment import Appointments
from utils.patient_validators import PatientValidator
from utils.appointment_validators import AppointmentValidator


class ReceptionistService:
    """
    Service layer for Receptionist operations.
    Handles business logic and coordinates with DAO layer using dedicated validators.
    """
    
    def __init__(self):
        self.receptionist_dao = ReceptionistDaoImplementation()
    
    dao_services: ReceptionistBase = ReceptionistDaoImplementation()
    
    # ---------------- PATIENT SERVICES ----------------
    
    def register_new_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new patient with validation.
        
        :param patient_data: Patient information dictionary
        :return: Result dictionary with success status and patient_id or error message
        """
        # Validate patient data using PatientValidator
        validation_result = PatientValidator.validate_patient_data(patient_data)
        if not validation_result["valid"]:
            return {
                "success": False,
                "message": "Validation failed: " + "; ".join(validation_result["errors"]),
                "patient_id": None,
                "errors": validation_result["errors"]
            }
        
        # Check if patient already exists by phone
        existing_patient = self.receptionist_dao.search_patient_by_phone(patient_data["phone"])
        if existing_patient:
            return {
                "success": False,
                "message": f"Patient with phone number {patient_data['phone']} already exists",
                "patient_id": existing_patient.get_patient_id(),
                "errors": ["Phone already registered"]
            }
        
        # Add patient to database
        try:
            result = self.receptionist_dao.add_patient(patient_data)
            if result and result != -1 and isinstance(result, str) and result.startswith("PAT"):
                return {
                    "success": True,
                    "message": "Patient registered successfully",
                    "patient_id": result,
                    "errors": []
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to register patient. Database error occurred.",
                    "patient_id": None,
                    "errors": ["Database insertion failed"]
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error registering patient: {str(e)}",
                "patient_id": None,
                "errors": [str(e)]
            }
    
    def update_patient_details(self, patient_id: str, field: str, new_value: str) -> Dict[str, Any]:
        """
        Update specific patient field with validation.
        
        :param patient_id: Patient ID to update (PAT####)
        :param field: Field name ('name', 'address', 'phone')
        :param new_value: New value for the field
        :return: Result dictionary with success status and message
        """
        # Validate patient ID format
        if not patient_id or not isinstance(patient_id, str) or not patient_id.startswith("PAT"):
            return {
                "success": False,
                "message": "Invalid patient ID format. Expected format: PAT####",
                "errors": ["Invalid patient ID"]
            }
        
        # Check if patient exists
        patient = self.receptionist_dao.search_patient_by_id(patient_id)
        if not patient:
            return {
                "success": False,
                "message": f"Patient with ID {patient_id} not found",
                "errors": ["Patient not found"]
            }
        
        # Validate the new value based on field type using PatientValidator
        validation_result = None
        if field == "name":
            validation_result = PatientValidator.validate_name(new_value)
        elif field == "address":
            validation_result = PatientValidator.validate_address(new_value)
        elif field == "phone":
            validation_result = PatientValidator.validate_phone(new_value)
        else:
            return {
                "success": False,
                "message": f"Invalid field '{field}'. Allowed fields: name, address, phone",
                "errors": ["Invalid field name"]
            }
        
        if not validation_result["valid"]:
            return {
                "success": False,
                "message": "Validation failed: " + "; ".join(validation_result["errors"]),
                "errors": validation_result["errors"]
            }
        
        # Check for duplicate phone if updating phone
        if field == "phone":
            existing_patient = self.receptionist_dao.search_patient_by_phone(new_value)
            if existing_patient and existing_patient.get_patient_id() != patient_id:
                return {
                    "success": False,
                    "message": f"Phone number {new_value} is already registered to another patient",
                    "errors": ["Phone number already exists"]
                }
        
        # Update the field
        try:
            success = False
            if field == "name":
                success = self.receptionist_dao.update_patient_name(patient_id, new_value)
            elif field == "address":
                success = self.receptionist_dao.update_patient_address(patient_id, new_value)
            elif field == "phone":
                success = self.receptionist_dao.update_patient_phone(patient_id, new_value)
            
            if success:
                return {
                    "success": True,
                    "message": f"Patient {field} updated successfully",
                    "errors": []
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to update patient {field}. No changes made.",
                    "errors": ["Database update failed"]
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating patient {field}: {str(e)}",
                "errors": [str(e)]
            }
    
    def find_patient(self, search_type: str, search_value: Any) -> Dict[str, Any]:
        """
        Find patient by ID or phone number.
        
        :param search_type: 'id' or 'phone'
        :param search_value: Patient ID (PAT####) or phone number
        :return: Result with patient data or error message
        """
        try:
            patient = None
            
            if search_type == "id":
                # Validate patient ID format
                if not search_value or not isinstance(search_value, str) or not search_value.startswith("PAT"):
                    return {
                        "success": False,
                        "message": "Invalid patient ID format. Expected format: PAT####",
                        "patient": None,
                        "errors": ["Invalid patient ID format"]
                    }
                patient = self.receptionist_dao.search_patient_by_id(search_value)
                
            elif search_type == "phone":
                # Validate phone using PatientValidator
                phone_validation = PatientValidator.validate_phone(str(search_value))
                if not phone_validation["valid"]:
                    return {
                        "success": False,
                        "message": "Invalid phone number format",
                        "patient": None,
                        "errors": phone_validation["errors"]
                    }
                patient = self.receptionist_dao.search_patient_by_phone(str(search_value))
            
            else:
                return {
                    "success": False,
                    "message": "Invalid search type. Use 'id' or 'phone'",
                    "patient": None,
                    "errors": ["Invalid search type"]
                }
            
            if patient:
                return {
                    "success": True,
                    "message": "Patient found",
                    "patient": patient,
                    "errors": []
                }
            else:
                return {
                    "success": False,
                    "message": f"No patient found with {search_type}: {search_value}",
                    "patient": None,
                    "errors": ["Patient not found"]
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching for patient: {str(e)}",
                "patient": None,
                "errors": [str(e)]
            }
    
    def get_all_patients(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all patients from the database and display them.
        
        :param limit: Optional limit for number of patients to return
        :return: Result with list of patients
        """
        try:
            patients = ReceptionistService.dao_services.list_patients()
            
            # Apply limit if specified
            if limit and isinstance(limit, int) and limit > 0:
                patients = patients[:limit]
            
            # Display patients
            if patients:
                print(f"\n=== Found {len(patients)} Patients ===")
                for patient in patients:
                    print(patient)
            else:
                print("No patients found in the database.")
            
            return {
                "success": True,
                "message": f"Found {len(patients)} patients",
                "patients": patients,
                "count": len(patients),
                "errors": []
            }
            
        except Exception as e:
            print(f"Error retrieving patients: {str(e)}")
            return {
                "success": False,
                "message": f"Error retrieving patients: {str(e)}",
                "patients": [],
                "count": 0,
                "errors": [str(e)]
            }
    
    # ---------------- APPOINTMENT SERVICES ----------------
    
    def schedule_appointment(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule a new appointment with validation.
        
        :param appointment_data: Appointment details
        :return: Result dictionary with success status and appointment_id
        """
        # Validate appointment data using AppointmentValidator
        validation_result = AppointmentValidator.validate_appointment_data(appointment_data)
        if not validation_result["valid"]:
            return {
                "success": False,
                "message": "Validation failed: " + "; ".join(validation_result["errors"]),
                "appointment_id": None,
                "token": None,
                "errors": validation_result["errors"]
            }
        
        # Check if patient exists
        patient = self.receptionist_dao.search_patient_by_id(appointment_data["patient_id"])
        if not patient:
            return {
                "success": False,
                "message": f"Patient with ID {appointment_data['patient_id']} not found",
                "appointment_id": None,
                "token": None,
                "errors": ["Patient not found"]
            }
        
        # Generate token if not provided
        if "token" not in appointment_data or not appointment_data["token"]:
            appointment_data["token"] = self._generate_token()
        
        # Set default status if not provided
        if "status" not in appointment_data:
            appointment_data["status"] = "Scheduled"
        
        # Set appointment date to now if not provided
        if "appointment_date" not in appointment_data or not appointment_data["appointment_date"]:
            appointment_data["appointment_date"] = datetime.now()
        
        # Schedule the appointment
        try:
            appointment_id = self.receptionist_dao.book_appointment(appointment_data)
            if appointment_id and appointment_id != -1 and isinstance(appointment_id, str) and appointment_id.startswith("APT"):
                
                appointment_details = self.receptionist_dao.get_appointment_with_fee(appointment_id)
                
                if appointment_details:
                    # Display appointment confirmation with fee
                    self._display_appointment_confirmation(appointment_details)
                
                return {
                    "success": True,
                    "message": "Appointment scheduled successfully",
                    "appointment_id": appointment_id,
                    "token": appointment_data["token"],
                    "errors": []
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to schedule appointment. Database error occurred.",
                    "appointment_id": None,
                    "token": None,
                    "errors": ["Database insertion failed"]
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error scheduling appointment: {str(e)}",
                "appointment_id": None,
                "token": None,
                "errors": [str(e)]
            }
    
    def find_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """
        Find appointment by ID.
        
        :param appointment_id: Appointment ID (APT####)
        :return: Result with appointment data
        """
        # Validate appointment ID format
        if not appointment_id or not isinstance(appointment_id, str) or not appointment_id.startswith("APT"):
            return {
                "success": False,
                "message": "Invalid appointment ID format. Expected format: APT####",
                "appointment": None,
                "errors": ["Invalid appointment ID format"]
            }
        
        try:
            appointment = self.receptionist_dao.search_appointment_by_id(appointment_id)
            if appointment:
                return {
                    "success": True,
                    "message": "Appointment found",
                    "appointment": appointment,
                    "errors": []
                }
            else:
                return {
                    "success": False,
                    "message": f"No appointment found with ID: {appointment_id}",
                    "appointment": None,
                    "errors": ["Appointment not found"]
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching for appointment: {str(e)}",
                "appointment": None,
                "errors": [str(e)]
            }
    
    def get_all_appointments(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all appointments from the database.
        
        :param limit: Optional limit for number of appointments to return
        :return: Result with list of appointments
        """
        try:
            appointments = self.receptionist_dao.list_appointments()
            
            # Apply limit if specified
            if limit and isinstance(limit, int) and limit > 0:
                appointments = appointments[:limit]
            
            # Display appointments
            if appointments:
                print(f"\n=== Found {len(appointments)} Appointments ===")
                for appointment in appointments:
                    print(appointment)
            else:
                print("No appointments found in the database.")
            
            return {
                "success": True,
                "message": f"Found {len(appointments)} appointments",
                "appointments": appointments,
                "count": len(appointments),
                "errors": []
            }
        except Exception as e:
            print(f"Error retrieving appointments: {str(e)}")
            return {
                "success": False,
                "message": f"Error retrieving appointments: {str(e)}",
                "appointments": [],
                "count": 0,
                "errors": [str(e)]
            }
    
    def get_appointments_by_date(self, target_date: str) -> Dict[str, Any]:
        """
        Get appointments for a specific date.
        
        :param target_date: Date in YYYY-MM-DD format
        :return: Result with filtered appointments
        """
        # Validate date format
        try:
            parsed_date = datetime.strptime(target_date, '%Y-%m-%d')
        except ValueError:
            return {
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DD",
                "appointments": [],
                "errors": ["Invalid date format"]
            }
        
        try:
            all_appointments = self.receptionist_dao.list_appointments()
            filtered_appointments = []
            
            for appointment in all_appointments:
                appt_date = appointment.get_appointment_date()
                if isinstance(appt_date, datetime):
                    appt_date_str = appt_date.strftime('%Y-%m-%d')
                elif isinstance(appt_date, str):
                    appt_date_str = appt_date[:10]  # Take first 10 characters (YYYY-MM-DD)
                else:
                    continue  # Skip if date format is unknown
                
                if appt_date_str == target_date:
                    filtered_appointments.append(appointment)
            
            return {
                "success": True,
                "message": f"Found {len(filtered_appointments)} appointments for {target_date}",
                "appointments": filtered_appointments,
                "date": target_date,
                "count": len(filtered_appointments),
                "errors": []
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving appointments: {str(e)}",
                "appointments": [],
                "errors": [str(e)]
            }
    
    def get_appointments_by_patient(self, patient_id: str) -> Dict[str, Any]:
        """
        Get all appointments for a specific patient.
        
        :param patient_id: Patient ID (PAT####)
        :return: Result with patient's appointments
        """
        # Validate patient ID format
        if not patient_id or not isinstance(patient_id, str) or not patient_id.startswith("PAT"):
            return {
                "success": False,
                "message": "Invalid patient ID format. Expected format: PAT####",
                "appointments": [],
                "errors": ["Invalid patient ID format"]
            }
        
        # Check if patient exists
        patient = self.receptionist_dao.search_patient_by_id(patient_id)
        if not patient:
            return {
                "success": False,
                "message": f"Patient with ID {patient_id} not found",
                "appointments": [],
                "errors": ["Patient not found"]
            }
        
        try:
            all_appointments = self.receptionist_dao.list_appointments()
            patient_appointments = [
                appt for appt in all_appointments 
                if appt.get_patient_id() == patient_id
            ]
            
            return {
                "success": True,
                "message": f"Found {len(patient_appointments)} appointments for patient {patient_id}",
                "appointments": patient_appointments,
                "patient_id": patient_id,
                "count": len(patient_appointments),
                "errors": []
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving patient appointments: {str(e)}",
                "appointments": [],
                "errors": [str(e)]
            }
    
    def cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """
        Cancel an appointment by updating its status.
        
        :param appointment_id: Appointment ID (APT####) to cancel
        :return: Result with success status
        """
        # Find the appointment first
        appointment_result = self.find_appointment(appointment_id)
        if not appointment_result["success"]:
            return appointment_result
        
        appointment = appointment_result["appointment"]
        
        # Check if appointment is already cancelled
        if appointment.get_status().lower() == "cancelled":
            return {
                "success": False,
                "message": "Appointment is already cancelled",
                "errors": ["Appointment already cancelled"]
            }
        
        # Update appointment status to cancelled
        try:
            appointment.set_status("Cancelled")
            return {
                "success": True,
                "message": f"Appointment {appointment_id} cancelled successfully",
                "appointment_id": appointment_id,
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error cancelling appointment: {str(e)}",
                "errors": [str(e)]
            }
    
    # ---------------- UTILITY METHODS ----------------
    
    def _generate_token(self) -> int:
        """Generate a unique token number for appointments."""
        import random
        # Generate token between 100-999
        token = random.randint(100, 999)
        # In production, you might want to check for uniqueness within the day
        return token
    
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """
        Get comprehensive patient information including appointments.
        
        :param patient_id: Patient ID (PAT####)
        :return: Combined patient and appointment data
        """
        # Get patient details
        patient_result = self.find_patient("id", patient_id)
        if not patient_result["success"]:
            return patient_result
        
        # Get patient appointments
        appointments_result = self.get_appointments_by_patient(patient_id)
        
        return {
            "success": True,
            "message": f"Patient summary retrieved for ID {patient_id}",
            "patient": patient_result["patient"],
            "appointments": appointments_result["appointments"],
            "appointment_count": appointments_result["count"],
            "errors": []
        }
    
    def _display_appointment_confirmation(self, appointment_details: Dict):
        """Display appointment confirmation with consultation fee"""
        print("\n" + "=" * 50)
        print("APPOINTMENT CONFIRMATION".center(50))
        print("=" * 50)
        print(f"Appointment ID    : {appointment_details['appointment_id']}")
        print(f"Patient ID        : {appointment_details['patient_id']}")
        print(f"Doctor ID         : {appointment_details['doctor_id']}")
        print(f"Token Number      : {appointment_details['token']}")
        print(f"Status            : {appointment_details['status']}")
        print(f"Appointment Date  : {appointment_details['appointment_date']}")
        print(f"Consultation Fee  : ₹{appointment_details['consultation_fee']:.2f}")
        print("=" * 50)
        print("Please make note of your token number and appointment ID.")
        print("=" * 50)

