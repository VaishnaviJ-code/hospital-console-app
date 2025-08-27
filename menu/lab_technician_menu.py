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
        print("4. Update Test Price")
        print("5. Update Test Status")
        print("6. View Pending Test Results")
        print("7. Record Test Result")
        print("8. Generate Test Report")
        print("9. Exit")
        print("=" * 50)
        
        choice = input("Enter your choice (1-9): ").strip()
        
        try:
            if choice == '1':
                LabTechnicianLib.add_test()
                
            elif choice == '2':
                LabTechnicianLib.display_all_tests()
                
            elif choice == '3':
                search_test()
                
            elif choice == '4':
                update_test_price()
                
            elif choice == '5':
                update_test_status()
                
            elif choice == '6':
                view_pending_tests()
                
            elif choice == '7':
                record_test_result()
                
            elif choice == '8':
                generate_test_report()
                
            elif choice == '9':
                print("Exiting Lab Technician System...")
                break
                
            else:
                print("❌ Invalid choice! Please enter a number between 1-9.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


def search_test():
    """Search for a specific lab test"""
    print("\n--- Search Lab Test ---")
    search_term = input("Enter test name or ID to search: ").strip()
    
    if search_term:
        print(f"Searching for tests containing '{search_term}'...")
        # Note: You'll need to implement search functionality in LabTechnicianLib
        print("Search functionality - to be implemented in LabTechnicianLib")
    else:
        print("❌ Please enter a search term.")


def update_test_price():
    """Update the price of an existing test"""
    print("\n--- Update Test Price ---")
    
    # First display all tests for reference
    print("Current tests:")
    LabTechnicianLib.display_all_tests()
    
    test_id = input("\nEnter test ID to update price: ").strip()
    
    if test_id:
        try:
            new_price = float(input("Enter new price: "))
            if new_price >= 0:
                print(f"Updating price for test ID {test_id} to ${new_price:.2f}")
                # Note: You'll need to implement update functionality in LabTechnicianLib
                print("Update functionality - to be implemented in LabTechnicianLib")
            else:
                print("❌ Price cannot be negative.")
        except ValueError:
            print("❌ Invalid price format. Please enter a valid number.")
    else:
        print("❌ Please enter a test ID.")


def update_test_status():
    """Update the status of an existing test"""
    print("\n--- Update Test Status ---")
    
    # First display all tests for reference
    print("Current tests:")
    LabTechnicianLib.display_all_tests()
    
    test_id = input("\nEnter test ID to update status: ").strip()
    
    if test_id:
        print("Status options:")
        print("y - Active")
        print("n - Inactive")
        
        new_status = input("Enter new status (y/n): ").strip().lower()
        
        if new_status in ['y', 'n']:
            print(f"Updating status for test ID {test_id} to {'Active' if new_status == 'y' else 'Inactive'}")
            # Note: You'll need to implement update functionality in LabTechnicianLib
            print("Update functionality - to be implemented in LabTechnicianLib")
        else:
            print("❌ Invalid status. Please enter 'y' or 'n'.")
    else:
        print("❌ Please enter a test ID.")


def view_pending_tests():
    """View tests that are pending results"""
    print("\n--- Pending Test Results ---")
    print("Displaying tests waiting for results...")
    # Note: You'll need to implement this functionality
    print("Pending tests functionality - to be implemented")


def record_test_result():
    """Record results for a completed test"""
    print("\n--- Record Test Result ---")
    
    prescription_id = input("Enter prescription ID: ").strip()
    test_id = input("Enter test ID: ").strip()
    
    if prescription_id and test_id:
        result = input("Enter test result: ").strip()
        notes = input("Enter additional notes (optional): ").strip()
        
        if result:
            print(f"Recording result for prescription {prescription_id}, test {test_id}")
            print(f"Result: {result}")
            if notes:
                print(f"Notes: {notes}")
            
            # Note: You'll need to implement this functionality
            print("Record result functionality - to be implemented")
        else:
            print("❌ Test result cannot be empty.")
    else:
        print("❌ Please enter both prescription ID and test ID.")


def generate_test_report():
    """Generate a test report"""
    print("\n--- Generate Test Report ---")
    
    print("Report options:")
    print("1. Daily test summary")
    print("2. Test statistics")
    print("3. Pending tests report")
    print("4. Custom date range")
    
    report_choice = input("Select report type (1-4): ").strip()
    
    if report_choice in ['1', '2', '3', '4']:
        print(f"Generating report type {report_choice}...")
        # Note: You'll need to implement report generation
        print("Report generation functionality - to be implemented")
    else:
        print("❌ Invalid report choice.")


if __name__ == "__main__":
    lab_technician_menu()
