from dao.AbstractDoctorDao import DoctorDaoService
from database.connection import DBConnection
from models.Doctor import Doctor
from typing import List
import pymysql  # type: ignore
from datetime import datetime

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
        
    def add_consultation(self, appointment_id, patient_id, doctor_id, diagnosis, treatment, medical_recordscol):
        try:
            with self.conn.cursor() as cursor:
                record_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_record_id = DoctorDaoImplementation.generate_new_record_id(self.conn)
                query = """
                    INSERT INTO medical_records 
                    (record_id, appointment_id, patient_id, doctor_id, diagnosis, treatment, record_date, medical_recordscol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    new_record_id,
                    appointment_id,
                    patient_id,
                    doctor_id,
                    diagnosis,
                    treatment,
                    record_date,
                    medical_recordscol
                ))
                self.conn.commit()
                print("Consultation added successfully.")
        except Exception as e:
            print("Error adding consultation:", e)

    def generate_new_record_id(conn):
        with conn.cursor() as cursor:
            cursor.execute("SELECT record_id FROM medical_records ORDER BY record_id DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                last_id = result[0]  # e.g. "REC1001"
                number = int(last_id[3:])  # extract numeric part
                new_number = number + 1
                new_id = f"REC{new_number}"
            else:
                new_id = "REC1000"  # start value if table empty
        return new_id
    
    def add_prescription(self, record_id, doctor_id, patient_id):
        try:
            with self.conn.cursor() as cursor:
                issued_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                prescription_id = self._generate_new_prescription_id()
                query = """
                    INSERT INTO prescriptions
                    (prescription_id, record_id, doctor_id, patient_id, issued_date)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    prescription_id,
                    record_id,
                    doctor_id,
                    patient_id,
                    issued_date
                ))
                self.conn.commit()
                print("Prescription added successfully.")
                return prescription_id
        except Exception as e:
            print("Error adding prescription:", e)
            return None
    def add_prescription_medicine(self, prescription_id, medicine_id, dosage, duration):
        try:
            with self.conn.cursor() as cursor:
                query = """
                    INSERT INTO prescription_medicine
                    (prescription_id, medicine_id, dosage, duration)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (prescription_id, medicine_id, dosage, duration))
                self.conn.commit()
                print(f"Medicine {medicine_id} added to prescription.")
        except Exception as e:
            print("Error adding prescription medicine:", e)

    def add_prescription_test(self, prescription_id, patient_id, doctor_id, test_id, status='Pending'):
        try:
            with self.conn.cursor() as cursor:
                query = """
                    INSERT INTO prescription_test
                    (patient_id, doctor_id, test_id, status, prescription_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (patient_id, doctor_id, test_id, status, prescription_id))
                self.conn.commit()
                print(f"Test {test_id} added to prescription.")
        except Exception as e:
            print("Error adding prescription test:", e)
            
    def _generate_new_prescription_id(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT prescription_id FROM prescriptions ORDER BY prescription_id DESC LIMIT 1")
                result = cursor.fetchone()
                if result and result[0]:
                    last_id = result[0]  # e.g. "PRES1001"
                    number = int(last_id[4:])  # Extract number part after 'PRES'
                    new_number = number + 1
                    new_id = f"PRES{new_number}"
                else:
                    new_id = "PRES1000"
                return new_id
        except Exception as e:
            print("Error generating prescription ID:", e)
            return None
