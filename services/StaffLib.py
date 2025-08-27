from dao.StaffDaoAbstract import StaffDaoServices
from dao.StaffDaoImple import StaffDaoImple
from datetime import datetime
from models.staff import Staff

class StaffLib:

    dao_services:StaffDaoServices=StaffDaoImple()

    @staticmethod
    def display_all():
        staff=StaffLib.dao_services.display_all_staffs()
        for s in staff:
            print(s)

    @staticmethod
    def add_staff():
        staff=Staff()
        sname=input("Enter the name of the staff: ")
        staff.set_staff_name=sname
        dob=input("Enter the date of birth (dd/mm/yyy): ")
        until_date=datetime.strptime(dob,"%d/%m/%Y")
        conv_m_date=until_date.date()
        staff.set_DOB=conv_m_date
        email=input("Enter the email: ")
        staff.set_email=email
        phn=input("Enter the phn number: ")
        staff.set_phone=phn
        addr=input("Enter the address: ")
        staff.set_address=addr
        exp=int(input("Enter the experience: "))
        staff.set_experience=exp
        doj=input("Enter the date of joining (dd/mm/yyy): ")
        until_date=datetime.strptime(doj,"%d/%m/%Y")
        conv_m_date=until_date.date()
        staff.set_date_joining=conv_m_date
        rid=int(input("Enter the id of the roloe: "))
        staff.set_role_id=rid
        staff.set_is_active="y"
        sex=input("Enter the gender(M/F/Other): ")
        staff.set_gender=sex
        staff.set_username=email
        staff.set_age=staff.age_calc()
        staff.set_passwrd=staff.passwrd_gen()

        if StaffLib.dao_services.add_staff(staff):
            print("Inserted Successfully....")
            print(f"username : {staff.get_username} ")
            print(f"password : {staff.get_passwrd}")

    @staticmethod
    def update_staff_name():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            staff.set_staff_name=input("Enter the new name: ")
            if StaffLib.dao_services.update_staff_name(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")
    
    @staticmethod
    def update_staff_email():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            staff.set_email=input("Enter the new email id: ")
            if StaffLib.dao_services.update_staff_email(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")

    @staticmethod
    def update_staff_role():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            staff.set_role_id=int(input("Enter the new role id: "))
            if StaffLib.dao_services.update_staff_role(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")

    @staticmethod
    def update_staff_phno():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            staff.set_phone=input("Enter the new phone number: ")
            if StaffLib.dao_services.update_staff_phno(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")

    @staticmethod
    def update_staff_addrs():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            staff.set_address=input("Enter the new address: ")
            if StaffLib.dao_services.update_staff_addrs(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")

    @staticmethod
    def update_staff_username():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            staff.set_username=input("Enter the new user name: ")
            if StaffLib.dao_services.update_staff_username(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")

    @staticmethod
    def update_staff_passwrd():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            staff.set_passwrd=input("Enter the new password: ")
            if StaffLib.dao_services.update_staff_psswrd(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")
    
    @staticmethod
    def suspend_staff():
        id=input("Enter the id of the staff to be updated: ")
        staff=StaffLib.dao_services.search_staff(id)
        if not staff:
            print("Product not found !!!!!")
            return
        print(staff)
        confirm=input("Do you want edit this staff(Y/N): ")
        if confirm.lower()=='y':
            if StaffLib.dao_services.suspend_staff(id):
                print("Updateted Successfullyt!!!")
            else:
                print("Something went wrong...")
    