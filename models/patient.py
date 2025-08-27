from datetime import datetime

class Patient:
    """
    Patient Model representing 'patients' table in the database.
    Encapsulates patient attributes with getters and setters.
    """
    # id_ini = 1000

    def __init__(self, patient_id: str, patient_name: str, dob: str, gender: str,
                 phone: str, address: str, email: str, registration_date: datetime = None):
        
        self.__patient_id = patient_id
        self.__patient_name = patient_name
        self.__dob = dob
        self.__gender = gender
        self.__phone = phone
        self.__address = address
        self.__email = email
        self.__registration_date = registration_date if registration_date else datetime.now()

    # Getters

    def get_patient_id(self) -> str:
        return self.__patient_id

    def get_patient_name(self) -> str:
        return self.__patient_name

    def get_dob(self) -> str:
        return self.__dob

    def get_gender(self) -> str:
        return self.__gender

    def get_phone(self) -> str:
        return self.__phone

    def get_address(self) -> str:
        return self.__address

    def get_email(self) -> str:
        return self.__email

    def get_registration_date(self) -> datetime:
        return self.__registration_date

    # Setters

    def set_patient_name(self, name: str):
        self.__patient_name = name

    def set_dob(self, dob: str):
        self.__dob = dob

    def set_gender(self, gender: str):
        self.__gender = gender

    def set_phone(self, phone: str):
        self.__phone = phone

    def set_address(self, address: str):
        self.__address = address

    def set_email(self, email: str):
        self.__email = email

    # Utility 

    def to_dict(self) -> dict:
        """Convert patient object to dict (useful for DB insert/update)"""
        return {
            "patient_id": self.__patient_id,
            "patient_name": self.__patient_name,
            "dob": self.__dob,
            "gender": self.__gender,
            "phone": self.__phone,
            "address": self.__address,
            "email": self.__email,
            "registration_date": self.__registration_date
        }

    # @staticmethod
    # def patient_id_gen():
    #     Patient.id_ini+=1
    #     id="PAT"+str(Patient.id_ini) 
    #     return id
    
    def __str__(self):
        return f"Patient[{self.__patient_id}] - {self.__patient_name}, {self.__dob}, {self.__gender}, {self.__phone}, {self.__address}, {self.__registration_date}"

