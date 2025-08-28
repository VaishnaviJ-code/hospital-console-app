# Business logic / core features like "book appointment", "dispense medicine"
# create files according to your role and push

from typing import List, Optional, Dict, Any
from datetime import datetime, date

import pymysql
from dao.abstract_receptionist import ReceptionistBase
from dao.receptionist_implementation import ReceptionistDaoImplementation
from models.patient import Patient
from models.appointment import Appointments
from services.appointment_scheduler import appointment_scheduler
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
        if "dob" in patient_data and patient_data["dob"]:
            dob_input = patient_data["dob"]
            try:
                # Try to parse as DD/MM/YYYY first
                if "/" in dob_input:
                    parsed_date = datetime.strptime(dob_input, "%d/%m/%Y")
                    patient_data["dob"] = parsed_date.strftime("%Y-%m-%d")  # Convert to MySQL format
                # If already in YYYY-MM-DD format, keep as is
                elif "-" in dob_input:
                    # Validate it's correct YYYY-MM-DD format
                    datetime.strptime(dob_input, "%Y-%m-%d")
                    # Keep as is
            except ValueError:
                return {
                    "success": False,
                    "message": "Invalid date format. Please use DD/MM/YYYY",
                    "patient_id": None,
                    "errors": ["Invalid date format"]
                }
        
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
                print("\n" + "=" * 120)
                print("ALL PATIENTS".center(120))
                print("=" * 120)
                print(f"{'ID':<10} {'Name':<20} {'DOB':<12} {'Gender':<8} {'Phone':<12} {'Address':<25} {'Email':<20} {'Registered':<12}")
                print("-" * 120)
                
                for patient in patients:
                    # Format registration date
                    reg_date = patient.get_registration_date()
                    if isinstance(reg_date, datetime):
                        reg_date_str = reg_date.strftime('%Y-%m-%d')
                    else:
                        reg_date_str = str(reg_date)[:10] if reg_date else "N/A"
                    
                    # Truncate long fields to fit columns
                    name = patient.get_patient_name()[:19] if patient.get_patient_name() else "N/A"
                    address = patient.get_address()[:24] if patient.get_address() else "N/A"
                    email = patient.get_email()[:19] if patient.get_email() else "N/A"
                    
                    print(f"{patient.get_patient_id():<10} {name:<20} {patient.get_dob():<12} {patient.get_gender():<8} {patient.get_phone():<12} {address:<25} {email:<20} {reg_date_str:<12}")
                
                print("=" * 120)
                print(f"Total Patients: {len(patients)}")
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
        # ✅ Initialize variables to avoid UnboundLocalError
        token = None
        appointment_id = None
        
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
        
        doctor_id = appointment_data["doctor_id"]
        appointment_date = appointment_data["appointment_date"]

        # ✅ Generate token automatically (1-25 per doctor per day)
        from services.token_manager import token_manager
        
        token = token_manager.get_next_available_token(doctor_id, appointment_date)
        
        if token == -1:
            date_str = appointment_date.strftime('%d/%m/%Y') if isinstance(appointment_date, datetime) else str(appointment_date)
            return {
                "success": False,
                "message": f"❌ Doctor {doctor_id} is fully booked for {date_str}! (25/25 tokens assigned)",
                "appointment_id": None,
                "token": None,
                "errors": ["Doctor fully booked"]
            }
        
        # ✅ Assign the token to appointment
        appointment_data["token"] = token
        
        # Set default status
        if "status" not in appointment_data:
            appointment_data["status"] = "Scheduled"

        # Schedule the appointment
        try:
            appointment_id = self.receptionist_dao.book_appointment(appointment_data)
            
            if appointment_id and appointment_id != -1:
                # Generate consultation bill
                bill_result = self._generate_consultation_bill(appointment_data, appointment_id)
                
                appointment_details = self.receptionist_dao.get_appointment_with_fee(appointment_id)
                if appointment_details:
                    self._display_appointment_confirmation(appointment_details)
                
                # Display the bill if generated successfully
                if bill_result['success']:
                    print("\n" + bill_result['bill_display'])
                
                return {
                    "success": True,
                    "message": f"✅ Appointment scheduled successfully! Token #{token} assigned to Dr. {doctor_id}",
                    "appointment_id": appointment_id,
                    "token": token,
                    "bill": bill_result.get('bill_data', None),
                    "errors": []
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to schedule appointment. Database error occurred.",
                    "appointment_id": None,
                    "token": token,
                    "errors": ["Database insertion failed"]
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error scheduling appointment: {str(e)}",
                "appointment_id": appointment_id,
                "token": token,
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
                print("\n" + "=" * 100)
                print("ALL APPOINTMENTS".center(100))
                print("=" * 100)
                print(f"{'ID':<12} {'Patient ID':<12} {'Doctor ID':<12} {'Token':<8} {'Status':<12} {'Date & Time':<20} {'Fee':<10}")
                print("-" * 100)
                
                for appointment in appointments:
                    # Format appointment date
                    appt_date = appointment.get_appointment_date()
                    if isinstance(appt_date, datetime):
                        date_str = appt_date.strftime('%Y-%m-%d %H:%M')
                    else:
                        date_str = str(appt_date)[:16] if appt_date else "N/A"
                    
                    # Get consultation fee (if available from joined query)
                    fee = self._get_consultation_fee(appointment.get_doctor_id())
                    
                    print(f"{appointment.get_appointment_id():<12} {appointment.get_patient_id():<12} {appointment.get_doctor_id():<12} {appointment.get_token():<8} {appointment.get_status():<12} {date_str:<20} {fee:<10}")
                
                print("=" * 100)
                print(f"Total Appointments: {len(appointments)}")
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
    id_ini = 1
    @staticmethod
    def _generate_token() -> int:
        """Generate a unique token number for appointments."""
        Appointments.id_ini+=1
        return Appointments.id_ini
    
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
    
    def _get_consultation_fee(self, doctor_id: str) -> str:
        """Get consultation fee for a doctor or return default"""
        try:
            cursor = self.receptionist_dao.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT consultation_fee FROM doctors WHERE doctor_id = %s", (doctor_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['consultation_fee']:
                return f"₹{result['consultation_fee']:.2f}"
            else:
                return "No Doctor"
        except Exception as e:
            return "Error"
    
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

    def _generate_consultation_bill(self, appointment_data: Dict[str, Any], appointment_id: str) -> Dict[str, Any]:
        """Generate consultation bill for the appointment and save to database"""
        try:
            from services.bill_generator import bill_generator
            
            # Get patient details
            patient = self.receptionist_dao.search_patient_by_id(appointment_data["patient_id"])
            if not patient:
                return {"success": False, "message": "Patient not found for billing"}
            
            # Check if patient registered today (newly registered)
            patient_reg_date = patient.get_registration_date()
            is_newly_registered = False
            
            if isinstance(patient_reg_date, datetime):
                is_newly_registered = patient_reg_date.date() == date.today()
            
            # Get doctor details and consultation fee
            doctor_id = appointment_data["doctor_id"]
            doctor_fee = self._get_doctor_consultation_fee(doctor_id)
            doctor_name = self._get_doctor_name(doctor_id)
            
            # Generate bill and save to database
            bill_data = bill_generator.generate_consultation_bill(
                patient_id=patient.get_patient_id(),
                doctor_id=doctor_id,
                consultation_fee=doctor_fee,
                appointment_id=appointment_id,  
                is_newly_registered=is_newly_registered,
                patient_name=patient.get_patient_name(),
                doctor_name=doctor_name,
                save_to_db=True  # Save to database
            )
            
            # Format for display
            bill_display = bill_generator.display_bill(bill_data)
            
            return {
                "success": True,
                "bill_data": bill_data,
                "bill_display": bill_display,
                "saved_to_db": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating bill: {str(e)}"
            }


    def _get_doctor_consultation_fee(self, doctor_id: str) -> float:
        """Get doctor's consultation fee"""
        try:
            cursor = self.receptionist_dao.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT consultation_fee FROM doctors WHERE doctor_id = %s", (doctor_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return float(result['consultation_fee']) if result and result['consultation_fee'] else 0.0
        except Exception as e:
            print(f"Error getting consultation fee: {e}")
            return 0.0

    def _get_doctor_name(self, doctor_id: str) -> str:
        """Get doctor's name"""
        try:
            cursor = self.receptionist_dao.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT s.staff_name 
                FROM doctors d 
                JOIN staff_tb s ON d.staff_id = s.staff_id 
                WHERE d.doctor_id = %s
            """, (doctor_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result['staff_name'] if result else "Unknown Doctor"
        except Exception as e:
            print(f"Error getting doctor name: {e}")
            return "Unknown Doctor"
        
    def get_patient_bills(self, patient_id: str) -> Dict[str, Any]:
        """Get all bills for a specific patient"""
        try:
            bills = self.receptionist_dao.list_patient_bills(patient_id)
            
            if bills:
                print(f"\nBills for Patient {patient_id}")
                print("=" * 80)
                print(f"{'Bill ID':<15} {'Date':<20} {'Doctor':<15} {'Amount':<12} {'Status':<10}")
                print("-" * 80)
                
                for bill in bills:
                    print(f"{bill['bill_id']:<15} {str(bill['bill_date'])[:19]:<20} {bill['doctor_id']:<15} ₹{bill['total_amount']:<11.2f} {'Paid' if bill.get('payment_status') else 'Pending'}")
                
                print("=" * 80)
                print(f"Total Bills: {len(bills)}")
            else:
                print(f"No bills found for patient {patient_id}")
            
            return {
                "success": True,
                "bills": bills,
                "count": len(bills)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving bills: {str(e)}",
                "bills": []
            }

    def get_bill_details(self, bill_id: str) -> Dict[str, Any]:
        """Get detailed bill information"""
        try:
            bill = self.receptionist_dao.get_consultation_bill(bill_id)
            
            if bill:
                # Format bill for display
                from services.bill_generator import bill_generator
                
                # Convert database record back to bill format
                bill_items = []
                if bill['op_charge'] > 0:
                    bill_items.append({"description": "OP Charge", "amount": bill['op_charge']})
                if bill['consultation_fee'] > 0:
                    bill_items.append({"description": "Consultation Fee", "amount": bill['consultation_fee']})
                if bill['registration_charge'] > 0:
                    bill_items.append({"description": "Registration Charge", "amount": bill['registration_charge']})
                
                formatted_bill = {
                    "bill_id": bill['bill_id'],
                    "date": str(bill['bill_date']),
                    "patient_id": bill['patient_id'],
                    "patient_name": bill['patient_name'],
                    "doctor_id": bill['doctor_id'],
                    "doctor_name": bill['doctor_name'],
                    "items": bill_items,
                    "total_amount": bill['total_amount'],
                    "is_newly_registered": bill['registration_charge'] > 0
                }
                
                bill_display = bill_generator.display_bill(formatted_bill)
                print(bill_display)
                
                return {
                    "success": True,
                    "bill": bill,
                    "formatted_display": bill_display
                }
            else:
                return {
                    "success": False,
                    "message": f"Bill {bill_id} not found"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving bill: {str(e)}"
            }
