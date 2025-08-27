from datetime import datetime

def validate_price(price):
    """Check if price is valid (non-negative number)."""
    try:
        price_val = float(price) if not isinstance(price, (int, float)) else price
        return price_val >= 0
    except (ValueError, TypeError):
        return False

def validate_stock(stock):
    """Check if stock is a valid integer >= 0."""
    try:
        stock_val = int(stock) if not isinstance(stock, int) else stock
        return stock_val >= 0
    except (ValueError, TypeError):
        return False

def validate_date(date_text):
    """Validate expiry date in YYYY-MM-DD format."""
    try:
        if isinstance(date_text, str):
            datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False