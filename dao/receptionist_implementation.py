from typing import List, Optional, Dict, Any
from datetime import datetime

import pymysql

from database.connection import DBConnection
from models.patient import Patient
from models.appointment import Appointments
from dao.abstract_receptionist import ReceptionistBase


class ReceptionistDaoImplementation(ReceptionistBase):
    """Implementation of ReceptionistBase using DB queries."""

    # SQL QUERIES 
    INSERT_PATIENT = """
        INSERT INTO patients (patient_id, patient_name, dob, gender, phone, address, email, registration_date)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
    """
    UPDATE_PATIENT_NAME = "UPDATE patients SET patient_name = %s WHERE patient_id = %s"
    UPDATE_PATIENT_ADDRESS = "UPDATE patients SET address = %s WHERE patient_id = %s"
    UPDATE_PATIENT_PHONE = "UPDATE patients SET phone = %s WHERE patient_id = %s"
    SEARCH_PATIENT_BY_ID = "SELECT * FROM patients WHERE patient_id = %s"
    SEARCH_PATIENT_BY_PHONE = "SELECT * FROM patients WHERE phone = %s"
    LIST_PATIENTS = "SELECT * FROM patients"

    INSERT_APPOINTMENT = """
        INSERT INTO appointments (appointment_id, patient_id, doctor_id, token, status, appointment_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    SEARCH_APPOINTMENT_BY_ID = "SELECT * FROM appointments WHERE appointment_id = %s"
    LIST_APPOINTMENTS = "SELECT * FROM appointments"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    # PATIENT MANAGEMENT 
    def add_patient(self, patient_data: Dict[str, Any]) -> int:
        cursor = None
        pid=self.incre_pat_id()
        try:
            cursor = self.conn.cursor()

            phone = str(patient_data.get("phone", ""))
            if 'e+' in phone or 'e-' in phone:  # Handle scientific notation
                phone = f"{int(float(phone)):010d}"  # Convert to 10-digit string

            # custom_patient_id = Patient.patient_id_gen()
            params = (
                pid,
                patient_data.get("patient_name"),
                patient_data.get("dob"),
                patient_data.get("gender"),
                phone,
                patient_data.get("address"),
                patient_data.get("email"),
                datetime.now()
            )
            cursor.execute(self.INSERT_PATIENT,params)
            self.conn.commit()
            return pid if cursor.rowcount == 1 else -1
        except Exception as e:
            print("Error inserting patient:", e)
            return -1
        finally:
            if cursor:
                cursor.close()

    def update_patient_name(self, patient_id: str, new_name: str) -> bool:
        return self._execute_update(self.UPDATE_PATIENT_NAME, (new_name, patient_id))

    def update_patient_address(self, patient_id: str, new_address: str) -> bool:
        return self._execute_update(self.UPDATE_PATIENT_ADDRESS, (new_address, patient_id))

    def update_patient_phone(self, patient_id: str, new_phone: str) -> bool:
        return self._execute_update(self.UPDATE_PATIENT_PHONE, (new_phone, patient_id))

    def search_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        return self._fetch_one(self.SEARCH_PATIENT_BY_ID, (patient_id,), Patient)

    def search_patient_by_phone(self, patient_phone: str) -> Optional[Patient]:
        return self._fetch_one(self.SEARCH_PATIENT_BY_PHONE, (patient_phone,), Patient)

    def list_patients(self) -> List[Patient]:
        return self._fetch_all(self.LIST_PATIENTS, Patient)

    # APPOINTMENT MANAGEMENT
    def book_appointment(self, appointment_data: Dict[str, Any]) -> int:
        cursor = None
        aptid=self.incre_apt_id()
        try:
            cursor = self.conn.cursor()

            params = (
                aptid,
                appointment_data.get("patient_id"),
                appointment_data.get("doctor_id"),
                appointment_data.get("token"),
                appointment_data.get("status", "Scheduled"),
                appointment_data.get("appointment_date", datetime.now())
            )

            cursor.execute(self.INSERT_APPOINTMENT, params)
            self.conn.commit()
            return aptid if cursor.rowcount == 1 else -1
        except Exception as e:
            print("Error booking appointment:", e)
            return -1
        finally:
            if cursor:
                cursor.close()

    def search_appointment_by_id(self, appointment_id: str) -> Optional[Appointments]:
        return self._fetch_one(self.SEARCH_APPOINTMENT_BY_ID, (appointment_id,), Appointments)

    def list_appointments(self) -> List[Appointments]:
        return self._fetch_all(self.LIST_APPOINTMENTS, Appointments)

    # HELPER METHODS 
    def _execute_update(self, query: str, params: tuple) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("DB Update Error:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def _fetch_one(self, query: str, params: tuple, model_class) -> Optional[Any]:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                return model_class(**row)
            return None
        except Exception as e:
            print("DB Fetch One Error:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def _fetch_all(self, query: str, model_class) -> List[Any]:
        cursor = None
        results = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                results.append(model_class(**row))
        except Exception as e:
            print("DB Fetch All Error:", e)
        finally:
            if cursor:
                cursor.close()
        return results
    
    def patient_id(self):
        cursor = None
        ids = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT patient_id FROM patients")  # Get all IDs
            rows = cursor.fetchall()
            for row in rows:
                ids.append(row['patient_id'])
        except Exception as e:
            print("Error fetching patient IDs: ", e)
        finally:
            if cursor:
                cursor.close()
        return ids

    
    def incre_pat_id(self):
        ids = self.patient_id()
        if not ids:
            return "PAT1000"
        
        numeric_ids = [int(i[3:]) for i in ids if i and i.startswith("PAT")]
        max_id = max(numeric_ids) if numeric_ids else 999  # Safety check
        new_id = max_id + 1
        return f"PAT{new_id:04d}"
    
    def appointment_id(self):
        cursor = None
        ids = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT appointment_id FROM appointments")  # Get all IDs
            rows = cursor.fetchall()
            for row in rows:
                ids.append(row['appointment_id'])
        except Exception as e:
            print("Error fetching appointment IDs: ", e)
        finally:
            if cursor:
                cursor.close()
        return ids

    
    def incre_apt_id(self):
        ids = self.appointment_id()
        if not ids:
            return "APT1000"
        
        numeric_ids = [int(i[3:]) for i in ids if i and i.startswith("APT")]
        max_id = max(numeric_ids) if numeric_ids else 999  # Safety check
        new_id = max_id + 1
        return f"APT{new_id:04d}"
    
    def get_appointment_with_fee(self, appointment_id: str) -> Optional[Dict]:
        """Get appointment details with consultation fee"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            
            query = """
            SELECT a.appointment_id, a.patient_id, a.doctor_id, a.token, 
                a.status, a.appointment_date, d.consultation_fee
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_id = %s
            """
            
            cursor.execute(query, (appointment_id,))
            result = cursor.fetchone()
            
            return result
            
        except Exception as e:
            print(f"Error fetching appointment with fee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

