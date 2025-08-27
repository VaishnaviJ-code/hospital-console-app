from dao.StaffDaoAbstract import StaffDaoServices
from models.staff import Staff
from typing import List
from database.connection import DBConnection
import pymysql

class StaffDaoImple(StaffDaoServices):
    INSERT_STAFF="INSERT into staff_tb(staff_id,staff_name,DOB,age,email,phone,address,experience,joining_date,role_id,username,pass_wrd,is_active,created_at,gender) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    DISPLAY_ALL="SELECT * from staff_tb"
    ALL_ID="SELECT max(staff_id) from staff_tb"


    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_staff(self,staff:Staff)->bool:
        cursor=None
        sid=self.incre_id()
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)#create a cursor object
            cursor.execute(self.INSERT_STAFF,
                           (sid,
                            staff.get_staff_name,
                           staff.get_DOB,
                           staff.get_age,
                           staff.get_email,
                           staff.get_phone,
                           staff.get_address,
                           staff.get_experience,
                           staff.get_date_joining,
                           staff.get_role_id,
                           staff.get_username,
                           staff.get_passwrd,
                           staff.get_is_active,
                           staff.get_created_at,
                           staff.get_gender))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting product:",e)
            return False
        finally:
            if cursor:
                cursor.close()
    
    def display_all_staffs(self) -> List[Staff]:
        staff_list = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM staff_tb"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for row in rows:
                staff = Staff(
                    staff_id=row.get('staff_id'),
                    staff_name=row.get('staff_name'),
                    DOB=row.get('DOB'),
                    age=row.get('age'),
                    email=row.get('email'),
                    phone=row.get('phone'),
                    address=row.get('address'),
                    experience=row.get('experience'),
                    joining_date=row.get('joining_date'),
                    role_id=row.get('role_id'),
                    username=row.get('username'),
                    pass_wrd=row.get('pass_wrd'),
                    is_active=row.get('is_active'),
                    created_at=row.get('created_at'),
                    gender=row.get('gender')
                )
                staff_list.append(staff)
                
        except Exception as e:
            print(f"Error fetching staff: {e}")
        finally:
            cursor.close()
            
        return staff_list

    
    def all_id(self):
        cursor = None
        ids = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT staff_id FROM staff_tb")  # Get all IDs
            rows = cursor.fetchall()
            for row in rows:
                ids.append(row['staff_id'])
        except Exception as e:
            print("Error fetching staff IDs: ", e)
        finally:
            if cursor:
                cursor.close()
        return ids

    
    def incre_id(self):
        ids = self.all_id()
        if not ids:
            return "EMP1000"
        
        numeric_ids = [int(i[3:]) for i in ids if i and i.startswith("EMP")]
        max_id = max(numeric_ids) if numeric_ids else 999  # Safety check
        new_id = max_id + 1
        return f"EMP{new_id:04d}"