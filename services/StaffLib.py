from dao.StaffDaoAbstract import StaffDaoServices
from dao.StaffDaoImple import StaffDaoImple
from datetime import datetime
from models.staff import Staff
from utils.staff_validators import StaffValidator
from services.DoctorCreateLib import DocLib

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
        #validate and add name
        while True:
            sname=input("Enter the name of the staff: ")
            e=StaffValidator.validate_staff_name(sname)
            if e['valid']==True:
                staff.set_staff_name=sname
                break
            else:
                print(e['errors'])
        #validate and add role id
        while True:
            rid=int(input("Enter the id of the role" 
            "\n2.Doctor " 
            "\n3.Pharmacist " 
            "\n4.Receptionist" 
            "\n5.Lab Tech" \
            "\nEnter your choice: "))
            e=StaffValidator.validate_role_id(rid)
            if e["valid"]==True:
                staff.set_role_id=rid
                if rid==2:
                    DocLib.create_doctor_profile(staff.set_staff_id)
                break
            else:
                print(e["errors"])
        #validate and add dob
        while True:
            dob=input("Enter the date of birth (dd/mm/yyy): ")
            e=StaffValidator.validate_date_of_birth(dob)
            if e['valid']==True:
                until_date=datetime.strptime(dob,"%d/%m/%Y")
                conv_m_date=until_date.date()
                staff.set_DOB=conv_m_date
                #validate age
                age=staff.age_calc()
                role=staff.get_role_id
                e=StaffValidator.validate_age(role,age)
                t=False
                if e["valid"]==True:
                    staff.set_age=age
                    t=True
                    break
                else:
                    print(e["errors"])
            else:
                print(e['errors'])    
        #validate and add email
        while True:
            email=input("Enter the email: ")
            e=StaffValidator.validate_email(email)
            if e["valid"]==True:
                staff.set_email=email
                break
            else:
                print(e["errors"])
        #validate and add phone number
        while True:
            phn=input("Enter the phn number: ")
            e=StaffValidator.validate_phone(phn)
            if e["valid"]==True:
                staff.set_phone=phn
                break
            else:
                print(e["errors"])
        addr=input("Enter the address: ")
        staff.set_address=addr
        #validate and add experience
        while True:
            exp=input("Enter the experience: ")
            age=staff.get_age
            e=StaffValidator.validate_experience(age,exp)
            if e["valid"]==True:
                staff.set_experience=int(exp)
                break
            else:
                print(e["errors"])
        #validate and add doj
        while True:
            doj=input("Enter the date of joining (dd/mm/yyy): ")
            e=StaffValidator.validate_doj(doj)
            if e["valid"]==True:
                until_date=datetime.strptime(doj,"%d/%m/%Y")
                conv_m_date=until_date.date()
                staff.set_date_joining=conv_m_date
                break
            else:
                print(e['errors'])   
        staff.set_is_active="y"
        #validate and add gender
        while True:
            sex=input("Enter the gender(M/F/Other): ")
            e=StaffValidator.validate_gender(sex)
            if e["valid"]==True:
                staff.set_gender=sex
                break
            else:
                print(e["errors"])
        staff.set_username=email
        staff.set_passwrd=staff.passwrd_gen()

        if StaffLib.dao_services.add_staff(staff):
            print("Inserted Successfully....")
            print(f"username : {staff.get_username} ")
            print(f"password : {staff.get_passwrd}")

    @staticmethod
    def update_staff_name():
        while True:
            id=input("Enter the id of the staff to be updated: ")
            e=StaffValidator.validate_staff_id(id)
            if e["valid"]==True:
                staff=StaffLib.dao_services.search_staff(id)
                if not staff:
                    print("Staff not found !!!!!")
                    return
                print(staff)
                confirm=input("Do you want edit this staff(Y/N): ")
                if confirm.lower()=='y':
                    while True:
                        name=input("Enter the new name: ")
                        e=StaffValidator.validate_staff_name(name)
                        if e['valid']==True:
                            staff.set_staff_name=name
                            break
                        else:
                            print(e["errors"])
                break
            else:
                print(e["errors"])
                    
        if StaffLib.dao_services.update_staff_name(staff,id):
            print("Upadeted Successfullyt!!!")
        else:
            print("Something went wrong...")
    
    @staticmethod
    def update_staff_email():
        while True:
            id=input("Enter the id of the staff to be updated: ")
            e=StaffValidator.validate_staff_id(id)
            if e['valid']==True:
                staff=StaffLib.dao_services.search_staff(id)
                if not staff:
                    print("Product not found !!!!!")
                    return
                print(staff)
                confirm=input("Do you want edit this staff(Y/N): ")
                if confirm.lower()=='y':
                    while True:
                        email=input("Enter the new email id: ")
                        e=StaffValidator.validate_email(email)
                        if e['valid']==True:
                            staff.set_email=email
                            break
                        else:
                            print(e["errors"])
                break
            else:
                print(e["errors"])
        if StaffLib.dao_services.update_staff_email(staff,id):
            print("Upadeted Successfullyt!!!")
        else:
            print("Something went wrong...")

    @staticmethod
    def update_staff_role():
        while True:
            id=input("Enter the id of the staff to be updated: ")
            e=StaffValidator.validate_staff_id(id)
            if e["valid"]==True:
                staff=StaffLib.dao_services.search_staff(id)
                if not staff:
                    print("Product not found !!!!!")
                    return
                print(staff)
                confirm=input("Do you want edit this staff(Y/N): ")
                if confirm.lower()=='y':
                    while True:
                        rid=int(input("Enter the new role id: "))
                        e=StaffValidator.validate_role_id(rid)
                        if e["valid"]==True:
                            staff.set_role_id=rid
                            break
                        else:
                            print(e["errors"])
                break            
            else:
                print(e["errors"])
            if StaffLib.dao_services.update_staff_role(staff,id):
                print("Upadeted Successfullyt!!!")
            else:
                print("Something went wrong...")

    @staticmethod
    def update_staff_phno():
        while True:
            id=input("Enter the id of the staff to be updated: ")
            e=StaffValidator.validate_staff_id(id)
            if e["valid"]==True:
                staff=StaffLib.dao_services.search_staff(id)
                if not staff:
                    print("Product not found !!!!!")
                    return
                print(staff)
                confirm=input("Do you want edit this staff(Y/N): ")
                if confirm.lower()=='y':
                    while True:
                        phn=input("Enter the new phone number: ")
                        e=StaffValidator.validate_phone(phn)
                        if e["valid"]==True:
                            staff.set_phone=phn
                            break
                        else:
                            print(e["errors"])
                    break
                else:
                    print(e["errors"])
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
        while True:
            id=input("Enter the id of the staff to be suspended: ")
            e=StaffValidator.validate_staff_id(id)
            if e["valid"]==True:
                staff=StaffLib.dao_services.search_staff(id)
                if not staff:
                    print("Product not found !!!!!")
                    return
                print(staff)
                confirm=input("Do you want edit this staff(Y/N): ")
                if confirm.lower()=='y':
                    if StaffLib.dao_services.suspend_staff(id):
                        print("Staff Suspended Successfully!!!")
                    else:
                        print("Something went wrong...")
                break
            else:
                print(e["errors"])

    @staticmethod
    def enable_staff():
        while True:
            id=input("Enter the id of the staff to be suspended: ")
            e=StaffValidator.validate_staff_id(id)
            if e["valid"]==True:
                staff=StaffLib.dao_services.search_staff(id)
                if not staff:
                    print("Product not found !!!!!")
                    return
                print(staff)
                confirm=input("Do you want edit this staff(Y/N): ")
                if confirm.lower()=='y':
                    if StaffLib.dao_services.enable_staff(id):
                        print("Staff Enabled Successfully!!!")
                    else:
                        print("Something went wrong...")
                break
            else:
                print(e["errors"])

    