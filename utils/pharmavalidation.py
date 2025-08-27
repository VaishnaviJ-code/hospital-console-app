from datetime import datetime

def validate_price(price):
    """Check if price is valid (non-negative number)."""
    return isinstance(price, (int, float)) and price >= 0

def validate_stock(stock):
    """Check if stock is a valid integer >= 0."""
    return isinstance(stock, int) and stock >= 0

def validate_date(date_text):
    """Validate expiry date in YYYY-MM-DD format."""
    try:
        datetime.strptime(str(date_text), "%Y-%m-%d")
        return True
    except ValueError:
        return False