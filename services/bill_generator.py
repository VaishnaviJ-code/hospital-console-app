from datetime import datetime
from typing import Dict, Any, Optional

class BillGenerator:
    """Generate consultation bills with conditional charges"""
    
    def __init__(self):
        self.op_charge = 100.00  # Default OP charge
        self.registration_charge = 100.00  # Registration fee for new patients
    
    def generate_consultation_bill(self, patient_id: str, doctor_id: str, 
                                  consultation_fee: float, appointment_id: str = None,
                                  is_newly_registered: bool = False,
                                  patient_name: str = None, doctor_name: str = None,
                                  save_to_db: bool = True) -> Dict[str, Any]:
        """
        Generate consultation bill with conditional registration fee
        """
        
        bill_items = []
        total_amount = 0.0
        
        # Add OP Charge (always included)
        op_item = {
            "description": "OP Charge",
            "amount": self.op_charge
        }
        bill_items.append(op_item)
        total_amount += self.op_charge
        
        # Add Consultation Fee (always included)
        consultation_item = {
            "description": "Consultation Fee",
            "amount": consultation_fee
        }
        bill_items.append(consultation_item)
        total_amount += consultation_fee
        
        # Add Registration Charge (only if newly registered)
        if is_newly_registered:
            registration_item = {
                "description": "Registration Charge",
                "amount": self.registration_charge
            }
            bill_items.append(registration_item)
            total_amount += self.registration_charge
        
        # Generate bill
        bill = {
            "bill_id": self._generate_bill_id(),
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "patient_id": patient_id,
            "patient_name": patient_name or "N/A",
            "doctor_id": doctor_id,
            "doctor_name": doctor_name or "N/A",
            "appointment_id": appointment_id,
            "items": bill_items,
            "total_amount": total_amount,
            "is_newly_registered": is_newly_registered
        }
        
        #  Save to database if requested
        if save_to_db:
            self.save_bill_to_database(bill)
        
        return bill
    
    def save_bill_to_database(self, bill: Dict[str, Any]) -> bool:
        """Save bill to database using DAO"""
        try:
            from dao.receptionist_implementation import ReceptionistDaoImplementation
            dao = ReceptionistDaoImplementation()
            return dao.save_consultation_bill(bill)
        except Exception as e:
            print(f"Error saving bill to database: {e}")
            return False
    
    def display_bill(self, bill: Dict[str, Any]) -> str:
        """Format bill for display"""
        
        bill_text = []
        bill_text.append("=" * 60)
        bill_text.append("HOSPITAL CONSULTATION BILL".center(60))
        bill_text.append("=" * 60)
        bill_text.append(f"Bill ID       : {bill['bill_id']}")
        bill_text.append(f"Date & Time   : {bill['date']}")
        bill_text.append(f"Patient ID    : {bill['patient_id']}")
        bill_text.append(f"Patient Name  : {bill['patient_name']}")
        bill_text.append(f"Doctor ID     : {bill['doctor_id']}")
        bill_text.append(f"Doctor Name   : {bill['doctor_name']}")
        bill_text.append("-" * 60)
        bill_text.append("CHARGES:")
        bill_text.append("-" * 60)
        
        for item in bill['items']:
            bill_text.append(f"{item['description']:<25} : ₹{item['amount']:.2f}")
        
        bill_text.append("-" * 60)
        bill_text.append(f"{'TOTAL AMOUNT':<25} : ₹{bill['total_amount']:.2f}")
        bill_text.append("=" * 60)
        
        if bill['is_newly_registered']:
            bill_text.append("* Registration charge applied for new patient")
        
        bill_text.append("Thank you for choosing our hospital!")
        bill_text.append("=" * 60)
        
        return "\n".join(bill_text)
    
    def _generate_bill_id(self) -> str:
        """Generate unique bill ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"BILL{timestamp}"

# Global instance
bill_generator = BillGenerator()
