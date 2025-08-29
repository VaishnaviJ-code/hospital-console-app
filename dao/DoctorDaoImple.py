from dao.AbstractDoctorDao import DoctorDaoService
from database.connection import DBConnection
from models.Doctor import Doctor
from typing import List
import pymysql
from datetime import datetime
import traceback


class DoctorDaoImplementation(DoctorDaoService):
    """Implementation for abstract class"""
    
    # SQL Queries
    VIEW_APPOINTMENTS = "SELECT * FROM appointments WHERE doctor_id=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def view_appointments(self, doctor_id: str):
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(self.VIEW_APPOINTMENTS, (doctor_id, ))
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error viewing appointments: ", e)
            return []
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
                return new_record_id
        except Exception as e:
            print("Error adding consultation:", str(e))
            traceback.print_exc()
            return None

    @staticmethod
    def generate_new_record_id(conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT record_id FROM medical_records ORDER BY record_id DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                last_id = result['record_id']
                number = int(last_id[3:])
                new_number = number + 1
                new_id = f"REC{new_number}"
            else:
                new_id = "REC1000"
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
                # Check if medicine exists first
                cursor.execute("SELECT med_id FROM medicines WHERE med_id = %s", (medicine_id,))
                if not cursor.fetchone():
                    print(f"Error: Medicine {medicine_id} does not exist in medicines table")
                    return False
                
                # Use correct table name from your database schema
                query = """
                    INSERT INTO prescription_medicine
                    (prescription_id, medicine_id, dosage, duration)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (prescription_id, medicine_id, dosage, duration))
                self.conn.commit()
                print(f"Medicine {medicine_id} added to prescription.")
                return True
        except Exception as e:
            print("Error adding prescription medicine:", e)
            return False

    def add_prescription_test(self, prescription_id, patient_id, doctor_id, test_id, status='Pending'):
        try:
            with self.conn.cursor() as cursor:
                # Check if test exists
                cursor.execute("SELECT test_id FROM lab_test WHERE test_id = %s", (test_id,))
                if not cursor.fetchone():
                    print(f"Error: Test {test_id} does not exist in lab_test table")
                    return False
                
                # Use correct table name and columns (no prescription_id column in this table)
                query = """
                    INSERT INTO prescription_test
                    (patient_id, doctor_id, test_id, status)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (patient_id, doctor_id, test_id, status))
                self.conn.commit()
                print(f"Test {test_id} added to prescription.")
                return True
        except Exception as e:
            print("Error adding prescription test:", e)
            return False
            
    def _generate_new_prescription_id(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT prescription_id FROM prescriptions ORDER BY prescription_id DESC LIMIT 1")
                result = cursor.fetchone()
                if result and result['prescription_id']:
                    last_id = result['prescription_id']
                    number = int(last_id[4:])
                    new_number = number + 1
                    new_id = f"PRES{new_number}"
                else:
                    new_id = "PRES1000"
                return new_id
        except Exception as e:
            print("Error generating prescription ID:", e)
            return None

    def get_medicines_list(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM medicines WHERE available = 'y'")
                medicines = cursor.fetchall()
                return medicines
        except Exception as e:
            print("Error fetching medicines:", e)
            return []

    def get_tests_list(self):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM lab_test WHERE is_active = 'y'")
                tests = cursor.fetchall()
                return tests
        except Exception as e:
            print("Error fetching tests:", e)
            return []

    def get_patient_medical_history(self, patient_id):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    SELECT mr.*, a.appointment_date 
                    FROM medical_records mr
                    JOIN appointments a ON mr.appointment_id = a.appointment_id
                    WHERE mr.patient_id = %s 
                    ORDER BY mr.record_date DESC
                """
                cursor.execute(query, (patient_id,))
                records = cursor.fetchall()
                return records
        except Exception as e:
            print("Error fetching patient medical history:", e)
            return []

    def get_prescription_details(self, prescription_id):
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # Get prescription info
                cursor.execute("SELECT * FROM prescriptions WHERE prescription_id = %s", (prescription_id,))
                prescription = cursor.fetchone()
                
                if prescription:
                    # Get medicines
                    cursor.execute("""
                        SELECT pm.*, m.name, m.med_type 
                        FROM prescription_medicine pm
                        JOIN medicines m ON pm.medicine_id = m.med_id
                        WHERE pm.prescription_id = %s
                    """, (prescription_id,))
                    medicines = cursor.fetchall()
                    
                    # Get tests  
                    cursor.execute("""
                        SELECT pt.*, lt.test_name, lt.description
                        FROM prescription_test pt
                        JOIN lab_test lt ON pt.test_id = lt.test_id
                        WHERE pt.patient_id = %s AND pt.doctor_id = %s
                    """, (prescription['patient_id'], prescription['doctor_id']))
                    tests = cursor.fetchall()
                    
                    return {
                        'prescription': prescription,
                        'medicines': medicines,
                        'tests': tests
                    }
                return None
        except Exception as e:
            print("Error fetching prescription details:", e)
            return None
