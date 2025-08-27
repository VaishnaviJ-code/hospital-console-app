from datetime import date

class Medicine:
    """Medicine model for pharmacy management"""
    
    def __init__(self, med_id=None, name=None, med_type=None, price=0.0, stock=0, expiry_date=None, available=True):
        self.__med_id = med_id
        self.__name = name
        self.__med_type = med_type
        self.__price = price
        self.__stock = stock
        self.__expiry_date = expiry_date
        self.__available = available

    # Getters
    def get_med_id(self): 
        return self.__med_id
        
    def get_name(self): 
        return self.__name
        
    def get_med_type(self): 
        return self.__med_type
        
    def get_price(self): 
        return self.__price
        
    def get_stock(self): 
        return self.__stock
        
    def get_expiry_date(self): 
        return self.__expiry_date
        
    def get_available(self): 
        return self.__available

    # Setters
    def set_med_id(self, med_id): 
        self.__med_id = med_id
        
    def set_name(self, name): 
        self.__name = name
        
    def set_med_type(self, med_type): 
        self.__med_type = med_type
        
    def set_price(self, price): 
        self.__price = price
        
    def set_stock(self, stock): 
        self.__stock = stock
        
    def set_expiry_date(self, expiry_date): 
        self.__expiry_date = expiry_date
        
    def set_available(self, available): 
        self.__available = available

    def __str__(self):
        return f"Medicine[{self.__med_id}] - {self.__name}, {self.__med_type}, Price: {self.__price}, Stock: {self.__stock}, Expiry: {self.__expiry_date}, Available: {self.__available}"

class PharmacySales:
    """Pharmacy sales model"""
    
    def __init__(self, sale_id=None, prescription_id=None, total_amount=0.0, sale_date=None):
        self.__sale_id = sale_id
        self.__prescription_id = prescription_id
        self.__total_amount = total_amount
        self.__sale_date = sale_date or date.today()

    # Getters
    def get_sale_id(self): 
        return self.__sale_id
        
    def get_prescription_id(self): 
        return self.__prescription_id
        
    def get_total_amount(self): 
        return self.__total_amount
        
    def get_sale_date(self): 
        return self.__sale_date

    # Setters
    def set_sale_id(self, sale_id): 
        self.__sale_id = sale_id
        
    def set_prescription_id(self, prescription_id): 
        self.__prescription_id = prescription_id
        
    def set_total_amount(self, total_amount): 
        self.__total_amount = total_amount
        
    def set_sale_date(self, sale_date): 
        self.__sale_date = sale_date
