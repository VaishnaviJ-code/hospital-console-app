from dao.pharmacistimple import PharmacistImpl
from models.pharmacist import Medicine  # Import from models, not dao
from utils.pharmavalidation import validate_price, validate_stock, validate_date

class PharmacistService:
    def __init__(self):
        self.dao = PharmacistImpl()

    def add_medicine(self, medicine: Medicine):
        """Add a new medicine after validation."""
        if not validate_price(medicine.get_price()):
            return False, "Invalid Price"
        if not validate_stock(medicine.get_stock()):
            return False, "Invalid Stock"
        if not validate_date(medicine.get_expiry_date()):
            return False, "Invalid Expiry Date"

        try:
            self.dao.add_medicine(medicine)
            return True, "Medicine added successfully"
        except Exception as e:
            return False, f"Error adding medicine: {str(e)}"
    
    def get_all_medicines(self):
        """Get all medicines from database."""
        try:
            return self.dao.display_all_medicines()
        except Exception as e:
            print(f"Error retrieving medicines: {e}")
            return []
