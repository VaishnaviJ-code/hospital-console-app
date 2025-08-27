import pymysql.cursors
from dao.AbstractTestDao import TestDaoService
from models.Test import Test
from database.connection import DBConnection

class TestDaoImplementation(TestDaoService):
    
    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_test(self, test: Test):
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            
            # Include test_id in the INSERT statement
            query = "INSERT INTO lab_test (test_id, test_name, description, price, is_active) VALUES (%s, %s, %s, %s, %s)"
            values = (test.test_id, test.test_name, test.description, test.price, test.status)
            
            cursor.execute(query, values)
            self.conn.commit()
            
            print(f"✅ Test '{test.test_name}' added successfully with ID: {test.test_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add test: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def display_tests(self):
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM lab_test ORDER BY test_id")
            rows = cursor.fetchall()
            
            if not rows:
                print("No lab tests found.")
                return
            
            print("\n" + "=" * 80)
            print("ALL LAB TESTS".center(80))
            print("=" * 80)
            print(f"{'ID':<10} {'Name':<25} {'Description':<30} {'Price':<10} {'Status':<8}")
            print("-" * 80)
            
            for row in rows:
                status_text = "Active" if row['is_active'] == 'y' else "Inactive"
                print(f"{row['test_id']:<10} {row['test_name']:<25} {row['description'][:29]:<30} ${row['price']:<9.2f} {status_text:<8}")
            
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ Failed to fetch tests: {e}")
        finally:
            if cursor:
                cursor.close()

    def search_test_by_id(self, test_id: str):
        """Search for a test by ID"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM lab_test WHERE test_id = %s", (test_id,))
            row = cursor.fetchone()
            
            if row:
                return Test(
                    test_id=row['test_id'],
                    test_name=row['test_name'],
                    description=row['description'],
                    price=row['price'],
                    status=row['is_active']
                )
            return None
            
        except Exception as e:
            print(f"❌ Error searching for test: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def update_test_price(self, test_id: str, new_price: float):
        """Update test price"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("UPDATE lab_test SET price = %s WHERE test_id = %s", (new_price, test_id))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Test {test_id} price updated to ${new_price:.2f}")
                return True
            else:
                print(f"❌ Test {test_id} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error updating test price: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def update_test_status(self, test_id: str, new_status: str):
        """Update test status"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("UPDATE lab_test SET is_active = %s WHERE test_id = %s", (new_status, test_id))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                status_text = "Active" if new_status == 'y' else "Inactive"
                print(f"✅ Test {test_id} status updated to {status_text}")
                return True
            else:
                print(f"❌ Test {test_id} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error updating test status: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
