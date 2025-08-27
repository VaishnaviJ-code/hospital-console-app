from abc import ABC, abstractmethod
from models.pharmacist import Medicine

class PharmacistDAO(ABC):
    @abstractmethod
    def add_medicine(self, medicine):
        pass
    @abstractmethod
    def display_all_medicines(self) -> list[Medicine]:
        pass
