from dao.AbstractDoctorDao import DoctorDaoService
from dao.DoctorDaoImple import DoctorDaoImplementation
from datetime import datetime
from models.Doctor import Doctor

class DoctorManagementLib:
    'Handles CRUD logic'
    dao_service:DoctorDaoService = DoctorDaoImplementation()

    # @staticmethod
    # def generate_doctor_id():
    #     new_id = Doctor.doctor_id_gen()
    #     return new_id

    @staticmethod
    def view_appointments():
        try:
            doctor_id = input("Enter Doctor ID to view appointments : ")
            appointmets = DoctorManagementLib.dao_service.view_appointments(doctor_id)
            if appointmets:
                print(f"-"*47)
                print(f"|Appointments for Doctor ID : {doctor_id}     ")
                for app in appointmets:
                    print(f"-"*47)
                    print(f"|Appointment ID  : {app.get('appointment_id')}  ")
                    print(f"|Patient ID      : {app.get('patient_id')}     ")
                    print(f"|Appointment Date: {app.get('appointment_date')}")
                    print(f"-"*47)
            else:
                print("No appointments found for this doctor!")
        except ValueError:
            print("Invalid input! Doctor ID must be a number!")
        except Exception as e:
            print("Error viewing appointments : ",e)

    @staticmethod
    def get_todays_appointments():
        try:
            doctor_id = input("Enter Doctor ID to view today's appointments: ")
            appointments = DoctorManagementLib.dao_service.view_appointments(doctor_id)
            today = datetime.today().date()

            todays_appointments = [
                                app for app in appointments
                                if app.get('appointment_date').date() == today
                            ]

            if todays_appointments:
                print(f"-"*47)
                print(f"|Today's Appointments for Doctor ID : {doctor_id} ")
                for app in todays_appointments:
                    print(f"-"*47)
                    print(f"|Appointment ID  : {app.get('appointment_id')}       ")
                    print(f"|Patient ID      : {app.get('patient_id')}          ")
                    print(f"|Appointment Date: {app.get('appointment_date')}     ")
                    print(f"-"*47)
            else:
                print("No appointments found for today!")
        except ValueError:
            print("Invalid input! Doctor ID must be a number!")
        except Exception as e:
            print("Error viewing today's appointments:", e)

    @staticmethod
    def consult_patient():
        print("\n--- Consult a Patient ---")
        try:
            appointment_id = input("Enter appointment ID: ").strip()
            patient_id = input("Enter patient ID: ").strip()
            doctor_id = input("Enter your doctor ID: ").strip()
            diagnosis = input("Enter diagnosis: ").strip()
            treatment = input("Enter treatment notes: ").strip()
            medical_recordscol = input("Enter medical records file path or notes (optional): ").strip()

            if not all([appointment_id, patient_id, doctor_id, diagnosis, treatment]):
                print("Error: All fields except medical records are required.")
                return

            DoctorManagementLib.dao_service.add_consultation(
                appointment_id,
                patient_id,
                doctor_id,
                diagnosis,
                treatment,
                medical_recordscol
            )

            print("Consultation successfully recorded.")

        except Exception as e:
            print(f"Error during consultation: {e}")
    
    @staticmethod
    def add_prescription_full():
        print("\n--- Add Prescription ---")
        record_id = input("Enter consultation record ID: ").strip()
        doctor_id = input("Enter your doctor ID: ").strip()
        patient_id = input("Enter patient ID: ").strip()

        prescription_id = DoctorManagementLib.dao_service.add_prescription(
            record_id,
            doctor_id,
            patient_id
        )
        if not prescription_id:
            print("Failed to add prescription.")
            return

        # Add medicines
        while True:
            add_med = input("Add medicine? (y/n): ").strip().lower()
            if add_med != 'y':
                break
            medicine_id = input("Enter medicine ID: ").strip()
            dosage = input("Enter dosage: ").strip()
            duration = input("Enter duration: ").strip()
            DoctorManagementLib.dao_service.add_prescription_medicine(
                prescription_id, medicine_id, dosage, duration
            )

        # Add tests
        while True:
            add_test = input("Add test? (y/n): ").strip().lower()
            if add_test != 'y':
                break
            test_id = input("Enter test ID: ").strip()
            DoctorManagementLib.dao_service.add_prescription_test(
                prescription_id, patient_id, doctor_id, test_id
            )

        print("Prescription with medicines and tests saved successfully.")
