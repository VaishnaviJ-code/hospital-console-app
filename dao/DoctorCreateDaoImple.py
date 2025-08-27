from dao.AbstractDoctorCreateDao import DoctorCreateDaoServices
from models.Doctor import Doctor
from typing import List
from database.connection import DBConnection
import pymysql

class DoctorCreateDaoImple(DoctorCreateDaoServices):
    INSERT_STAFF="INSERT into doctors(doctor_id,staff_id,dept_id,sp_id,consultation_fee) VALUES (%s,%s,%s,%s,%s)"
    DISPLAY_ALL_DOC="SELECT * from doctors"
    ALL_ID="SELECT max(staff_id) from staff_tb"


    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_doctor(self,doc:Doctor)->bool:
        cursor=None
        # sid=StaffDaoImple.incre_id(self)
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)#create a cursor object
            cursor.execute(self.INSERT_STAFF,
                           (doc.get_doc_id,
                            doc.get_staff_id,
                            doc.get_dept_id,
                            doc.get_spcl_id,
                            doc.get_consultation_fee))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting doctor:",e)
            return False
        finally:
            cursor.close()
    
    def display_all_doctors(self) -> List[Doctor]:
        doc_list = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.DISPLAY_ALL_DOC)
            rows = cursor.fetchall()
            
            for row in rows:
                doc = Doctor(doctor_id=row["doctor_id"],
                    staff_id=row["staff_id"],
                    dept_id=row["dept_id"],
                    sp_id = row["sp_id"],
                    consultation_fee=row["consultation_fee"]
                    )
                doc_list.append(doc)
                
        except Exception as e:
            print(f"Error fetching doctors: {e}")
        finally:
            cursor.close()
            
        return doc_list

    
    # def all_id(self):
    #     ids = []#To store the records from db
    #     try:
    #         cursor = self.conn.cursor(pymysql.cursors.DictCursor)#return data in dictionary format
    #         cursor.execute(self.ALL_ID)#fire the query
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             ids.append(Staff(staff_id=row['staff_id'],))
        
    #     except Exception as e:
    #         print("Error fetching products: ",e)
        
    #     finally:
    #         cursor.close()
        
    #     return ids
    
    # def incre_id(self):
    #     ids=StaffDaoImple.all_id(self)
    #     id=0
    #     for i in ids:
    #         if id==0:
    #             x=i[3:]
    #             print(x)
    #             id=int(x)+1
    #             print(id)
    #     return id