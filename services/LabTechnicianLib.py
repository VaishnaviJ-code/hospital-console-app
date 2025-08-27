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
                print("❌ Test name cannot be empty.")
                return
                
            desc = input("Enter description: ").strip()
            
            price = float(input("Enter price: $"))
            if price < 0:
                print("❌ Price cannot be negative.")
                return
                
            print("Status options: y (Active) / n (Inactive)")
            status = input("Enter status (y/n): ").strip().lower()
            
            if status not in ['y', 'n']:
                print("❌ Invalid status. Using 'y' (Active) as default.")
                status = 'y'
            
            # Generate test ID automatically
            test_id = LabTechnicianLib.generate_test_id()
            
            test = Test(test_id, name, desc, price, status)
            LabTechnicianLib.dao.add_test(test)
            
        except ValueError:
            print("❌ Invalid price format. Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error adding test: {e}")

    @staticmethod
    def display_all_tests():
        """Display all lab tests"""
        print("\n--- All Lab Tests ---")
        LabTechnicianLib.dao.display_tests()
    
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
