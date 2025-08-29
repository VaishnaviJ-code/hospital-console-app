from models.pharmacist import Medicine
from services.pharmacistservice import PharmacistService
from datetime import date, datetime

def pharmacist_menu():
    service = PharmacistService()

    while True:
        print("\n--- Pharmacy Management System ---")
        print("1. Add Medicine")
        print("2. View All Medicines")
        print("3. Update Medicine Info")
        print("4. Delete Medicine")
        print("5. Dispense Medicines & Generate Bill")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_medicine(service)
        elif choice == "2":
            view_all_medicines_detailed(service)
        elif choice == "3":
            update_medicine_info(service)
        elif choice == "4":
            delete_medicine(service)
        elif choice == "5":
            dispense_and_bill(service)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def add_medicine(service):
    """Add new medicine with comprehensive validation"""
    from utils.pharmavalidation import (
        validate_medicine_name, validate_medicine_type, 
        validate_price, validate_stock, validate_date, validate_availability
    )
    
    print("\n--- Add New Medicine ---")
    
    # Generate medicine ID
    med_id = service.generate_medicine_id()
    print(f"Generated Medicine ID: {med_id}")
    
    # Medicine name validation
    while True:
        name = input("Enter medicine name: ").strip()
        is_valid, message = validate_medicine_name(name)
        if is_valid:
            break
        else:
            print(f"Error: {message}")
    
    # Medicine type validation
    print("Valid types: Tablet, Syrup, Capsule, Injection, Cream, Drops, Inhaler, Spray")
    while True:
        med_type = input("Enter medicine type: ").strip()
        is_valid, message = validate_medicine_type(med_type)
        if is_valid:
            med_type = med_type.capitalize()  # Standardize format
            break
        else:
            print(f"Error: {message}")
    
    # Price validation
    while True:
        price_str = input("Enter price: $").strip()
        is_valid, message = validate_price(price_str)
        if is_valid:
            price = float(price_str)
            break
        else:
            print(f"Error: {message}")
    
    # Stock validation
    while True:
        stock_str = input("Enter stock quantity: ").strip()
        is_valid, message = validate_stock(stock_str)
        if is_valid:
            stock = int(stock_str)
            break
        else:
            print(f"Error: {message}")
    
    # Expiry date validation
    while True:
        expiry_str = input("Enter expiry date (YYYY-MM-DD): ").strip()
        is_valid, message = validate_date(expiry_str)
        if is_valid:
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
            break
        else:
            print(f"Error: {message}")
    
    # Availability validation
    while True:
        available_str = input("Is medicine available? (y/n): ").strip()
        is_valid, message = validate_availability(available_str)
        if is_valid:
            available = "y" if available_str.lower() in ['y', 'yes'] else "n"
            break
        else:
            print(f"Error: {message}")
    
    # Show summary for confirmation
    print("\n--- Medicine Details Summary ---")
    print(f"ID: {med_id}")
    print(f"Name: {name}")
    print(f"Type: {med_type}")
    print(f"Price: ${price:.2f}")
    print(f"Stock: {stock}")
    print(f"Expiry Date: {expiry_date}")
    print(f"Available: {'Yes' if available == 'y' else 'No'}")
    
    # Final confirmation
    confirm = input("\nConfirm adding this medicine? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Medicine addition cancelled.")
        return
    
    # Create medicine object and add to database
    med = Medicine(
        med_id=med_id,
        name=name,
        med_type=med_type,
        price=price,
        stock=stock,
        expiry_date=expiry_date,
        available=available
    )
    
    status, msg = service.add_medicine(med)
    if status:
        print(f"Success: {msg}")
    else:
        print(f"Failed: {msg}")


def view_all_medicines_detailed(service):
    """View all medicines with detailed formatting"""
    medicines = service.get_all_medicines()
    
    if not medicines:
        print("\nNo medicines available in inventory.")
        return
    
    # Enhanced display similar to your patient list
    width = 140
    print("=" * width)
    print("PHARMACY INVENTORY - ALL MEDICINES".center(width))
    print("=" * width)
    
    # Column headers
    headers = f"{'Medicine ID':<12} {'Medicine Name':<30} {'Type':<15} {'Price':<10} {'Stock':<8} {'Expiry':<12} {'Status':<10}"
    print(headers)
    print("-" * width)
    
    # Display medicines
    total_medicines = len(medicines)
    total_value = 0
    
    for med in medicines:
        # Calculate total inventory value
        med_value = med.get_price() * med.get_stock()
        total_value += med_value
        
        # Format availability status
        status = "Available" if med.get_available() == "y" else "Unavailable"
        
        # Display medicine row
        row = (f"{med.get_med_id():<12} "
               f"{med.get_name():<30} "
               f"{med.get_med_type().title():<15} "
               f"${med.get_price():<9.2f} "
               f"{med.get_stock():<8} "
               f"{str(med.get_expiry_date()):<12} "
               f"{status:<10}")
        print(row)
    
    print("=" * width)
    print(f"Total Medicines: {total_medicines} | Total Inventory Value: ${total_value:.2f}")
    print("=" * width)

def update_medicine_info(service):
    """Update medicine information with validation"""
    from utils.pharmavalidation import (
        validate_medicine_name, validate_medicine_type, 
        validate_price, validate_stock, validate_date, validate_availability
    )
    
    print("\n--- Update Medicine Info ---")
    
    # Display all medicines first
    view_all_medicines_detailed(service)
    
    med_id = input("\nEnter Medicine ID to update: ").strip()
    if not med_id:
        print("Medicine ID cannot be empty")
        return
    
    # Get existing medicine info
    existing_medicine = service.get_medicine_by_id(med_id)
    if not existing_medicine:
        print(f"No medicine found with ID '{med_id}'")
        return
    
    print(f"\nCurrent medicine info:")
    print(f"Name: {existing_medicine.get_name()}")
    print(f"Type: {existing_medicine.get_med_type()}")
    print(f"Price: ${existing_medicine.get_price()}")
    print(f"Stock: {existing_medicine.get_stock()}")
    print(f"Expiry Date: {existing_medicine.get_expiry_date()}")
    print(f"Available: {'Yes' if existing_medicine.get_available() == 'y' else 'No'}")
    
    print("\nEnter new values (press Enter to keep current):")
    
    # Medicine name validation
    while True:
        new_name = input(f"Medicine name [{existing_medicine.get_name()}]: ").strip()
        if not new_name:
            new_name = existing_medicine.get_name()
            break
        is_valid, message = validate_medicine_name(new_name)
        if is_valid:
            break
        else:
            print(f"Error: {message}")
    
    # Medicine type validation
    while True:
        new_type = input(f"Type [{existing_medicine.get_med_type()}]: ").strip()
        if not new_type:
            new_type = existing_medicine.get_med_type()
            break
        is_valid, message = validate_medicine_type(new_type)
        if is_valid:
            new_type = new_type.capitalize()
            break
        else:
            print(f"Error: {message}")
    
    # Price validation
    while True:
        new_price_str = input(f"Price [{existing_medicine.get_price()}]: ").strip()
        if not new_price_str:
            new_price = float(existing_medicine.get_price())
            break
        is_valid, message = validate_price(new_price_str)
        if is_valid:
            new_price = float(new_price_str)
            break
        else:
            print(f"Error: {message}")
    
    # Stock validation
    while True:
        new_stock_str = input(f"Stock [{existing_medicine.get_stock()}]: ").strip()
        if not new_stock_str:
            new_stock = int(existing_medicine.get_stock())
            break
        is_valid, message = validate_stock(new_stock_str)
        if is_valid:
            new_stock = int(new_stock_str)
            break
        else:
            print(f"Error: {message}")
    
    # Expiry date validation
    while True:
        new_expiry = input(f"Expiry date (YYYY-MM-DD) [{existing_medicine.get_expiry_date()}]: ").strip()
        if not new_expiry:
            new_expiry = str(existing_medicine.get_expiry_date())
            break
        is_valid, message = validate_date(new_expiry)
        if is_valid:
            break
        else:
            print(f"Error: {message}")
    
    # Availability validation
    while True:
        current_available = 'y' if existing_medicine.get_available() == 'y' else 'n'
        new_available_str = input(f"Available (y/n) [{current_available}]: ").strip()
        if not new_available_str:
            new_available = existing_medicine.get_available()
            break
        is_valid, message = validate_availability(new_available_str)
        if is_valid:
            new_available = "y" if new_available_str.lower() in ['y', 'yes'] else "n"
            break
        else:
            print(f"Error: {message}")
    
    # Update the medicine
    success, message = service.update_medicine(med_id, new_name, new_type, new_price, new_stock, new_expiry, new_available)
    
    if success:
        print(f" Success: {message}")
        print("\nUpdated medicine details:")
        updated_med = service.get_medicine_by_id(med_id)
        if updated_med:
            print(f"Name: {updated_med.get_name()}")
            print(f"Type: {updated_med.get_med_type()}")
            print(f"Price: ${updated_med.get_price()}")
            print(f"Stock: {updated_med.get_stock()}")
            print(f"Expiry Date: {updated_med.get_expiry_date()}")
            print(f"Available: {'Yes' if updated_med.get_available() == 'y' else 'No'}")
    else:
        print(f" Failed: {message}")



def delete_medicine(service):
    """Delete medicine"""
    print("\n--- Delete Medicine ---")
    
    # Display all medicines first
    view_all_medicines_detailed(service)
    
    med_id = input("\nEnter Medicine ID to delete: ").strip()
    if not med_id:
        print("Medicine ID cannot be empty")
        return
    
    # Delete the medicine
    success, message = service.delete_medicine(med_id)
    print(message)

def dispense_and_bill(service):
    """Dispense medicines and generate bill"""
    print("\n--- Dispense Medicines & Generate Bill ---")
    
    prescription_id = input("Enter Prescription ID: ").strip()
    if not prescription_id:
        print("Prescription ID cannot be empty")
        return
    
    # Dispense medicines
    result = service.dispense_medicines(prescription_id)
    
    if result["success"]:
        print(f"\n" + "=" * 80)
        print(f"PHARMACY BILL - SALE ID: {result['sale_id']}".center(80))
        print(f"PRESCRIPTION: {result['prescription_id']}".center(80))
        print("=" * 80)
        print(f"{'Medicine':<25} {'Price':<12} {'Qty':<6} {'Dosage':<15} {'Duration':<12} {'Total'}")
        print("-" * 80)
        
        for item in result["items"]:
            print(f"{item['name']:<25} ${item['price']:<11.2f} {item['quantity']:<6} {item['dosage']:<15} {item['duration']:<12} ${item['total']:.2f}")
        
        print("-" * 80)
        print(f"{'TOTAL AMOUNT:':<70} ${result['total_amount']:.2f}")
        print("=" * 80)
        print("Thank you! Please take medicines as prescribed by the doctor.")
        print("=" * 80)
        
        # Save bill to file (optional)
        save_bill = input("\nSave bill to file? (y/N): ").strip().lower()
        if save_bill == 'y':
            filename = f"pharmacy_bill_{result['sale_id']}.txt"
            try:
                with open(filename, 'w') as f:
                    f.write(f"PHARMACY BILL - SALE ID: {result['sale_id']}\n")
                    f.write(f"PRESCRIPTION: {result['prescription_id']}\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"{'Medicine':<25} {'Price':<12} {'Qty':<6} {'Dosage':<15} {'Duration':<12} {'Total'}\n")
                    f.write("-" * 80 + "\n")
                    for item in result["items"]:
                        f.write(f"{item['name']:<25} ${item['price']:<11.2f} {item['quantity']:<6} {item['dosage']:<15} {item['duration']:<12} ${item['total']:.2f}\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"{'TOTAL AMOUNT:':<70} ${result['total_amount']:.2f}\n")
                    f.write("=" * 80 + "\n")
                print(f"Bill saved as '{filename}'")
            except Exception as e:
                print(f"Error saving bill: {e}")
    else:
        print(f"Error: {result['message']}")

if __name__ == "__main__":
    pharmacist_menu()
