import re
from datetime import datetime, date
from typing import Dict, Any
from models.staff import Staff


class StaffValidator:
    """Handles staff data validation"""
    
    VALID_GENDERS = ['M', 'F', 'Other', 'm', 'f', 'other']
    VALID_STATUSES = ['y', 'n', 'Y', 'N']
    
    @staticmethod
    def validate_staff_id(staff_id: str) -> Dict[str, Any]:
        """Validate staff ID format"""
        errors = []
        if not staff_id:
            errors.append("Staff ID is required")
        elif not isinstance(staff_id, str):
            errors.append("Staff ID must be a string")
        elif not staff_id.startswith("EMP"):
            errors.append("Staff ID must start with 'EMP'")
        elif len(staff_id) != 7:  # EMP1000 format
            errors.append("Staff ID must be in format EMP####")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_staff_name(name: str) -> Dict[str, Any]:
        """Validate staff name"""
        errors = []   
        if not name or not name.strip():
            errors.append("Staff name is required")
        elif not name.isalpha:
            errors.append("Staff ID must be a string")
        elif len(name.strip()) < 2:
            errors.append("Staff name must be at least 2 characters")
        elif len(name.strip()) > 50:
            errors.append("Staff name cannot exceed 50 characters")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """Validate email format"""
        errors = []
        
        if not email:
            errors.append("Email is required")
        else:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                errors.append("Invalid email format")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_phone(phone: str) -> Dict[str, Any]:
        """Validate phone number"""
        errors = []
        
        if not phone:
            errors.append("Phone number is required")
        else:
            # Remove any formatting and check if it's 10 digits
            clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
            if not re.match(r'^\d{10}$', clean_phone):
                errors.append("Phone number must be exactly 10 digits")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_date_of_birth(dob_str: str) -> Dict[str, Any]:
        """Validate date of birth"""
        errors = []
        
        if not dob_str:
            errors.append("Date of birth is required")
            return {"valid": False, "errors": errors}
        
        try:
            # Parse date from dd/mm/yyyy format
            dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
            
            # Check if date is not in the future
            if dob > date.today():
                errors.append("Date of birth cannot be in the future")
            
            # Check reasonable age range
            age = (date.today() - dob).days // 365
            if age > 100:
                errors.append("Invalid date of birth (age cannot exceed 100 years)")
            elif age < 18:
                errors.append("Staff member must be at least 18 years old")
                
        except ValueError:
            errors.append("Invalid date format. Use DD/MM/YYYY")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_gender(gender: str) -> Dict[str, Any]:
        """Validate gender"""
        errors = []
        
        if not gender:
            errors.append("Gender is required")
        elif gender not in StaffValidator.VALID_GENDERS:
            errors.append("Gender must be M, F, or Other")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_role_id(role_id: str) -> Dict[str, Any]:
        """Validate role ID"""
        errors = []
        valid_roles = ["2", "3", "4", "5"]  # Doctor, Pharmacist, Receptionist, Lab Tech
        if not role_id:
            errors.append("Role ID must be given")
        elif not role_id.isdigit():
            errors.append("Role ID must be an integer")
        elif role_id not in valid_roles:
            errors.append(f"Role ID must be one of {valid_roles}")
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_experience(age,exp:int)->Dict[str,Any]:
        errors = []
        if not exp:
            errors.append("Experience must be entred")
        elif int(exp)>(age-18):
            errors.append("Enter the correct experience")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_age(role:int,age:int)->Dict[str,Any]:
        errors = []
        if age<18:
            errors.append("Age must be at least 18 to get employeed")
        elif age<25 and role==2:
            errors.append("Doctor must be atleast 25 years old")
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_doj(doj_str: str,exp:int) -> Dict[str, Any]:
        """Validate date of joining"""
        errors = []
        if not doj_str:
            errors.append("Date of joining is required")
            return {"valid": False, "errors": errors}
        try:
            # Parse date from dd/mm/yyyy format
            doj = datetime.strptime(doj_str, "%d/%m/%Y").date()
            td=date.today()
            yrs=td.year-doj.year
            # Check if date is not in the future
            if doj > date.today():
                errors.append("Date of joining cannot be in the future")
            elif yrs>exp:
                errors.append("Give the correct date of joining")
        except ValueError:
            errors.append("Invalid date format. Use DD/MM/YYYY")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }