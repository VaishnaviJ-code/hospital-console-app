from dao.pharmacistimple import PharmacistImpl
from models.pharmacist import Medicine
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

    def update_medicine(self, med_id: str, name: str, med_type: str, price: float, stock: int, expiry_date: str, available: str):
        """Update medicine with validation"""
        if not validate_price(price):
            return False, "Invalid Price"

        if not validate_stock(stock):
            return False, "Invalid Stock"

        if not validate_date(expiry_date):
            return False, "Invalid Expiry Date"

        try:
            success = self.dao.update_medicine(med_id, name, med_type, price, stock, expiry_date, available)
            if success:
                return True, "Medicine updated successfully"
            else:
                return False, "Medicine not found or update failed"
        except Exception as e:
            return False, f"Error updating medicine: {str(e)}"

    def delete_medicine(self, med_id: str):
        """Delete medicine"""
        try:
            success = self.dao.delete_medicine(med_id)
            if success:
                return True, "Medicine deleted successfully"
            else:
                return False, "Medicine not found or deletion failed"
        except Exception as e:
            return False, f"Error deleting medicine: {str(e)}"

    def get_medicine_by_id(self, med_id: str):
        """Get medicine by ID"""
        try:
            return self.dao.get_medicine_by_id(med_id)
        except Exception as e:
            print(f"Error getting medicine: {e}")
            return None

    def dispense_medicines(self, prescription_id: str):
        """Dispense medicines and generate bill"""
        try:
            result = self.dao.dispense_medicine(prescription_id)
            return result
        except Exception as e:
            return {"success": False, "message": f"Error dispensing medicines: {str(e)}"}

    def generate_medicine_id(self):
        """Generate new medicine ID"""
        return self.dao.generate_medicine_id()
