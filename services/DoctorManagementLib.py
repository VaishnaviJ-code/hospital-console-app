from dao.AbstractDoctorDao import DoctorDaoService
from dao.DoctorDaoImple import DoctorDaoImplementation
from datetime import datetime, date
from models.Doctor import Doctor
from dao.DoctorCreateDaoImple import DoctorCreateDaoImple

class DoctorManagementLib:
    """Handles CRUD logic for doctor operations"""
    
    dao_service: DoctorDaoService = DoctorDaoImplementation()

    @staticmethod
    def resolve_doctor_id_for_staff(staff_id: str) -> str:
        """Return the doctor_id mapped to a given staff_id, or empty string if not found."""
        try:
            dao = DoctorCreateDaoImple()
            doctors = dao.display_all_doctors()
            for doc in doctors:
                if str(doc.get_staff_id) == str(staff_id):
                    return str(doc.get_doc_id)
        except Exception as e:
            print("Error resolving doctor id:", e)
        return ""

    @staticmethod
    def view_appointments(doctor_id: str):
        try:
            appointments = DoctorManagementLib.dao_service.view_appointments(doctor_id)
            if appointments:
                print("-" * 47)
                print(f"WELCOME DOCTOR : {doctor_id}")
                print(f"Appointments for Doctor ID : {doctor_id}")
                for app in appointments:
                    print("-" * 47)
                    print(f"Appointment ID : {app.get('appointment_id')}")
                    print(f"Patient ID : {app.get('patient_id')}")
                    print(f"Token : {app.get('token')}")
                    print(f"Status : {app.get('status')}")
                    print(f"Appointment Date: {app.get('appointment_date')}")
                    print("-" * 47)
            else:
                print("No appointments found for this doctor!")
        except Exception as e:
            print("Error viewing appointments:", e)

    @staticmethod
    def get_todays_appointments(doctor_id: str):
        try:
            appointments = DoctorManagementLib.dao_service.view_appointments(doctor_id)
            today = date.today()
            todays_appointments = [
                app for app in appointments
                if app.get('appointment_date').date() == today
            ]

            if todays_appointments:
                print("-" * 47)
                print(f"WELCOME DOCTOR : {doctor_id}")
                print(f"Today's Appointments for Doctor ID : {doctor_id}")
                for app in todays_appointments:
                    print("-" * 47)
                    print(f"Appointment ID : {app.get('appointment_id')}")
                    print(f"Patient ID : {app.get('patient_id')}")
                    print(f"Token : {app.get('token')}")
                    print(f"Status : {app.get('status')}")
                    print(f"Appointment Date: {app.get('appointment_date')}")
                    print("-" * 47)
            else:
                print("No appointments found for today!")
        except Exception as e:
            print("Error viewing today's appointments:", e)

    @staticmethod
    def consult_patient(doctor_id: str):
        print("\n--- Consult a Patient ---")
        try:
            appointment_id = input("Enter appointment ID: ").strip()
            patient_id = input("Enter patient ID: ").strip()
            diagnosis = input("Enter diagnosis: ").strip()
            treatment = input("Enter treatment notes: ").strip()
            medical_recordscol = input("Enter medical records file path or notes (optional): ").strip()

            if not all([appointment_id, patient_id, doctor_id, diagnosis, treatment]):
                print("Error: All fields except medical records are required.")
                return

            record_id = DoctorManagementLib.dao_service.add_consultation(
                appointment_id,
                patient_id,
                doctor_id,
                diagnosis,
                treatment,
                medical_recordscol
            )
            
            if record_id:
                print(f"Consultation successfully recorded with ID: {record_id}")
                
                # Offer to add prescription
                add_prescription = input("Would you like to add a prescription for this consultation? (y/n): ").strip().lower()
                if add_prescription == 'y':
                    DoctorManagementLib.add_prescription_for_record(record_id, doctor_id, patient_id)
            else:
                print("Failed to record consultation.")

        except Exception as e:
            print(f"Error during consultation: {e}")

    @staticmethod
    def add_prescription_full(doctor_id: str):
        print("\n--- Add Prescription ---")
        try:
            record_id = input("Enter consultation record ID: ").strip()
            patient_id = input("Enter patient ID: ").strip()
            
            if not all([record_id, patient_id]):
                print("Error: Record ID and Patient ID are required.")
                return

            DoctorManagementLib.add_prescription_for_record(record_id, doctor_id, patient_id)

        except Exception as e:
            print(f"Error during prescription creation: {e}")

    @staticmethod
    def add_prescription_for_record(record_id: str, doctor_id: str, patient_id: str):
        """Helper method to add prescription with medicines and tests"""
        try:
            prescription_id = DoctorManagementLib.dao_service.add_prescription(
                record_id, doctor_id, patient_id
            )

            if not prescription_id:
                print("Failed to add prescription.")
                return

            print(f"Prescription created with ID: {prescription_id}")

            # Add medicines
            medicines = DoctorManagementLib.dao_service.get_medicines_list()
            if medicines:
                print("\nAvailable medicines:")
                for med in medicines[:10]:  # Show first 10
                    print(f"ID: {med['med_id']}, Name: {med['name']}, Type: {med['med_type']}")
                if len(medicines) > 10:
                    print(f"... and {len(medicines) - 10} more medicines")

            while True:
                add_med = input("\nAdd medicine? (y/n): ").strip().lower()
                if add_med != 'y':
                    break
                    
                medicine_id = input("Enter medicine ID: ").strip()
                dosage = input("Enter dosage: ").strip()
                duration = input("Enter duration: ").strip()

                if DoctorManagementLib.dao_service.add_prescription_medicine(
                    prescription_id, medicine_id, dosage, duration
                ):
                    print("Medicine added successfully.")
                else:
                    print("Failed to add medicine.")

            # Add tests
            tests = DoctorManagementLib.dao_service.get_tests_list()
            if tests:
                print("\nAvailable tests:")
                for test in tests:
                    print(f"ID: {test['test_id']}, Name: {test['test_name']}")

            while True:
                add_test = input("\nAdd test? (y/n): ").strip().lower()
                if add_test != 'y':
                    break
                    
                test_id = input("Enter test ID: ").strip()

                if DoctorManagementLib.dao_service.add_prescription_test(
                    prescription_id, patient_id, doctor_id, test_id
                ):
                    print("Test added successfully.")
                else:
                    print("Failed to add test.")

            print("Prescription with medicines and tests saved successfully.")

        except Exception as e:
            print(f"Error creating prescription: {e}")

    @staticmethod
    def view_patient_history(patient_id: str):
        """View patient's medical history"""
        try:
            history = DoctorManagementLib.dao_service.get_patient_medical_history(patient_id)
            if history:
                print(f"\n--- Medical History for Patient {patient_id} ---")
                for record in history:
                    print(f"Record ID: {record['record_id']}")
                    print(f"Date: {record['record_date']}")
                    print(f"Diagnosis: {record['diagnosis']}")
                    print(f"Treatment: {record['treatment']}")
                    print("-" * 50)
            else:
                print("No medical history found for this patient.")
        except Exception as e:
            print(f"Error viewing patient history: {e}")

    @staticmethod
    def view_prescription_details(prescription_id: str):
        """View complete prescription details"""
        try:
            details = DoctorManagementLib.dao_service.get_prescription_details(prescription_id)
            if details:
                print(f"\n--- Prescription Details for {prescription_id} ---")
                print(f"Patient ID: {details['prescription']['patient_id']}")
                print(f"Issued Date: {details['prescription']['issued_date']}")
                
                print("\nMedicines:")
                for med in details['medicines']:
                    print(f"- {med['name']} ({med['med_type']}) - {med['dosage']} for {med['duartion']}")
                    
                print("\nTests:")
                for test in details['tests']:
                    print(f"- {test['test_name']} - Status: {test['status']}")
            else:
                print("Prescription not found.")
        except Exception as e:
            print(f"Error viewing prescription details: {e}")
