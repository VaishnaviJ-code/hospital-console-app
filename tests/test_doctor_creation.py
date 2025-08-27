"""
Complete test with staff creation first
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.StaffLib import StaffLib
from services.DoctorCreateLib import DocLib
from models.staff import Staff
from models.Doctor import Doctor
from datetime import datetime

def test_complete_staff_doctor_flow():
    print("=== Testing Complete Staff -> Doctor Flow ===")
    
    # Step 1: Create Staff Member First
    staff = Staff(
        staff_name="Test Doctor",
        DOB=datetime.strptime("01/01/1990", "%d/%m/%Y").date(),
        age=35,
        email="testdoc@hospital.com",
        phone="9876543210",
        address="Test Address",
        experience=5,
        joining_date=datetime.strptime("01/01/2020", "%d/%m/%Y").date(),
        role_id=2,  # Doctor role
        username="testdoc@hospital.com",
        pass_wrd="TEST2025",
        is_active="y",
        created_at=datetime.now().date(),
        gender="M"
    )
    
    # Add staff to database
    print("Adding staff member...")
    staff_added = StaffLib.dao_services.add_staff(staff)
    
    if staff_added:
        print("✅ Staff added successfully!")
        
        # Step 2: Now create doctor record
        print("Adding doctor profile...")
        
        doc = Doctor(
            doctor_id="DOC1001",
            staff_id="EMP1005",  # Now this exists!
            dept_id=1,
            sp_id=1,
            consultation_fee=150.0
        )
        
        doctor_added = DocLib.dao_services.add_doctor(doc)
        
        if doctor_added:
            print("✅ Doctor added successfully!")
            
            # Verify both records exist
            print("\nVerification:")
            print("All staff:")
            staff_list = StaffLib.dao_services.display_all_staffs()
            for s in staff_list:
                if s.get_staff_id == "EMP1005":
                    print(f"  ✅ Staff found: {s.get_staff_id}")
            
            print("All doctors:")
            doctor_list = DocLib.dao_services.display_all_doctors()
            for d in doctor_list:
                print(f"  ✅ Doctor found: {d}")
                    
        else:
            print("❌ Failed to add doctor")
    else:
        print("❌ Failed to add staff")

if __name__ == "__main__":
    test_complete_staff_doctor_flow()
