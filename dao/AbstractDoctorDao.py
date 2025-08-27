from abc import ABC, abstractmethod
from typing import List
from models.Doctor import Doctor

class DoctorDaoService(ABC):
    @abstractmethod
    def view_appointments(self, doctor_id:int):
        'View all appointments'
        pass

    @abstractmethod
    def add_consultation(self, appointment_id, patient_id, doctor_id, diagnosis, treatment, medical_recordscol):
        pass

    @abstractmethod
    def add_prescription(self, record_id, doctor_id, patient_id) -> str:
        """Add a new prescription and return the prescription_id"""
        pass

    @abstractmethod
    def add_prescription_medicine(self, prescription_id, medicine_id, dosage, duration):
        pass

    @abstractmethod
    def add_prescription_test(self, prescription_id, patient_id, doctor_id, test_id, status='Pending'):
        pass