from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from models.appointment import Appointments
from models.patient import Patient


class ReceptionistBase(ABC):
    """
    Abstract base class for Receptionist role.
    Defines responsibilities such as managing patients and appointments.
    """

    # Patient Management

    @abstractmethod
    def add_patient(self, patient_data: Dict[str, Any]) -> int:
        """
        Add a new patient to the database.
        :param patient_data: Dictionary containing patient details 
                             (e.g., name, age, gender, address, phone).
        :return: Newly created patient_id.
        """
        pass

    @abstractmethod
    def update_patient_name(self, patient_id: int, new_name: str) -> bool:
        """
        Update the patient's name.
        :return: True if update successful, False otherwise.
        """
        pass

    @abstractmethod
    def update_patient_address(self, patient_id: int, new_address: str) -> bool:
        """
        Update the patient's address.
        :return: True if update successful, False otherwise.
        """
        pass

    @abstractmethod
    def update_patient_phone(self, patient_id: int, new_phone: str) -> bool:
        """
        Update the patient's phone number.
        :return: True if update successful, False otherwise.
        """
        pass

    @abstractmethod
    def search_patient_by_id(self, patient_id: int) -> Patient:
        """
        Retrieve patient details by ID.
        :return: Patient record dict if found, else None.
        """
        pass

    @abstractmethod
    def search_patient_by_phone(self, patient_phone: str) -> Patient:
        """
        Retrieve patient details by phone number.
        :return: Patient record dict if found, else None.
        """
        pass

    @abstractmethod
    def list_patients(self) -> List[Patient]:
        """
        Return all patients in the database.
        """
        pass

    # Appointment Management

    @abstractmethod
    def book_appointment(self, appointment_data: Dict[str, Any]) -> int:
        """
        Book a new appointment.
        :param appointment_data: Dictionary with details such as 
                                 patient_id, doctor_id, date, time, reason.
        :return: Newly created appointment_id.
        """
        pass

    @abstractmethod
    def search_appointment_by_id(self, appointment_id: int) -> Appointments:
        """
        Retrieve appointment details by ID.
        :return: Appointment record dict if found, else None.
        """
        pass

    @abstractmethod
    def list_appointments(self) -> List[Appointments]:
        """
        Return all appointments in the system.
        """
        pass
