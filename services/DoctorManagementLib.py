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
