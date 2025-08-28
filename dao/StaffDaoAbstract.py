from abc import ABC,abstractmethod
from models.staff import Staff
from typing import List

class StaffDaoServices(ABC):
    @abstractmethod
    def display_all_staffs(self)->List[Staff]:
        '''display all staffs'''
        pass

    @abstractmethod
    def search_staff(self,staff_id)->bool:
        '''search a staff by id'''
        pass

    @abstractmethod
    def add_staff(self)->bool:
        '''add new staff'''
        pass

    @abstractmethod
    def update_staff_email(self,staff:Staff,staff_id)->bool:
        '''upadate email of the employee'''
        pass

    @abstractmethod
    def update_staff_name(self,staff:Staff,staff_id)->bool:
        '''update name of the staff'''
        pass

    @abstractmethod
    def update_staff_role(self,staff:Staff,staff_id)->bool:
        '''update role of the staff'''
        pass

    @abstractmethod
    def update_staff_phno(self,staff:Staff,staff_id)->bool:
        '''update phno of the staff'''
        pass

    @abstractmethod
    def update_staff_addrs(self,staff:Staff,staff_id)->bool:        
        '''update address of the staff'''
        pass

    @abstractmethod
    def update_staff_username(self,staff:Staff,staff_id)->bool:
        '''update username of the staff'''
        pass

    @abstractmethod
    def update_staff_psswrd(self,staff:Staff,staff_id)->bool:
        '''update password of the staff'''
        pass

    @abstractmethod
    def suspend_staff(self,staff_id)->bool:
        '''update active status of the staff'''
        pass

    @abstractmethod
    def enable_staff(self,staff_id)->bool:
        '''enable active status of the staff'''
        pass