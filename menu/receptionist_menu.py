from services.receptionist_service import ReceptionistService
from datetime import datetime

service = ReceptionistService()

def patient_id_exists(patient_id):
    """Check if patient ID exists in the database"""
    if not patient_id or not patient_id.strip():
        return True  # Return True to indicate invalid (empty ID should fail validation)
    
    try:
        result = service.find_patient("id", patient_id.strip())
        return result['success']  # Returns True if patient exists (validation fails)
    except Exception as e:
        print(f"Error checking patient ID: {e}")
        return True  # Return True to fail validation on error

def input_with_validation(prompt, validation_func, error_msg):
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        else:
            print(error_msg)

def add_patient():
    print("Enter new patient details:")
    name = input_with_validation("Name: ", lambda x: len(x) >= 2, "Name should be at least 2 characters.")
    dob = input_with_validation("DOB (YYYY-MM-DD): ", lambda x: validate_date(x), "Invalid date format.")
    gender = input_with_validation("Gender (male/female/other): ", lambda x: x.lower() in ['male', 'female', 'other'], "Invalid gender.")
    phone = input_with_validation("Phone (digits): ", lambda x: x.isdigit() and len(x) == 10, "Phone must be 10 digits.")
    address = input_with_validation("Address: ", lambda x: len(x) >= 5, "Address too short.")
    email = input_with_validation("Email: ", lambda x: '@' in x and '.' in x, "Invalid email.")

    patient_data = {
        "patient_name": name,
        "dob": dob,
        "gender": gender,
        "phone": phone,
        "address": address,
        "email": email
    }
    res = service.register_new_patient(patient_data)
    print(res['message'])

def create_appointment():
    print("Create a new appointment:")
    patient_id = input("Patient ID: ").strip()
    doctor_id = input("Doctor ID (number): ").strip()
    token = input("Token (number): ").strip()
    status = input("Status (default Scheduled): ").strip() or "Scheduled"
    date_str = input("Appointment Date (YYYY-MM-DD HH:MM): ").strip()

    try:
        doctor_id = doctor_id
        token = int(token)
        appointment_date = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        print("Invalid input values.")
        return

    appt_data = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "token": token,
        "status": status,
        "appointment_date": appointment_date
    }
    res = service.schedule_appointment(appt_data)
    print(res['message'])


def validate_date(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except:
        return False

def recep_menu():
    while True:
        print("==== Receptionist Menu ====")
        print("1) Add Patient")
        print("2) List Patients")
        print("3) Create Appointment")
        print("4) List Appointments")
        print("5) Exit")
        choice = input("Choose option: ")

        if choice == '1':
            add_patient()
        elif choice == '2':
            ReceptionistService().get_all_patients()
        elif choice == '3':
            create_appointment()
        elif choice == '4':
            ReceptionistService().get_all_appointments()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
