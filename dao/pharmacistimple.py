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
