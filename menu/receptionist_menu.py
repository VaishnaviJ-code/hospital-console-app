import pymysql
from database.connection import DBConnection
from services.appointment_scheduler import appointment_scheduler
from services.receptionist_service import ReceptionistService
from datetime import date, datetime

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
    
def show_doctor_availability_detailed(doctor_id, appointment_date):
    """Show detailed doctor availability"""
    if isinstance(appointment_date, datetime):
        date_str = appointment_date.strftime('%Y-%m-%d')
        display_date = appointment_date.strftime('%d/%m/%Y')
    else:
        date_str = appointment_date
        display_date = date_str
    
    # Get real-time availability from database
    status = appointment_scheduler.get_availability_status(doctor_id, date_str)
    
    print(f"\nDr. {doctor_id} Availability for {display_date}")
    print("-" * 50)
    print(f"Current Appointments: {status['current_appointments']}/{status['max_appointments']}")
    print(f"Available Slots: {status['available_slots']}")
    print(f"Capacity Used: {status['availability_percentage']}%")
    
    if status['is_available']:
        print(f"{status['available_slots']} slots available")
        return True
    else:
        print("Fully booked for this date!")
        return False
    
def show_doctor_availability(doctor_id, appointment_date):
    """Show doctor availability for specific date"""
    if isinstance(appointment_date, datetime):
        date_str = appointment_date.strftime('%Y-%m-%d')
        display_date = appointment_date.strftime('%d/%m/%Y')
    else:
        date_str = appointment_date
        display_date = date_str
    
    # Get real-time availability from database
    status = appointment_scheduler.get_availability_status(doctor_id, date_str)
        
    print(f"Dr. {doctor_id} availability for TODAY: {display_date}")
    print("-" * 50)
    print(f"Current Appointments: {status['current_appointments']}/{status['max_appointments']}")
    print(f"Available Slots: {status['available_slots']}")
    print(f"Capacity Used: {status['availability_percentage']}%")
    
    if status['is_available']:
        print(f"{status['available_slots']} slots available")
        return True
    else:
        print("Fully booked for this date!")
        return False

def show_all_doctors_availability():
    """Show availability for all doctors today"""
    try:
        from dao.receptionist_implementation import ReceptionistDaoImplementation
        dao = ReceptionistDaoImplementation()
        
        cursor = dao.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT d.doctor_id, s.staff_name, d.consultation_fee
            FROM doctors d
            JOIN staff_tb s ON d.staff_id = s.staff_id
            WHERE s.is_active = 'y'
        """)
        doctors = cursor.fetchall()
        cursor.close()
        
        if doctors:
            today = date.today().strftime('%Y-%m-%d')
            print(f"\nDoctor Availability for Today ({today})")
            print("=" * 80)
            print(f"{'Doctor ID':<12} {'Name':<20} {'Appointments':<15} {'Status':<15} {'Fee':<10}")
            print("-" * 80)
            
            for doctor in doctors:
                doctor_id = doctor['doctor_id']
                status = appointment_scheduler.get_availability_status(doctor_id, today)
                
                status_text = "Available" if status['is_available'] else "Full"
                appt_text = f"{status['current_appointments']}/25"
                
                print(f"{doctor_id:<12} {doctor['staff_name']:<20} {appt_text:<15} {status_text:<15} ₹{doctor['consultation_fee']:.2f}")
            
            print("=" * 80)
        
    except Exception as e:
        print(f"Error showing availability: {e}")

def create_appointment():
    print("Create a new appointment:")
    # Show current availability
    show_all_doctors_availability()
    
    patient_id = input("Patient ID: ").strip()
    doctor_id = input("Doctor ID (from list above): ").strip()
    
    while True:
        date_str = input("Appointment Date & Time (DD/MM/YYYY HH:MM): ").strip()
        
        try:
            # Parse the input date/time
            appointment_datetime = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            
            if appointment_datetime <= datetime.now():
                print("ERROR: Appointment cannot be in the past!")
                continue

            if not show_doctor_availability_detailed(doctor_id, appointment_datetime):
                choice = input("Doctor is fully booked. Try different date/doctor? (y/n): ").lower()
                if choice != 'y':
                    return
                continue
            
             # Other validations (working hours, weekends)
            if appointment_datetime.hour < 9 or appointment_datetime.hour >= 18:
                print("ERROR: Appointments only between 9:00 AM - 6:00 PM!")
                continue
                
            if appointment_datetime.weekday() >= 5:
                print("ERROR: No weekend appointments!")
                continue
            
            break
            
        except ValueError:
            print("ERROR: Invalid date/time format! Please use DD/MM/YYYY HH:MM")
            print("Example: 25/12/2025 14:30")
            continue

    token = input("Token (number): ").strip()
    status = input("Status (default Scheduled): ").strip() or "Scheduled"

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

    if res['success']:
        print(f"\nUpdated availability:")
        show_doctor_availability_detailed(doctor_id, appointment_datetime)


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
            cursor.close()
            return True
        else:
            print("No doctors available. Please add doctor profiles first.")
            
            cursor.close()
            return False
        
    except Exception as e:
        print(f"Error fetching doctors: {e}")
        return False

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