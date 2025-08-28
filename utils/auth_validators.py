"""
Authentication and user validation utilities
"""

import re
from typing import Dict, Any, Optional
from dao.StaffDaoImple import StaffDaoImple


class AuthValidator:
    """Handles authentication and user validation"""
    
    # Role mapping for validation
    ROLE_MAPPING = {
        1: "Administrator",
        2: "Doctor", 
        3: "Lab Technician",
        4: "Pharmacist",
        5: "Receptionist"
    }

    DB_ROLE_MAPPING = {
        "Administrator": "admin",
        "Doctor": "doctor", 
        "Pharmacist": "pharma",
        "Receptionist": "reception", 
        "Lab Technician": "lab"
    }
    
    @staticmethod
    def validate_credentials_format(username: str, password: str) -> Dict[str, Any]:
        """
        Validate username and password format
        
        :param username: Username to validate
        :param password: Password to validate
        :return: Validation result dict
        """
        errors = []
        
        if not username or len(username.strip()) < 3:
            errors.append("Username must be at least 3 characters")
        
        if not password or len(password) < 4:
            errors.append("Password must be at least 4 characters")
            
        # Check for valid username format (alphanumeric + some special chars)
        if username and not re.match(r'^[a-zA-Z0-9._@-]+$', username):
            errors.append("Username contains invalid characters")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def authenticate_user(username: str, password: str, expected_role: str) -> Dict[str, Any]:
        """
        Authenticate user against database and verify role
        
        :param username: Username to authenticate
        :param password: Password to verify
        :param expected_role: Expected role name (e.g., "Administrator")
        :return: Authentication result dict
        """
        # Format validation first
        format_validation = AuthValidator.validate_credentials_format(username, password)
        if not format_validation["valid"]:
            return {
                "success": False,
                "message": "Invalid credentials format",
                "user": None,
                "errors": format_validation["errors"]
            }
        
        try:
            # Get staff member from database
            staff_dao = StaffDaoImple()
            staff_list = staff_dao.display_all_staffs()
            
            # Find user by username
            user_found = None
            for staff in staff_list:
                if staff.get_username == username:
                    user_found = staff
                    break
            
            if not user_found:
                return {
                    "success": False,
                    "message": "Invalid credentials",
                    "user": None,
                    "errors": ["User not found"]
                }
            
            # Verify password (in production, use hashed passwords)
            if user_found.get_passwrd != password:
                return {
                    "success": False,
                    "message": "Invalid credentials",
                    "user": None,
                    "errors": ["Incorrect password"]
                }
            
            # Check if user is active
            if user_found.get_is_active != 'y':
                return {
                    "success": False,
                    "message": "Account is disabled",
                    "user": None,
                    "errors": ["Account disabled"]
                }
            
            # Verify role matches
            user_role = AuthValidator.ROLE_MAPPING.get(user_found.get_role_id)
            if user_role != expected_role:
                return {
                    "success": False,
                    "message": f"Access denied. This account is not authorized for {expected_role} role",
                    "user": None,
                    "errors": ["Role mismatch"]
                }
            
            # Authentication successful
            return {
                "success": True,
                "message": "Authentication successful",
                "user": user_found,
                "errors": []
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Authentication error: {str(e)}",
                "user": None,
                "errors": [str(e)]
            }

    @staticmethod
    def get_user_role_name(role_id: int) -> Optional[str]:
        """Get role name from role ID"""
        return AuthValidator.ROLE_MAPPING.get(role_id)
    
    @staticmethod
    def validate_role_access(user_role_id: int, required_role: str) -> bool:
        """Check if user role matches required role"""
        user_role = AuthValidator.ROLE_MAPPING.get(user_role_id)
        return user_role == required_role