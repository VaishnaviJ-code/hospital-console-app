from typing import Any, Dict
import pymysql
from database.connection import DBConnection
from dao.pharmacistabstract import PharmacistDAO
from models.pharmacist import Medicine

class PharmacistImpl(PharmacistDAO):

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_medicine(self, medicine: Medicine):
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            sql = "INSERT INTO medicines (med_id, name, med_type, price, stock, expiry_date, available) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            values = (
                medicine.get_med_id(),
                medicine.get_name(),
                medicine.get_med_type(),
                medicine.get_price(),
                medicine.get_stock(),
                medicine.get_expiry_date(),
                medicine.get_available()
            )
            cursor.execute(sql, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding medicine: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def display_all_medicines(self) -> list[Medicine]:
        medicines = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM medicines"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                medicine = Medicine(
                    med_id=row['med_id'],
                    name=row['name'],
                    med_type=row['med_type'],
                    price=row['price'],
                    stock=row['stock'],
                    expiry_date=row['expiry_date'],
                    available=row['available']
                )
                medicines.append(medicine)
        except Exception as e:
            print(f"Error occurred while fetching medicines: {e}")
        finally:
            cursor.close()
        return medicines

    def update_medicine(self, med_id: str, name: str, med_type: str, price: float, stock: int, expiry_date: str, available: str) -> bool:
        """Update an existing medicine"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            query = """
            UPDATE medicines 
            SET name = %s, med_type = %s, price = %s, stock = %s, expiry_date = %s, available = %s 
            WHERE med_id = %s
            """
            cursor.execute(query, (name, med_type, price, stock, expiry_date, available, med_id))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Medicine '{med_id}' updated successfully!")
                return True
            else:
                print(f"No medicine found with ID '{med_id}'")
                return False
                
        except Exception as e:
            print(f"Error updating medicine: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_medicine(self, med_id: str) -> bool:
        """Delete a medicine with confirmation"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            
            # First check if medicine exists
            check_query = "SELECT name FROM medicines WHERE med_id = %s"
            cursor.execute(check_query, (med_id,))
            medicine = cursor.fetchone()
            
            if not medicine:
                print(f"No medicine found with ID '{med_id}'")
                return False
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete medicine '{medicine['name']}' (ID: {med_id})? (y/N): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled")
                return False
            
            # Delete the medicine
            delete_query = "DELETE FROM medicines WHERE med_id = %s"
            cursor.execute(delete_query, (med_id,))
            self.conn.commit()
            
            print(f"Medicine '{medicine['name']}' deleted successfully!")
            return True
            
        except Exception as e:
            print(f"Error deleting medicine: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def get_medicine_by_id(self, med_id: str):
        """Get a specific medicine by ID"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM medicines WHERE med_id = %s"
            cursor.execute(query, (med_id,))
            result = cursor.fetchone()
            
            if result:
                return Medicine(
                    med_id=result['med_id'],
                    name=result['name'],
                    med_type=result['med_type'],
                    price=result['price'],
                    stock=result['stock'],
                    expiry_date=result['expiry_date'],
                    available=result['available']
                )
            return None
            
        except Exception as e:
            print(f"Error fetching medicine: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def dispense_medicine(self, prescription_id: str) -> Dict[str, Any]:
        """Dispense medicines for a prescription and generate bill"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            
            # Get medicines for this prescription
            query = """
            SELECT m.med_id, m.name, m.price, pm.dosage, pm.duartion as duration
            FROM prescribtion_medicine pm
            JOIN medicines m ON pm.medicine_id = m.med_id
            WHERE pm.prescribtion_id = %s
            """
            
            cursor.execute(query, (prescription_id,))
            medicines = cursor.fetchall()
            
            if not medicines:
                return {"success": False, "message": "No medicines found for this prescription"}
            
            total_amount = 0.0
            dispensed_items = []
            
            for med in medicines:
                quantity = 1  # Default quantity, can be modified
                item_total = float(med['price']) * quantity
                total_amount += item_total
                
                dispensed_items.append({
                    'med_id': med['med_id'],
                    'name': med['name'],
                    'price': med['price'],
                    'quantity': quantity,
                    'dosage': med['dosage'],
                    'duration': med['duration'],
                    'total': item_total
                })
            
            # Record the sale
            sale_id = self.generate_sale_id()
            sale_query = """
            INSERT INTO pharmacy_sales (sale_id, prescription_id, total_amount, sale_date)
            VALUES (%s, %s, %s, NOW())
            """
            
            cursor.execute(sale_query, (sale_id, prescription_id, total_amount))
            self.conn.commit()
            
            return {
                "success": True,
                "sale_id": sale_id,
                "prescription_id": prescription_id,
                "items": dispensed_items,
                "total_amount": total_amount
            }
            
        except Exception as e:
            print(f"Error dispensing medicines: {e}")
            self.conn.rollback()
            return {"success": False, "message": str(e)}
        finally:
            if cursor:
                cursor.close()

    def generate_sale_id(self):
        """Generate next sale ID"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT sale_id FROM pharmacy_sales ORDER BY sale_id DESC LIMIT 1")
            result = cursor.fetchone()
            
            if result and result['sale_id'].startswith("SAL"):
                last_num = int(result['sale_id'][3:])
                return f"SAL{last_num + 1:04d}"
            else:
                return "SAL1000"
                
        except Exception as e:
            print(f"Error generating sale ID: {e}")
            return "SAL1000"
        finally:
            if cursor:
                cursor.close()

    def generate_medicine_id(self) -> str:
        """Generate next medicine ID"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT med_id FROM medicines ORDER BY med_id DESC LIMIT 1")
            result = cursor.fetchone()
            
            if result and result['med_id'].startswith("MED"):
                last_num = int(result['med_id'][3:])
                return f"MED{last_num + 1:04d}"
            else:
                return "MED1000"
                
        except Exception as e:
            print(f"Error generating medicine ID: {e}")
            return "MED1000"
        finally:
            if cursor:
                cursor.close()
