from dao.AbstractDoctorCreateDao import DoctorCreateDaoServices
from dao.DoctorCreateDaoImple import DoctorCreateDaoImple
from datetime import datetime
from models.Doctor import Doctor

class DocLib:

    dao_services:DoctorCreateDaoServices=DoctorCreateDaoImple()

    @staticmethod
    def display_all():
        doc=DocLib.dao_services.display_all_doctors()
        for d in doc:
            print(d)

    @staticmethod 
    def create_doctor_profile(staff_id):
        """Create doctor profile for existing staff member"""
        try:
            # Initialize variables to avoid UnboundLocalError
            did = None
            dept_id = None
            sp_id = None
            consult_fee = None
            
            # Get doctor details from user input
            did = input("Enter Doctor ID: ").strip()
            if not did:
                print("Doctor ID cannot be empty")
                return False
            
            staff_id = input("Enter the Staff id: ")

            print("Available Departments:")
            dept_id = int(input("Enter the department ID: "))
            
            print("Available Specializations:")
            sp_id = int(input("Enter the specialization ID: "))
            
            consult_fee = float(input("Enter the consultation fee: "))
            
            # Create Doctor object with ALL required parameters
            doc = Doctor(
                doctor_id=did,
                staff_id=staff_id,
                dept_id=dept_id,
                sp_id=sp_id,
                consultation_fee=consult_fee
            )
            
            # Add doctor to database
            if DocLib.dao_services.add_doctor(doc):
                print("Doctor profile created successfully!")
                return True
            else:
                print("Failed to create doctor profile")
                return False
                
        except ValueError as e:
            print(f"Invalid input: {e}")
            return False
        except Exception as e:
            print(f"Error creating doctor profile: {e}")
            return False
        
    @staticmethod
    def add_doctor():
        """Standalone method for adding doctor (existing functionality)"""
        doc = Doctor()
        
        did = input("Enter Doctor ID: ")
        doc.set_doc_id = did
        
        sid = input("Enter the Staff ID of the Doctor: ")
        doc.set_staff_id = sid
        
        dept_id = int(input("Enter the department ID: "))
        doc.set_dept_id = dept_id
        
        sp_id = int(input("Enter the specialization ID: "))
        doc.set_spcl_id = sp_id
        
        consult_fee = float(input("Enter the consultation fee: "))
        doc.set_consultation_fee = consult_fee
        
        if DocLib.dao_services.add_doctor(doc):
            print("Doctor added successfully!")
        else:
            print("Failed to add doctor")
    @staticmethod
    def add_staff():
        doc = Doctor()
        
        # Generate staff ID
        # sid = f"EMP{Staff.id_ini + 1}"
        # Staff.id_ini += 1

        did = input("Enter Doctor ID: ")  # Use the property setter
        doc.set_doc_id=did
        
        sid = input("Enter the Staff ID of the Doctor: ")
        doc.set_staff_id = sid 
        
        did=int(input("Enter the department ID: "))
        doc.set_dept_id=did

        spid = input("Enter the specialization id: ")
        doc.set_spcl_id=spid
        
        consult_fee = float(input("Enter the consultation fee: "))
        doc.set_consultation_fee = consult_fee


