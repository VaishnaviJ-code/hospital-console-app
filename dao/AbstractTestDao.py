from abc import ABC, abstractmethod
from typing import Dict, List

class TestDaoService(ABC):

    @abstractmethod
    def add_test(self, test):
        pass

    @abstractmethod
    def display_tests(self):
        pass
    
    @abstractmethod
    def update_test(self, test_id: str, test_name: str, description: str, price: float, status: str) -> bool:
        pass
    
    @abstractmethod
    def delete_test(self, test_id: str) -> bool:
        pass
    
    @abstractmethod
    def get_test_by_id(self, test_id: str):
        pass
    
    @abstractmethod
    def get_tests_for_prescription(self, prescription_id: str) -> List[Dict]:
        pass