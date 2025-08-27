from dao.AbstractDoctorDao import DoctorDaoService
from database.connection import DBConnection
from models.Doctor import Doctor
from typing import List
import pymysql  # type: ignore

class DoctorDaoImplementation(DoctorDaoService):
    'Implementation for abstract class'
    #SQL Queries
    VIEW_APPOINTMENTS = "SELECT * FROM appointments WHERE doctor_id=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def view_appointments(self, doctor_id:int):
        try:
            # appointments = []
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.VIEW_APPOINTMENTS,(doctor_id, ))
            rows = cursor.fetchall()
            # for row in rows:
            #     appointments.append()
            return rows
        except Exception as e:
            print("Error viewing appointments : ",e)
            return[]
        finally:
            cursor.close()
        
        