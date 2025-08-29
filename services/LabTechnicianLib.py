from models.Test import Test
from dao.TestDaoImpl import TestDaoImplementation
import pymysql
from datetime import datetime

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
            
            price_str = input("Enter price: $").strip()
            try:
                price = float(price_str)
                if price < 0:
                    print("Price cannot be negative.")
                    return
            except ValueError:
                print("Invalid price format. Please enter a valid number.")
                return

            print("Status options: y (Active) / n (Inactive)")
            status = input("Enter status (y/n): ").strip().lower()
            if status not in ['y', 'n']:
                print("Invalid status. Using 'y' (Active) as default.")
                status = 'y'

            # Generate test ID automatically
            test_id = LabTechnicianLib.generate_test_id()
            
            test = Test(test_id, name, desc, price, status)
            
            if LabTechnicianLib.dao.add_test(test):
                print(f"Test '{name}' added successfully with ID: {test_id}")
            else:
                print("Failed to add test.")

        except Exception as e:
            print(f"Error adding test: {e}")

    @staticmethod
    def display_all_tests():
        """Display all lab tests"""
        print("\n--- All Lab Tests ---")
        LabTechnicianLib.dao.display_tests()

    @staticmethod
    def search_test():
        """Search for tests by name or ID"""
        print("\n--- Search Lab Test ---")
        search_term = input("Enter test name or ID to search: ").strip()
        
        if not search_term:
            print("Please enter a search term.")
            return
            
        cursor = None
        try:
            conn = LabTechnicianLib.dao.conn
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Search by ID or name
            cursor.execute("""
                SELECT * FROM lab_test 
                WHERE test_id LIKE %s OR test_name LIKE %s
                ORDER BY test_id
            """, (f"%{search_term}%", f"%{search_term}%"))
            
            results = cursor.fetchall()
            
            if not results:
                print(f"No tests found matching '{search_term}'")
                return
                
            print(f"\nSearch Results for '{search_term}':")
            print("=" * 80)
            print(f"{'ID':<10} {'Name':<25} {'Description':<30} {'Price':<10} {'Status':<8}")
            print("-" * 80)
            
            for row in results:
                status_text = "Active" if row['is_active'] == 'y' else "Inactive"
                print(f"{row['test_id']:<10} {row['test_name']:<25} {row['description'][:29]:<30} ${row['price']:<9.2f} {status_text:<8}")
            
            print("=" * 80)
            
        except Exception as e:
            print(f"Error searching tests: {e}")
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def update_test():
        """Update an existing lab test"""
        print("\n--- Update Lab Test ---")
        
        # Display all tests first for reference
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
                if new_price < 0:
                    print("Price cannot be negative")
                    return
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
    def view_pending_tests():
        """View tests that are pending results"""
        print("\n--- Pending Test Results ---")
        
        cursor = None
        try:
            conn = LabTechnicianLib.dao.conn
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("""
                SELECT pt.patient_id, pt.doctor_id, pt.test_id, lt.test_name, pt.status
                FROM prescription_test pt
                JOIN lab_test lt ON pt.test_id = lt.test_id
                WHERE pt.status = 'Pending'
                ORDER BY pt.patient_id, pt.test_id
            """)
            
            results = cursor.fetchall()
            
            if not results:
                print("No pending tests found.")
                return
                
            print("=" * 80)
            print(f"{'Patient ID':<12} {'Doctor ID':<10} {'Test ID':<10} {'Test Name':<25} {'Status':<10}")
            print("-" * 80)
            
            for row in results:
                print(f"{row['patient_id']:<12} {row['doctor_id']:<10} {row['test_id']:<10} {row['test_name']:<25} {row['status']:<10}")
            
            print("=" * 80)
            
        except Exception as e:
            print(f"Error fetching pending tests: {e}")
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def record_test_result():
        """Record results for a completed test"""
        print("\n--- Record Test Result ---")
        
        # First show pending tests
        LabTechnicianLib.view_pending_tests()
        
        patient_id = input("\nEnter Patient ID: ").strip()
        test_id = input("Enter Test ID: ").strip()
        
        if not patient_id or not test_id:
            print("Both Patient ID and Test ID are required.")
            return
            
        result = input("Enter test result: ").strip()
        if not result:
            print("Test result cannot be empty.")
            return
            
        notes = input("Enter additional notes (optional): ").strip()
        
        cursor = None
        try:
            conn = LabTechnicianLib.dao.conn
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Check if test exists and is pending
            cursor.execute("""
                SELECT pt.*, lt.test_name 
                FROM prescription_test pt
                JOIN lab_test lt ON pt.test_id = lt.test_id
                WHERE pt.patient_id = %s AND pt.test_id = %s AND pt.status = 'Pending'
            """, (patient_id, test_id))
            
            test_record = cursor.fetchone()
            if not test_record:
                print("No pending test found for this patient and test ID.")
                return
            
            # Insert result into lab_test_result table
            cursor.execute("""
                INSERT INTO lab_test_result (test_id, prescription_id, result, notes, created_at)
                VALUES (%s, (SELECT prescription_id FROM prescriptions WHERE patient_id = %s LIMIT 1), %s, %s, %s)
            """, (test_id, patient_id, result, notes, datetime.now()))
            
            # Update test status to completed
            cursor.execute("""
                UPDATE prescription_test 
                SET status = 'Completed' 
                WHERE patient_id = %s AND test_id = %s
            """, (patient_id, test_id))
            
            conn.commit()
            
            print(f"Test result recorded successfully for {test_record['test_name']}")
            print(f"Result: {result}")
            if notes:
                print(f"Notes: {notes}")
                
        except Exception as e:
            print(f"Error recording test result: {e}")
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def generate_test_report():
        """Generate various test reports"""
        print("\n--- Generate Test Report ---")
        print("Report options:")
        print("1. Daily test summary")
        print("2. Test statistics")
        print("3. Pending tests report")
        print("4. Custom date range")
        
        report_choice = input("Select report type (1-4): ").strip()
        
        cursor = None
        try:
            conn = LabTechnicianLib.dao.conn
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            if report_choice == '1':
                # Daily test summary
                cursor.execute("""
                    SELECT lt.test_name, COUNT(*) as count, SUM(lt.price) as total_revenue
                    FROM lab_test_result ltr
                    JOIN lab_test lt ON ltr.test_id = lt.test_id
                    WHERE DATE(ltr.created_at) = CURDATE()
                    GROUP BY lt.test_id, lt.test_name
                    ORDER BY count DESC
                """)
                
                results = cursor.fetchall()
                
                print(f"\n=== DAILY TEST SUMMARY - {datetime.now().strftime('%Y-%m-%d')} ===")
                print(f"{'Test Name':<30} {'Count':<8} {'Revenue':<10}")
                print("-" * 50)
                
                total_tests = 0
                total_revenue = 0
                
                for row in results:
                    total_tests += row['count']
                    total_revenue += float(row['total_revenue'])
                    print(f"{row['test_name']:<30} {row['count']:<8} ${row['total_revenue']:<9.2f}")
                
                print("-" * 50)
                print(f"{'TOTAL:':<30} {total_tests:<8} ${total_revenue:<9.2f}")
                
            elif report_choice == '2':
                # Test statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_tests,
                        COUNT(CASE WHEN is_active = 'y' THEN 1 END) as active_tests,
                        COUNT(CASE WHEN is_active = 'n' THEN 1 END) as inactive_tests,
                        AVG(price) as avg_price,
                        MIN(price) as min_price,
                        MAX(price) as max_price
                    FROM lab_test
                """)
                
                stats = cursor.fetchone()
                
                print("\n=== TEST STATISTICS ===")
                print(f"Total Tests: {stats['total_tests']}")
                print(f"Active Tests: {stats['active_tests']}")
                print(f"Inactive Tests: {stats['inactive_tests']}")
                print(f"Average Price: ${stats['avg_price']:.2f}")
                print(f"Minimum Price: ${stats['min_price']:.2f}")
                print(f"Maximum Price: ${stats['max_price']:.2f}")
                
            elif report_choice == '3':
                # Pending tests report
                LabTechnicianLib.view_pending_tests()
                
            elif report_choice == '4':
                # Custom date range
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                
                cursor.execute("""
                    SELECT lt.test_name, COUNT(*) as count, SUM(lt.price) as total_revenue
                    FROM lab_test_result ltr
                    JOIN lab_test lt ON ltr.test_id = lt.test_id
                    WHERE DATE(ltr.created_at) BETWEEN %s AND %s
                    GROUP BY lt.test_id, lt.test_name
                    ORDER BY count DESC
                """, (start_date, end_date))
                
                results = cursor.fetchall()
                
                print(f"\n=== TEST REPORT - {start_date} to {end_date} ===")
                print(f"{'Test Name':<30} {'Count':<8} {'Revenue':<10}")
                print("-" * 50)
                
                for row in results:
                    print(f"{row['test_name']:<30} {row['count']:<8} ${row['total_revenue']:<9.2f}")
                
            else:
                print("Invalid report choice.")
                
        except Exception as e:
            print(f"Error generating report: {e}")
        finally:
            if cursor:
                cursor.close()

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
            filename = f"lab_bill_{prescription_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
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
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                print(f"Bill saved as '{filename}'")
            except Exception as e:
                print(f"Error saving bill: {e}")

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
        """Generate next test ID following the pattern TEST1000, TEST1001, etc."""
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
