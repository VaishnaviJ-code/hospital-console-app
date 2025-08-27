from services.DoctorManagementLib import DoctorManagementLib

def doctor_menu():
    while True:
        print("\n" + "=" * 32)
        print("     Doctor Management System     ")
        print("=" * 32)
        print("1. View Appointments")
        print("2. View Today's Appointments")
        print("3. Consult a Patient")
        print("4. Add Prescription")
        print("5. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            DoctorManagementLib.view_appointments()
        elif choice == '2':
            DoctorManagementLib.get_todays_appointments()
        elif choice == '3':
            DoctorManagementLib.consult_patient()
        elif choice == '4':
            DoctorManagementLib.add_prescription_full()
        elif choice == '5':
            print("Exiting Doctor Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")
