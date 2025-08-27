from abc import ABC,abstractmethod
from models.staff import Staff
from typing import List

class StaffDaoServices(ABC):
    @abstractmethod
    def display_all_staffs(self)->List[Staff]:
        '''display all staffs'''
        pass

    # @abstractmethod
    # def search_staff(self,staff_id)->bool:
    #     '''search a staff by id'''
    #     pass

    @abstractmethod
    def add_staff(self)->bool:
        '''add new staff'''
        pass

    # @abstractmethod
    # def update_staff_email(self,email):
    #     '''upadate email of the employee'''
    #     pass

    # @abstractmethod
    # def update_staff_name(self,name):
    #     '''update name of the staff'''
    #     pass