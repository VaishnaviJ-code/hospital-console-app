from abc import ABC, abstractmethod
from typing import Any, Dict
from models.pharmacist import Medicine

class PharmacistDAO(ABC):

    @abstractmethod
    def add_medicine(self, medicine):
        pass

    @abstractmethod
    def display_all_medicines(self) -> list[Medicine]:
        pass

    @abstractmethod
    def update_medicine(self, med_id: str, name: str, med_type: str, price: float, stock: int, expiry_date: str, available: str) -> bool:
        pass

    @abstractmethod
    def delete_medicine(self, med_id: str) -> bool:
        pass

    @abstractmethod
    def get_medicine_by_id(self, med_id: str):
        pass

    @abstractmethod
    def dispense_medicine(self, prescription_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate_medicine_id(self) -> str:
        pass

    @abstractmethod
    def generate_sale_id(self) -> str:
        pass
