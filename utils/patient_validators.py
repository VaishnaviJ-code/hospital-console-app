import re
from datetime import datetime, date
from typing import Dict, Any

class PatientValidator:
    """Validator class for patient data validation."""

    VALID_GENDERS = ['other', 'm', 'f', 'male', 'female', 'o', 'M', 'F', 'Other']
    PHONE_PATTERN = r'^\d{10}$'  # Simplified to 10 digits
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    VALID_NAME = r'^[a-zA-Z .\-]+$'

    @staticmethod
    def validate_patient_data(patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete patient data dictionary."""
        errors = []

        # Check required fields
        required_fields = ['patient_name', 'dob', 'gender', 'phone', 'address', 'email']
        for field in required_fields:
            if field not in patient_data or not patient_data[field]:
                errors.append(f"{field.replace('_', ' ').title()} is required")

        if errors:
            return {"valid": False, "errors": errors}

        # Validate individual fields
        validations = [
            PatientValidator.validate_name(patient_data['patient_name']),
            PatientValidator.validate_date_of_birth(patient_data['dob']),
            PatientValidator.validate_gender(patient_data['gender']),
            PatientValidator.validate_phone(str(patient_data['phone'])),
            PatientValidator.validate_address(patient_data['address']),
            PatientValidator.validate_email(patient_data['email'])
        ]

        for validation in validations:
            if not validation['valid']:
                errors.extend(validation['errors'])

        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def validate_name(name: str) -> Dict[str, Any]:
        """Validate patient name."""
        errors = []
        if not name or not name.strip():
            errors.append("Name cannot be empty")
        elif len(name.strip()) < 2:
            errors.append("Name must be at least 2 characters long")
        elif len(name.strip()) > 100:
            errors.append("Name cannot exceed 100 characters")
        elif not re.match(PatientValidator.VALID_NAME, name):
            errors.append("Name cannot contain integers or symbols")
        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def validate_date_of_birth(dob: str) -> Dict[str, Any]:
        """Validate date of birth."""
        errors = []
        if not dob:
            errors.append("Date of birth is required")
            return {"valid": False, "errors": errors}

        try:
            birth_date = None
        
            for date_format in ['%d/%m/%Y', '%Y-%m-%d']:
                try:
                    if isinstance(dob, str):
                        birth_date = datetime.strptime(dob, date_format).date()
                        break
                except ValueError:
                    continue
            
            # If no format matched
            if birth_date is None:
                errors.append("Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD")
                return {"valid": False, "errors": errors}

            # Existing validation logic
            if birth_date > date.today():
                errors.append("Date of birth cannot be in the future")

            age = (date.today() - birth_date).days // 365
            if age > 150:
                errors.append("Invalid date of birth (age cannot exceed 150 years)")

        except Exception as e:
            errors.append(f"Invalid date: {str(e)}")

        return {"valid": len(errors) == 0, "errors": errors}
    @staticmethod
    def validate_gender(gender: str) -> Dict[str, Any]:
        """Validate gender."""
        errors = []
        if not gender:
            errors.append("Gender is required")
        elif gender not in PatientValidator.VALID_GENDERS:
            errors.append("Invalid gender value")
        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def validate_phone(phone: str) -> Dict[str, Any]:
        """Validate phone number."""
        errors = []
        if not phone:
            errors.append("Phone number is required")
        else:
            cleaned_phone = re.sub(r'[\s\-\(\)]', '', str(phone))
            if not re.match(PatientValidator.PHONE_PATTERN, cleaned_phone):
                errors.append("Phone number must be exactly 10 digits")
        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def validate_address(address: str) -> Dict[str, Any]:
        """Validate address."""
        errors = []
        if not address or not address.strip():
            errors.append("Address is required")
        elif len(address.strip()) < 5:
            errors.append("Address must be at least 5 characters long")
        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """Validate email address."""
        errors = []
        if not email:
            errors.append("Email is required")
        elif not re.match(PatientValidator.EMAIL_PATTERN, email):
            errors.append("Invalid email format")
        return {"valid": len(errors) == 0, "errors": errors}
