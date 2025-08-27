from services.DoctorManagementLib import DoctorManagementLib

def doctor_menu():
    while True:
        print("")
        print(f"================================")
        print("--- Doctor Management System ---")
        print(f"================================")
        print("1. View Appointments")
        print("2. View Today's Appointments")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            DoctorManagementLib.view_appointments()
        elif choice == '2':
            DoctorManagementLib.get_todays_appointments()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please enter a valid option!")
