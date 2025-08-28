import pymysql
from database.connection import DBConnection
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
    dob = input_with_validation("DOB (DD/MM/YYYY): ", lambda x: validate_date_format(x), "Invalid date format. Use DD/MM/YYYY")
     # Convert to YYYY-MM-DD format for database storage
    try:
        parsed_date = datetime.strptime(dob, "%d/%m/%Y")
        formatted_dob = parsed_date.strftime("%Y-%m-%d")  # Convert to MySQL format
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY")
        return
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

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def create_appointment():
    print("Create a new appointment:")
    show_available_doctors()
    
    patient_id = input("Patient ID: ").strip()
    doctor_id = input("Doctor ID (from list above): ").strip()
    token = input("Token (number): ").strip()
    status = input("Status (default Scheduled): ").strip() or "Scheduled"
    
    
    while True:
        date_str = input("Appointment Date & Time (DD/MM/YYYY HH:MM): ").strip()
        
        try:
            # Parse the input date/time
            appointment_datetime = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            
            # Check if appointment is in the past
            current_time = datetime.now()
            if appointment_datetime <= current_time:
                print("ERROR: Appointment date and time cannot be in the past!")
                print(f"Current time: {current_time.strftime('%d/%m/%Y %H:%M')}")
                print(f"You entered: {appointment_datetime.strftime('%d/%m/%Y %H:%M')}")
                continue  # Ask for input again
            
            # Check if appointment is too far in future (optional)
            days_ahead = (appointment_datetime.date() - current_time.date()).days
            if days_ahead > 365:
                print("ERROR: Appointment cannot be scheduled more than 1 year in advance!")
                continue
            
            # Check working hours (9 AM to 6 PM)
            appointment_hour = appointment_datetime.hour
            if appointment_hour < 9 or appointment_hour >= 18:
                print("ERROR: Appointments can only be scheduled between 9:00 AM and 6:00 PM!")
                continue
            
            # Check weekends (optional)
            if appointment_datetime.weekday() >= 5:  # Saturday=5, Sunday=6
                print("ERROR: Appointments cannot be scheduled on weekends!")
                continue
            
            # If all validations pass, break the loop
            break
            
        except ValueError:
            print("ERROR: Invalid date/time format! Please use DD/MM/YYYY HH:MM")
            print("Example: 25/12/2025 14:30")
            continue

    try:
        token = int(token)
    except ValueError:
        print("Invalid token. Must be a number.")
        return

    appt_data = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "token": token,
        "status": status,
        "appointment_date": appointment_datetime
    }

    res = service.schedule_appointment(appt_data)
    print(res['message'])


def validate_date(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except:
        return False

def update_patient():

    print("Update Patient Details")
    patient_id = input("Patient ID: ").strip()
    
    # Check if patient exists first
    result = service.find_patient("id", patient_id)
    if not result["success"]:
        print(f"{result['message']}")
        return
    
    print(f" Patient found: {result['patient']}")
    
    valid_fields = ['name', 'address', 'phone']
    field = input_with_validation(
        "Enter field to be updated (name, address, phone): ",
        lambda x: x.lower() in valid_fields,
        f"Invalid field. Must be one of: {', '.join(valid_fields)}"
    ).lower()
    

    new_value = input(f"Enter new value for {field}: ").strip()
    
    if not new_value:
        print("New value cannot be empty.")
        return
    
    update_result = service.update_patient_details(patient_id, field, new_value)
    print(f"{'SUCCESS!' if update_result['success'] else 'FAILURE'} {update_result['message']}")

def show_available_doctors():
    """Display available doctors for appointment booking"""
    try:
        conn = DBConnection().get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        query = """
        SELECT d.doctor_id, s.staff_name, dept.dept_name, sp.specialization, d.consultation_fee
        FROM doctors d
        JOIN staff_tb s ON d.staff_id = s.staff_id
        JOIN department dept ON d.dept_id = dept.dept_id
        JOIN specialization sp ON d.sp_id = sp.sp_id
        WHERE s.is_active = 'y'
        """
        
        cursor.execute(query)
        doctors = cursor.fetchall()
        
        if doctors:
            print("\n" + "=" * 80)
            print("AVAILABLE DOCTORS".center(80))
            print("=" * 80)
            print(f"{'Doctor ID':<12} {'Name':<20} {'Department':<15} {'Specialization':<15} {'Fee':<10}")
            print("-" * 80)
            
            for doc in doctors:
                print(f"{doc['doctor_id']:<12} {doc['staff_name']:<20} {doc['dept_name']:<15} {doc['specialization']:<15} ₹{doc['consultation_fee']:.2f}")
            
            print("=" * 80)
        else:
            print("No doctors available. Please add doctor profiles first.")
            
        cursor.close()
        
    except Exception as e:
        print(f"Error fetching doctors: {e}")

def recep_menu():
    while True:
        print("\n" + "=" * 40)
        print("RECEPTIONIST MENU".center(40))
        print("=" * 40)
        print("1) Add Patient")
        print("2) List Patients")
        print("3) Update Patient")
        print("4) Create Appointment")
        print("5) List Appointments")
        print("6) Exit")
        print("=" * 40)
        
        choice = input("Choose option (1-6): ").strip()

        try:
            if choice == '1':
                add_patient()
            elif choice == '2':
                service.get_all_patients()  
            elif choice == '3':
                update_patient()
            elif choice == '4':
                create_appointment()
            elif choice == '5':
                service.get_all_appointments() 
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number 1-6.")
        except Exception as e:
            print(f" An error occurred: {e}")
            print("Please try again.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    recep_menu()