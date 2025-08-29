from datetime import datetime, date
import re

def validate_medicine_name(name):
    """Validate medicine name"""
    if not name or not name.strip():
        return False, "Medicine name cannot be empty"
    if len(name.strip()) > 50:
        return False, "Medicine name too long (max 50 characters)"
    # Allow letters, numbers, spaces, hyphens, and parentheses
    if not re.match(r'^[a-zA-Z0-9 \-()]+$', name.strip()):
        return False, "Medicine name contains invalid characters"
    return True, "Valid name"

def validate_medicine_type(med_type):
    """Validate medicine type"""
    valid_types = ['tablet', 'syrup', 'capsule', 'injection', 'cream', 'drops', 'inhaler', 'spray']
    if not med_type or not med_type.strip():
        return False, "Medicine type cannot be empty"
    if med_type.lower().strip() not in valid_types:
        return False, f"Invalid medicine type. Valid types: {', '.join(valid_types)}"
    return True, "Valid type"

def validate_price(price):
    """Check if price is valid (non-negative number)."""
    try:
        price_val = float(price) if not isinstance(price, (int, float)) else price
        if price_val < 0:
            return False, "Price cannot be negative"
        if price_val > 10000:
            return False, "Price seems unreasonably high"
        return True, "Valid price"
    except (ValueError, TypeError):
        return False, "Invalid price format"

def validate_stock(stock):
    """Check if stock is a valid integer >= 0."""
    try:
        stock_val = int(stock) if not isinstance(stock, int) else stock
        if stock_val < 0:
            return False, "Stock cannot be negative"
        if stock_val > 100000:
            return False, "Stock quantity seems unreasonably high"
        return True, "Valid stock"
    except (ValueError, TypeError):
        return False, "Invalid stock format"

def validate_date(date_text):
    """Validate expiry date in YYYY-MM-DD format."""
    try:
        if isinstance(date_text, str):
            expiry_date = datetime.strptime(date_text, "%Y-%m-%d").date()
            today = date.today()
            if expiry_date <= today:
                return False, "Expiry date must be in the future"
            return True, "Valid date"
        elif isinstance(date_text, date):
            if date_text <= date.today():
                return False, "Expiry date must be in the future"
            return True, "Valid date"
        else:
            return False, "Invalid date type"
    except (ValueError, TypeError):
        return False, "Invalid date format. Use YYYY-MM-DD"

def validate_availability(available):
    """Validate availability status"""
    if available.lower() not in ['y', 'n', 'yes', 'no']:
        return False, "Invalid availability. Enter 'y' or 'n'"
    return True, "Valid availability"
