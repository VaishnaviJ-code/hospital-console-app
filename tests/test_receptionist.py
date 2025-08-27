from services.receptionist_service import ReceptionistService
from datetime import datetime

service = ReceptionistService()

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
    res = service.register_patient(patient_data)
    print(res['message'])

def list_patients():
    result = service.get_all_patients()
    if not result['success']:
        print("Error fetching patients:", result['message'])
        return
    print(f"Total patients: {result['count']}")
    for p in result['patients']:
        print(f"{p.get_patient_id()}: {p.get_patient_name()} - {p.get_phone()}")

def create_appointment():
    print("Create a new appointment:")
    patient_id = input("Patient ID: ").strip()
    doctor_id = input("Doctor ID (number): ").strip()
    token = input("Token (number): ").strip()
    status = input("Status (default Scheduled): ").strip() or "Scheduled"
    date_str = input("Appointment Date (YYYY-MM-DD HH:MM): ").strip()

    try:
        doctor_id = int(doctor_id)
        token = int(token)
        appointment_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
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

def list_appointments():
    res = service.get_all_appointments()
    if not res['success']:
        print("Error fetching appointments:", res['message'])
        return
    print(f"Total appointments: {res['count']}")
    for a in res['appointments']:
        print(f"{a.get_appointment_id()}: Patient {a.get_patient_id()}, Date {a.get_appointment_date()}")

def validate_date(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except:
        return False

def main():
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
            list_patients()
        elif choice == '3':
            create_appointment()
        elif choice == '4':
            list_appointments()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()