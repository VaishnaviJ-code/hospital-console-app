from dao.StaffDaoAbstract import StaffDaoServices
from dao.StaffDaoImple import StaffDaoImple
from datetime import datetime
from models.staff import Staff
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
        staff = Staff()
        
        # Generate staff ID
        # sid = f"EMP{Staff.id_ini + 1}"
        # Staff.id_ini += 1

        # sid = input("Enter Staff ID: ")  # Use the property setter
        # staff.set_staff_id = sid
        
        sname = input("Enter the name of the staff: ")
        staff.set_staff_name = sname
        
        dob = input("Enter the date of birth (dd/mm/yyyy): ")
        until_date = datetime.strptime(dob, "%d/%m/%Y")
        conv_m_date = until_date.date()
        staff.set_DOB = conv_m_date
        
        email = input("Enter the email: ")
        staff.set_email = email
        
        phn = input("Enter the phone number: ")
        staff.set_phone = phn
        
        addr = input("Enter the address: ")
        staff.set_address = addr
        
        exp = int(input("Enter the experience: "))
        staff.set_experience = exp
        
        doj = input("Enter the date of joining (dd/mm/yyyy): ")
        until_date = datetime.strptime(doj, "%d/%m/%Y")
        conv_m_date = until_date.date()
        staff.set_date_joining = conv_m_date
        
        rid = int(input("Enter the role ID: "))
        staff.set_role_id = rid
        
        staff.set_is_active = "y"
        
        sex = input("Enter the gender (M/F/Other): ")
        staff.set_gender = sex
        
        # Set username and password after other fields are set
        staff.set_username = email
        
        if StaffLib.dao_services.add_staff(staff):
            print("Inserted Successfully....")
            print(f"Username: {staff.get_username}")
            print(f"Password: {staff.get_passwrd}")

            if rid == 2:
                print("\n--- Creating Doctor Profile ---")
                try:
                    DocLib.create_doctor_profile(staff.get_staff_id)
                except Exception as e:
                    print(f"Error creating doctor profile: {e}")

