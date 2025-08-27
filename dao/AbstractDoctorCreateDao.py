from abc import ABC, abstractmethod
from typing import List
from models.Doctor import Doctor

class DoctorCreateDaoServices(ABC):
    @abstractmethod
    def display_all_doctors(self)->List[Doctor]:
        '''display all doctors'''
        pass

    # @abstractmethod
    # def search_staff(self,staff_id)->bool:
    #     '''search a staff by id'''
    #     pass

    @abstractmethod
    def add_doctor(self)->bool:
        '''add new doctor'''
        pass

    # @abstractmethod
    # def update_staff_email(self,email):
    #     '''upadate email of the employee'''
    #     pass

    # @abstractmethod
    # def update_staff_name(self,name):
    #     '''update name of the staff'''
    #     passclass StaffDaoServices(ABC):
