from models.Test import Test
from dao.TestDaoImpl import TestDaoImplementation
import pymysql

class LabTechnicianLib:
    dao = TestDaoImplementation()

    @staticmethod
    def add_test():
        """Add a new lab test with validation"""
        print("\n--- Add New Lab Test ---")
        
        try:
            name = input("Enter test name: ").strip()
            if not name:
                print("Test name cannot be empty.")
                return
                
            desc = input("Enter description: ").strip()
            
            price = float(input("Enter price: $"))
            if price < 0:
                print("Price cannot be negative.")
                return
                
            print("Status options: y (Active) / n (Inactive)")
            status = input("Enter status (y/n): ").strip().lower()
            
            if status not in ['y', 'n']:
                print("Invalid status. Using 'y' (Active) as default.")
                status = 'y'
            
            # Generate test ID automatically
            test_id = LabTechnicianLib.generate_test_id()
            
            test = Test(test_id, name, desc, price, status)
            LabTechnicianLib.dao.add_test(test)
            
        except ValueError:
            print("Invalid price format. Please enter a valid number.")
        except Exception as e:
            print(f"Error adding test: {e}")

    @staticmethod
    def display_all_tests():
        """Display all lab tests"""
        print("\n--- All Lab Tests ---")
        LabTechnicianLib.dao.display_tests()

    @staticmethod
    def update_test():
        """Update an existing lab test"""
        print("\n--- Update Lab Test ---")
        
        # Display all tests first
        LabTechnicianLib.display_all_tests()
        
        test_id = input("\nEnter Test ID to update: ").strip()
        if not test_id:
            print("Test ID cannot be empty")
            return
        
        # Get existing test info
        existing_test = LabTechnicianLib.dao.get_test_by_id(test_id)
        if not existing_test:
            print(f"No test found with ID '{test_id}'")
            return
        
        print(f"\nCurrent test info:")
        print(f"Name: {existing_test.test_name}")
        print(f"Description: {existing_test.description}")
        print(f"Price: ${existing_test.price}")
        print(f"Status: {'Active' if existing_test.status == 'y' else 'Inactive'}")
        
        # Get new values (allow empty to keep current)
        print("\nEnter new values (press Enter to keep current):")
        
        new_name = input(f"Test name [{existing_test.test_name}]: ").strip()
        if not new_name:
            new_name = existing_test.test_name
        
        new_desc = input(f"Description [{existing_test.description}]: ").strip()
        if not new_desc:
            new_desc = existing_test.description
        
        new_price_str = input(f"Price [{existing_test.price}]: ").strip()
        if new_price_str:
            try:
                new_price = float(new_price_str)
            except ValueError:
                print("Invalid price format")
                return
        else:
            new_price = existing_test.price
        
        new_status_str = input(f"Status (y/n) [{'y' if existing_test.status == 'y' else 'n'}]: ").strip().lower()
        if new_status_str and new_status_str in ['y', 'n']:
            new_status = new_status_str
        else:
            new_status = existing_test.status
        
        # Update the test
        success = LabTechnicianLib.dao.update_test(test_id, new_name, new_desc, new_price, new_status)
        if success:
            print("Test updated successfully!")

    @staticmethod
    def delete_test():
        """Delete a lab test"""
        print("\n--- Delete Lab Test ---")
        
        # Display all tests first
        LabTechnicianLib.display_all_tests()
        
        test_id = input("\nEnter Test ID to delete: ").strip()
        if not test_id:
            print("Test ID cannot be empty")
            return
        
        # Delete the test (confirmation handled in DAO)
        LabTechnicianLib.dao.delete_test(test_id)

    @staticmethod
    def generate_test_bill():
        """Generate bill for lab tests"""
        print("\n--- Generate Lab Test Bill ---")
        
        prescription_id = input("Enter Prescription ID: ").strip()
        if not prescription_id:
            print("Prescription ID cannot be empty")
            return
        
        # Get tests for this prescription
        tests = LabTechnicianLib.dao.get_tests_for_prescription(prescription_id)
        
        if not tests:
            print("No tests found for this prescription")
            return
        
        print(f"\n" + "=" * 60)
        print(f"LAB TEST BILL - PRESCRIPTION: {prescription_id}".center(60))
        print("=" * 60)
        print(f"{'Test ID':<10} {'Test Name':<25} {'Price':<10} {'Status':<10}")
        print("-" * 60)
        
        total_amount = 0.0
        for test in tests:
            test_price = float(test['price'])
            total_amount += test_price
            print(f"{test['test_id']:<10} {test['test_name']:<25} ${test_price:<9.2f} {test['status']:<10}")
        
        print("-" * 60)
        print(f"{'TOTAL AMOUNT:':<45} ${total_amount:.2f}")
        print("=" * 60)
        print("Thank you for using our lab services!")
        print("=" * 60)
        
        # Save bill to file (optional)
        save_bill = input("\nSave bill to file? (y/N): ").strip().lower()
        if save_bill == 'y':
            filename = f"lab_bill_{prescription_id}.txt"
            with open(filename, 'w') as f:
                f.write(f"LAB TEST BILL - PRESCRIPTION: {prescription_id}\n")
                f.write("=" * 60 + "\n")
                f.write(f"{'Test ID':<10} {'Test Name':<25} {'Price':<10} {'Status':<10}\n")
                f.write("-" * 60 + "\n")
                for test in tests:
                    test_price = float(test['price'])
                    f.write(f"{test['test_id']:<10} {test['test_name']:<25} ${test_price:<9.2f} {test['status']:<10}\n")
                f.write("-" * 60 + "\n")
                f.write(f"{'TOTAL AMOUNT:':<45} ${total_amount:.2f}\n")
                f.write("=" * 60 + "\n")
            print(f" Bill saved as '{filename}'")
    
    @staticmethod
    def get_all_test_ids():
        """Get all existing test IDs from database"""
        cursor = None
        ids = []
        try:
            conn = LabTechnicianLib.dao.conn
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT test_id FROM lab_test")
            rows = cursor.fetchall()
            for row in rows:
                ids.append(row['test_id'])
        except Exception as e:
            print("Error fetching test IDs: ", e)
        finally:
            if cursor:
                cursor.close()
        return ids

    @staticmethod
    def generate_test_id():
        """Generate next test ID following the pattern TEST0001, TEST0002, etc."""
        ids = LabTechnicianLib.get_all_test_ids()
        
        # If no tests exist, start with TEST1000
        if not ids:
            return "TEST1000"
        
        # Extract numeric parts from existing test IDs
        numeric_ids = []
        for test_id in ids:
            if test_id and test_id.startswith("TEST"):
                try:
                    numeric_part = int(test_id[4:])  # Extract part after "TEST"
                    numeric_ids.append(numeric_part)
                except ValueError:
                    continue  # Skip invalid IDs
        
        # Find the maximum ID and increment by 1
        max_id = max(numeric_ids) if numeric_ids else 999
        new_id = max_id + 1
        
        # Return formatted ID with 4-digit padding
        return f"TEST{new_id:04d}"
