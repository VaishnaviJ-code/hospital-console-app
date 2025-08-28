from typing import List, Optional, Dict, Any
from datetime import date, datetime

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
            self.conn.rollback()
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

    def get_daily_appointment_count_from_db(self, doctor_id: str, appointment_date: str) -> int:
        """Get appointment count for doctor on specific date from database"""
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT COUNT(*) as appointment_count
                FROM appointments 
                WHERE doctor_id = %s 
                AND DATE(appointment_date) = %s
                AND status NOT IN ('Cancelled', 'No-show')
            """, (doctor_id, appointment_date))
            
            result = cursor.fetchone()
            return result['appointment_count'] if result else 0
        except Exception as e:
            print(f"Error getting appointment count from DB: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def update_all_doctors_availability(self):
        """Update availability for all doctors based on today's appointments"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            today = date.today().strftime('%Y-%m-%d')
            
            # Get all active doctors
            cursor.execute("""
                SELECT d.doctor_id 
                FROM doctors d
                JOIN staff_tb s ON d.staff_id = s.staff_id
                WHERE s.is_active = 'y'
            """)
            doctors = cursor.fetchall()
            
            for doctor in doctors:
                doctor_id = doctor['doctor_id']
                appointment_count = self.get_daily_appointment_count_from_db(doctor_id, today)
                
                # Update availability status (if you have an availability column)
                # Or just use this information in your booking logic
                print(f"Doctor {doctor_id}: {appointment_count}/25 appointments today")
                
        except Exception as e:
            print(f"Error updating doctors availability: {e}")
        finally:
            if cursor:
                cursor.close()

    def get_doctor_availability_status(self, doctor_id: str, appointment_date: str) -> dict:
        """Get comprehensive availability status for a doctor on a specific date"""
        current_count = self.get_daily_appointment_count_from_db(doctor_id, appointment_date)
        max_appointments = 25
        
        return {
            'doctor_id': doctor_id,
            'date': appointment_date,
            'current_appointments': current_count,
            'max_appointments': max_appointments,
            'available_slots': max_appointments - current_count,
            'is_available': current_count < max_appointments,
            'availability_percentage': round((current_count / max_appointments) * 100, 1)
        }

    def save_consultation_bill(self, bill_data: Dict[str, Any]) -> bool:
        """Save consultation bill to database"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            # Extract individual charges from bill items
            consultation_fee = 0.0
            op_charge = 0.0
            registration_charge = 0.0
            
            for item in bill_data["items"]:
                if item["description"] == "Consultation Fee":
                    consultation_fee = item["amount"]
                elif item["description"] == "OP Charge":
                    op_charge = item["amount"]
                elif item["description"] == "Registration Charge":
                    registration_charge = item["amount"]
            
            # Insert bill into database
            insert_bill_query = """
                INSERT INTO consultation_bill (
                    bill_id, patient_id, patient_name, doctor_id, doctor_name,
                    appointment_id, consultation_fee, op_charge, registration_charge, 
                    total_amount, bill_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                bill_data["bill_id"],
                bill_data["patient_id"],
                bill_data.get("patient_name", ""),
                bill_data["doctor_id"],
                bill_data.get("doctor_name", ""),
                bill_data.get("appointment_id", None),
                consultation_fee,
                op_charge,
                registration_charge,
                bill_data["total_amount"],
                bill_data["date"]
            )
            
            cursor.execute(insert_bill_query, params)
            self.conn.commit()
            
            print(f"Bill saved to database: {bill_data['bill_id']}")
            return True
            
        except Exception as e:
            print(f"Error saving bill to database: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def get_consultation_bill(self, bill_id: str) -> Optional[Dict]:
        """Retrieve consultation bill by ID"""
        cursor = None
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM consultation_bill WHERE bill_id = %s", (bill_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error retrieving bill: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def list_patient_bills(self, patient_id: str) -> List[Dict]:
        """Get all bills for a specific patient"""
        cursor = None
        bills = []
        try:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT * FROM consultation_bill 
                WHERE patient_id = %s 
                ORDER BY bill_date DESC
            """, (patient_id,))
            bills = cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving patient bills: {e}")
        finally:
            if cursor:
                cursor.close()
        return bills

