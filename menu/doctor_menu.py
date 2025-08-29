from services.DoctorManagementLib import DoctorManagementLib
from services.StaffLib import StaffLib
def doctor_menu(doctor_id: str):
    while True:
        print("\n" + "=" * 32)
        print("     Doctor Management System     ")
        print("=" * 32)
        if doctor_id:
            print(f"WELCOME DOCTOR : {doctor_id}")
        print("1. View Appointments")
        print("2. View Today's Appointments")
        print("3. Consult a Patient")
        print("4. Add Prescription")
        print("5. Change username")
        print("6. Change password")
        print("7. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            DoctorManagementLib.view_appointments(doctor_id)
        elif choice == '2':
            DoctorManagementLib.get_todays_appointments(doctor_id)
        elif choice == '3':
            DoctorManagementLib.consult_patient(doctor_id)
        elif choice == '4':
            DoctorManagementLib.add_prescription_full(doctor_id)
        elif choice == '5':
            StaffLib.update_staff_username()
        elif choice == '6':
            StaffLib.update_staff_passwrd()
        elif choice == '7':
            print("Exiting Doctor Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")
