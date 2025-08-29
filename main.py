"""
Hospital Management System - Main Entry Point
Author: Vaishnavi J and Team
Version: 1.0
Description: Main file with role-based menu access for hospital management system
"""

from datetime import datetime
import sys
import os

from services.appointment_scheduler import appointment_scheduler

# Import menu modules
try:
    from menu.admin_menu import admin_menu
    from menu.doctor_menu import doctor_menu
    from menu.pharmacist_menu import pharmacist_menu
    from menu.receptionist_menu import recep_menu
    from menu.lab_technician_menu import lab_technician_menu
    from database.connection import DBConnection
    from utils.auth_validators import AuthValidator
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required modules are in the correct directories.")
    sys.exit(1)

class HospitalManagementSystem:
    """Main class for Hospital Management System"""
    
    def __init__(self):
        self.system_name = "HOSPITAL MANAGEMENT SYSTEM"
        self.version = "1.0"
        self.current_user = None
        self.current_role = None
        self.current_user_obj = None
        self.current_doctor_id = None
    
    def display_header(self):
        """Display system header"""
        print("=" * 60)
        print(f"{self.system_name.center(60)}")
        print(f"Version {self.version}".center(60))
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(60))
        print("=" * 60)
    
    def display_main_menu(self):
        """Display main role selection menu"""
        print("\n" + "=" * 40)
        print("SELECT YOUR ROLE".center(40))
        print("=" * 40)
        print("1. Administrator")
        print("2. Doctor")
        print("3. Pharmacist")
        print("4. Receptionist")
        print("5. Lab Technician")
        print("6. Exit System")
        print("=" * 40)
    
    def validate_database_connection(self):
        """Test database connection before starting"""
        try:
            conn = DBConnection().get_connection()
            if conn:
                print("✓ Database connection successful")
                return True
            else:
                print("Database connection failed")
                return False
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def authenticate_user(self, role):
        """Database-backed authentication with role verification"""
        print(f"\n--- {role.upper()} LOGIN ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Use validation utility
        auth_result = AuthValidator.authenticate_user(username, password, role)
        
        if auth_result["success"]:
            self.current_user = username
            self.current_role = role
            self.current_user_obj = auth_result.get("user")
            # Resolve doctor id for doctor role
            if role == "Doctor" and self.current_user_obj:
                try:
                    from services.DoctorManagementLib import DoctorManagementLib
                    staff_id = getattr(self.current_user_obj, 'get_staff_id', None)
                    if callable(staff_id):
                        staff_id = self.current_user_obj.get_staff_id
                    self.current_doctor_id = DoctorManagementLib.resolve_doctor_id_for_staff(staff_id)
                except Exception as e:
                    print(f"Warning: could not resolve doctor id: {e}")
            print(f"Login successful! Welcome, {username}")
            return True
        else:
            print(f"{auth_result['message']}")
            if auth_result["errors"]:
                for error in auth_result["errors"]:
                    print(f"  - {error}")
            return False
    
    def handle_role_selection(self, choice):
        """Handle role-based menu navigation"""
        roles = {
            1: ("Administrator", admin_menu),
            2: ("Doctor", doctor_menu),
            3: ("Pharmacist", pharmacist_menu),
            4: ("Receptionist", recep_menu),
            5: ("Lab Technician", lab_technician_menu)
        }
        
        if choice in roles:
            role_name, menu_function = roles[choice]
            
            # Authenticate user
            if self.authenticate_user(role_name):
                try:
                    print(f"\nAccessing {role_name} Dashboard...")
                    print(f"User: {self.current_user} | Role: {self.current_role}")
                    print("-" * 50)
                    
                    # Call the respective menu function
                    if role_name == "Doctor":
                        menu_function(self.current_doctor_id)
                    else:
                        menu_function()
                    
                    # Logout message
                    print(f"\nGoodbye, {self.current_user}!")
                    self.current_user = None
                    self.current_role = None
                    self.current_user_obj = None
                    self.current_doctor_id = None
                    
                except Exception as e:
                    print(f"Error accessing {role_name} menu: {e}")
                    print("Please contact system administrator.")
            else:
                print("Access denied. Returning to main menu...")
        
        elif choice == 6:
            self.exit_system()
        
        else:
            print("Invalid choice! Please select a valid option (1-5).")
    
    def exit_system(self):
        """Exit the system gracefully"""
        print("\n" + "=" * 60)
        print("Thank you for using Hospital Management System!".center(60))
        print("System shutting down...".center(60))
        print("=" * 60)
        sys.exit(0)
    
    def run(self):
        """Main application loop"""
        # Display header
        self.display_header()
        
        # Validate database connection
        if not self.validate_database_connection():
            print("Cannot proceed without database connection.")
            print("Please check your database configuration and try again.")
            return
        
        # Main application loop
        while True:
            try:
                self.display_main_menu()
                choice = input("\nEnter your choice (1-5): ").strip()
                
                # Validate input
                try:
                    choice = int(choice)
                    self.handle_role_selection(choice)
                except ValueError:
                    print("Please enter a valid number (1-5).")
                
                # Add spacing between menu iterations
                input("\nPress Enter to continue...")
                print("\n" * 2)  # Clear screen effect
                
            except KeyboardInterrupt:
                print("\n\nSystem interrupted by user.")
                self.exit_system()
            except Exception as e:
                print(f"Unexpected error: {e}")
                print("Please restart the application.")
                break

def main():
    """Entry point of the application"""
    try:
        # Create and run the hospital management system
        print("Initializing appointment scheduler...")
        print("Initializing token management system...")
        from services.token_manager import token_manager
        token_manager.reset_if_new_day()
        token_manager.sync_with_database()
        appointment_scheduler.reset_if_new_day()
        appointment_scheduler.sync_with_database()
        hms = HospitalManagementSystem()
        hms.run()
    
    except Exception as e:
        print(f"Critical error starting application: {e}")
        print("Please contact system administrator.")
        sys.exit(1)

if __name__ == "__main__":
    main()
