from services.DoctorManagementLib import DoctorManagementLib
from services.StaffLib import StaffLib

def doctor_menu(doctor_id: str):
    while True:
        print("\n" + "=" * 40)
        print("    DOCTOR MANAGEMENT SYSTEM    ")
        print("=" * 40)
        
        if doctor_id:
            print(f"WELCOME DOCTOR : {doctor_id}")
            print("1. View Appointments")
            print("2. View Today's Appointments")
            print("3. Consult a Patient")
            print("4. Add Prescription")
            print("5. View Patient History")
            print("6. View Prescription Details")
            print("7. Change Username")
            print("8. Change Password")
            print("9. Exit")
            print("=" * 40)

            choice = input("Enter your choice (1-9): ").strip()

            if choice == '1':
                DoctorManagementLib.view_appointments(doctor_id)
            elif choice == '2':
                DoctorManagementLib.get_todays_appointments(doctor_id)
            elif choice == '3':
                DoctorManagementLib.consult_patient(doctor_id)
            elif choice == '4':
                DoctorManagementLib.add_prescription_full(doctor_id)
            elif choice == '5':
                patient_id = input("Enter patient ID: ").strip()
                DoctorManagementLib.view_patient_history(patient_id)
            elif choice == '6':
                prescription_id = input("Enter prescription ID: ").strip()
                DoctorManagementLib.view_prescription_details(prescription_id)
            elif choice == '7':
                StaffLib.update_staff_username()
            elif choice == '8':
                StaffLib.update_staff_passwrd()
            elif choice == '9':
                print("Exiting Doctor Management System. Goodbye!")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 9.")
        else:
            print("Error: Invalid doctor ID.")
            break
