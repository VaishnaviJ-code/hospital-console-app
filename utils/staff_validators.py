"""
Staff validation utilities
"""

import re
from datetime import datetime, date
from typing import Dict, Any


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
    def validate_role_id(role_id: int) -> Dict[str, Any]:
        """Validate role ID"""
        errors = []
        
        valid_roles = [1, 2, 3, 4, 5]  # Admin, Doctor, Pharmacist, Receptionist, Lab Tech
        
        if not isinstance(role_id, int):
            errors.append("Role ID must be an integer")
        elif role_id not in valid_roles:
            errors.append(f"Role ID must be one of {valid_roles}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_staff_data(staff_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete staff data"""
        all_errors = []
        
        # Validate each field
        validations = [
            StaffValidator.validate_staff_name(staff_data.get('staff_name', '')),
            StaffValidator.validate_email(staff_data.get('email', '')),
            StaffValidator.validate_phone(staff_data.get('phone', '')),
            StaffValidator.validate_date_of_birth(staff_data.get('dob', '')),
            StaffValidator.validate_gender(staff_data.get('gender', '')),
            StaffValidator.validate_role_id(staff_data.get('role_id', 0))
        ]
        
        # Collect all errors
        for validation in validations:
            if not validation['valid']:
                all_errors.extend(validation['errors'])
        
        return {
            "valid": len(all_errors) == 0,
            "errors": all_errors
        }
