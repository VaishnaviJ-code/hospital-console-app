from abc import ABC, abstractmethod
from typing import List
from models.Doctor import Doctor

class DoctorDaoService(ABC):
    @abstractmethod
    def view_appointments(self, doctor_id:int):
        'View all appointments'
        pass
