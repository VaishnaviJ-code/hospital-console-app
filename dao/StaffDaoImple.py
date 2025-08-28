from dao.StaffDaoAbstract import StaffDaoServices
from models.staff import Staff
from typing import List
from database.connection import DBConnection
import pymysql

class StaffDaoImple(StaffDaoServices):
    INSERT_STAFF="INSERT into staff_tb(staff_id,staff_name,DOB,age,email,phone,address,experience,joining_date,role_id,username,pass_wrd,is_active,created_at,gender) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    DISPLAY_ALL="SELECT * from staff_tb"
    ALL_ID="SELECT staff_id from staff_tb"
    UPDATE_STAFF_NAME="UPDATE staff_tb set staff_name=%s where staff_id=%s"
    SEARCH_ID="SELECT * from staff_tb where staff_id=%s" 
    UPDATE_STAFF_EMAIL="UPDATE staff_tb set email=%s where staff_id=%s"
    UPDATE_STAFF_ROLE="UPDATE staff_tb set role_id=%s where staff_id=%s"
    UPDATE_STAFF_PHNO="UPDATE staff_tb set phone=%s where staff_id=%s"
    UPDATE_STAFF_ADDRS="UPDATE staff_tb set address=%s where staff_id=%s"
    UPDATE_STAFF_USERNAME="UPDATE staff_tb set username=%s where staff_id=%s"
    UPDATE_STAFF_PASSWRD="UPDATE staff_tb set pass_wrd=%s where staff_id=%s"
    SUSPEND_STAFF="UPDATE staff_tb set is_active='n' where staff_id=%s"
    ENABLE_STAFF="UPDATE staff_tb set is_active='n' where staff_id=%s"


    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_staff(self,staff:Staff)->bool:
        cursor=None
        try:
            sid=StaffDaoImple.incre_id(self)
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
            cursor.close()
    
    def display_all_staffs(self)->List[Staff]:
        staff = []#To store the records from db
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)#return data in dictionary format
            cursor.execute(self.DISPLAY_ALL)#fire the query
            rows = cursor.fetchall()
            for row in rows:
                staff.append(Staff(staff_id=row['staff_id'],staff_name=row['staff_name'],DOB=row['DOB'],age=row['age'],email=row['email'],
                                   phone=row['phone'],address=row['address'],experience=row['experience'],joining_date=row['joining_date'],
                                   role_id=row['role_id'],username=row['username'],pass_wrd=row['pass_wrd'],is_active=row['is_active'],
                                   created_at=row['created_at'],gender=row['gender']))
        
        except Exception as e:
            print("Error fetching products: ",e)
        
        finally:
            cursor.close()
        
        return staff
    
    def all_id(self):
        ids = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)  
            cursor.execute(self.ALL_ID)  
            rows = cursor.fetchall()
            for row in rows:
                ids.append(row['staff_id']) 
        except Exception as e:
            print("Error fetching staff IDs: ", e)
        finally:
            cursor.close()
    
        return ids

    
    def incre_id(self):
        ids = self.all_id()
        if not ids:
            return "EMP1000"

        numeric_ids = [int(i[3:]) for i in ids if i.startswith("EMP")]
        max_id = max(numeric_ids)
        new_id = max_id + 1

        return f"EMP{new_id:04d}" 

    def search_staff(self, staff_id):
        staff=None
        try:
            cursor=self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.SEARCH_ID,(staff_id,))
            row=cursor.fetchone()
            if row:
                staff=Staff(staff_id=row["staff_id"],
                            staff_name=row["staff_name"],
                            is_active=row["is_active"])
        except Exception as e:
            print("Error finding product: ",e)
        finally:
            cursor.close()
        return staff

    def update_staff_name(self,staff:Staff,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.UPDATE_STAFF_NAME,(staff.get_staff_name,staff_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in updating staff name: ",e)
            return False
        finally:
            cursor.close()

    def update_staff_email(self,staff:Staff,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.UPDATE_STAFF_EMAIL,(staff.get_email,staff_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in updating staff email: ",e)
            return False
        finally:
            cursor.close()

    def update_staff_role(self,staff:Staff,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.UPDATE_STAFF_ROLE,(staff.get_role_id,staff_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in updating staff role: ",e)
            return False
        finally:
            cursor.close()

    def update_staff_phno(self,staff:Staff,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.UPDATE_STAFF_PHNO,(staff.get_phone,staff_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in updating staff phone number: ",e)
            return False
        finally:
            cursor.close()       
    
    def update_staff_addrs(self,staff:Staff,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.UPDATE_STAFF_ADDRS,(staff.get_address,staff_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in updating staff address: ",e)
            return False
        finally:
            cursor.close()
    
    def update_staff_username(self,staff:Staff,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.UPDATE_STAFF_USERNAME,(staff.get_username,staff_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in updating username: ",e)
            return False
        finally:
            cursor.close()    
    
    def update_staff_psswrd(self,staff:Staff,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.UPDATE_STAFF_PASSWRD,(staff.get_passwrd,staff_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in updating staff psswrd: ",e)
            return False
        finally:
            cursor.close()    

    def suspend_staff(self,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.SUSPEND_STAFF,(staff_id,))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in suspending staff: ",e)
            return False
        finally:
            cursor.close()        

    def enable_staff(self,staff_id)->bool:
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.ENABLE_STAFF,(staff_id,))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print("Error in enabling staff: ",e)
            return False
        finally:
            cursor.close()  