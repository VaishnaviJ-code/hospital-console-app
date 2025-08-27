from datetime import datetime

class Appointments:

    """
    Appointment model maps to the 'appointments' table in the database.
    """
    # id_ini = 1000
    
    def __init__(self, appointment_id: str, patient_id: str, doctor_id: str, token:int, status:str, appointment_date:datetime=None):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__token = token
        self.__status = status
        self.__appointment_date = appointment_date or datetime.now()

    # Getters

    def get_appointment_id(self) -> str:
        return self.__appointment_id
    
    def get_patient_id(self) -> str:
        return self.__patient_id
    
    def get_doctor_id(self) -> str:
        return self.__doctor_id
    
    def get_token(self) -> int:
        return self.__token
    
    def get_status(self) -> str:
        return self.__status
    
    def get_appointment_date(self) -> datetime:
        return self.__appointment_date
    
    # Setters

    def set_status(self, status: str):
        self.__status = status

    def set_appointment_date(self, new_date: datetime):
        self.__appointment_date = new_date

    def set_doctor_id(self, new_doc: int):
        self.__doctor_id = new_doc

    def set_token(self, new_token: int): 
        self.__token = new_token

    # Utility

    def to_dict(self) -> dict:
        """Convert appointment object to dict (useful for DB insert/update)"""
        return {
            "appointment_id": self.__appointment_id,
            "patient_id": self.__patient_id,
            "doctor_id": self.__doctor_id,
            "token": self.__token,
            "status": self.__status,
            "appointment_date": self.__appointment_date
        }

    # @staticmethod
    # def appointment_id_gen():
    #     Appointments.id_ini+=1
    #     id="AP"+str(Appointments.id_ini) 
    #     return id
    
    def __str__(self):
        return f"Appointment[{self.__appointment_id}] - {self.__patient_id}, {self.__doctor_id}, {self.__token}, {self.__status}, {self.__appointment_date}"