"""
AdGenius AI Backend - Validation Utilities
"""
import re
from typing import Any, Dict, List, Optional, Union

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> Dict[str, Any]:
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        Dict[str, Any]: Validation result
    """
    # Check length
    if len(password) < 8:
        return {
            "valid": False,
            "message": "Password must be at least 8 characters long"
        }
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return {
            "valid": False,
            "message": "Password must contain at least one uppercase letter"
        }
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return {
            "valid": False,
            "message": "Password must contain at least one lowercase letter"
        }
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return {
            "valid": False,
            "message": "Password must contain at least one digit"
        }
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return {
            "valid": False,
            "message": "Password must contain at least one special character"
        }
    
    return {
        "valid": True,
        "message": "Password is valid"
    }

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
    """
    Validate required fields in data
    
    Args:
        data (Dict[str, Any]): Data to validate
        required_fields (List[str]): List of required field names
        
    Returns:
        Dict[str, Any]: Validation result
    """
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        return {
            "valid": False,
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }
    
    return {
        "valid": True,
        "message": "All required fields are present"
    }

def validate_field_type(value: Any, expected_type: type) -> bool:
    """
    Validate field type
    
    Args:
        value (Any): Value to validate
        expected_type (type): Expected type
        
    Returns:
        bool: True if value is of expected type, False otherwise
    """
    return isinstance(value, expected_type)

def validate_field_length(value: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
    """
    Validate field length
    
    Args:
        value (str): Value to validate
        min_length (int, optional): Minimum length. Defaults to 0.
        max_length (Optional[int], optional): Maximum length. Defaults to None.
        
    Returns:
        bool: True if value length is within range, False otherwise
    """
    if len(value) < min_length:
        return False
    
    if max_length is not None and len(value) > max_length:
        return False
    
    return True

def validate_numeric_range(value: Union[int, float], min_value: Optional[Union[int, float]] = None, max_value: Optional[Union[int, float]] = None) -> bool:
    """
    Validate numeric value range
    
    Args:
        value (Union[int, float]): Value to validate
        min_value (Optional[Union[int, float]], optional): Minimum value. Defaults to None.
        max_value (Optional[Union[int, float]], optional): Maximum value. Defaults to None.
        
    Returns:
        bool: True if value is within range, False otherwise
    """
    if min_value is not None and value < min_value:
        return False
    
    if max_value is not None and value > max_value:
        return False
    
    return True

def validate_url(url: str) -> bool:
    """
    Validate URL format
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    pattern = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
    return bool(re.match(pattern, url))

def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if phone number is valid, False otherwise
    """
    # Remove common separators and spaces
    cleaned_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    # Check if it's a valid phone number (simple check)
    pattern = r'^(\+\d{1,3})?(\d{8,15})$'
    return bool(re.match(pattern, cleaned_phone))
