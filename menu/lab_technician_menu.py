from services.LabTechnicianLib import LabTechnicianLib

def lab_technician_menu():
    """Lab Technician menu for managing lab tests and operations"""
    while True:
        print("\n" + "=" * 50)
        print("--- LAB TECHNICIAN MANAGEMENT SYSTEM ---".center(50))
        print("=" * 50)
        print("1. Add New Lab Test")
        print("2. Display All Lab Tests")
        print("3. Search Lab Test")
        print("4. Update Test Info")
        print("5. Delete Test")
        print("6. Generate Test Bill")
        print("7. View Pending Tests")
        print("8. Record Test Result")
        # print("9. Generate Reports")
        print("9. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-10): ").strip()

        try:
            if choice == '1':
                LabTechnicianLib.add_test()
            elif choice == '2':
                LabTechnicianLib.display_all_tests()
            elif choice == '3':
                LabTechnicianLib.search_test()
            elif choice == '4':
                LabTechnicianLib.update_test()
            elif choice == '5':
                LabTechnicianLib.delete_test()
            elif choice == '6':
                LabTechnicianLib.generate_test_bill()
            elif choice == '7':
                LabTechnicianLib.view_pending_tests()
            elif choice == '8':
                LabTechnicianLib.record_test_result()
            # elif choice == '9':
            #     LabTechnicianLib.generate_test_report()
            elif choice == '9':
                print("Exiting Lab Technician System...")
                break
            else:
                print("Invalid choice! Please enter a number between 1-10.")

        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

        # Pause before showing menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    lab_technician_menu()
