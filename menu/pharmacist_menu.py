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
            view_all_medicines(service)
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
    """Add new medicine"""
    med_id = service.generate_medicine_id()
    print(f"Generated Medicine ID: {med_id}")
    
    name = input("Enter medicine name: ")
    med_type = input("Enter medicine type (Tablet/Syrup/etc): ")
    
    try:
        price = float(input("Enter price: "))
    except ValueError:
        print("Invalid price format.")
        return
    
    try:
        stock = int(input("Enter stock quantity: "))
    except ValueError:
        print("Invalid stock format.")
        return
    
    expiry_str = input("Enter expiry date (YYYY-MM-DD): ")
    
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    available_str = input("Is medicine available? (Y/N): ").strip().upper()
    available = "y" if available_str == "Y" else "n"

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
    print("Add Medicine:", msg)

def view_all_medicines(service):
    """View all medicines"""
    medicines = service.get_all_medicines()
    if not medicines:
        print("No medicines found.")
    else:
        print("\n--- All Medicines ---")
        print(f"{'ID':<10} {'Name':<20} {'Type':<15} {'Price':<10} {'Stock':<8} {'Expiry':<12} {'Available'}")
        print("-" * 85)
        for med in medicines:
            available_text = "Yes" if med.get_available() == "y" else "No"
            print(f"{med.get_med_id():<10} {med.get_name():<20} {med.get_med_type():<15} ${med.get_price():<9.2f} {med.get_stock():<8} {med.get_expiry_date():<12} {available_text}")

def update_medicine_info(service):
    """Update medicine information"""
    print("\n--- Update Medicine Info ---")
    
    # Display all medicines first
    view_all_medicines(service)
    
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
    
    # Get new values (allow empty to keep current)
    print("\nEnter new values (press Enter to keep current):")
    
    new_name = input(f"Medicine name [{existing_medicine.get_name()}]: ").strip()
    if not new_name:
        new_name = existing_medicine.get_name()
    
    new_type = input(f"Type [{existing_medicine.get_med_type()}]: ").strip()
    if not new_type:
        new_type = existing_medicine.get_med_type()
    
    new_price_str = input(f"Price [{existing_medicine.get_price()}]: ").strip()
    if new_price_str:
        try:
            new_price = float(new_price_str)
            if new_price < 0:
                print("Price cannot be negative")
                return
        except ValueError:
            print("Invalid price format")
            return
    else:
        new_price = float(existing_medicine.get_price())  # Convert to float explicitly
    
    new_stock_str = input(f"Stock [{existing_medicine.get_stock()}]: ").strip()
    if new_stock_str:
        try:
            new_stock = int(new_stock_str)
            if new_stock < 0:
                print("Stock cannot be negative")
                return
        except ValueError:
            print("Invalid stock format")
            return
    else:
        new_stock = int(existing_medicine.get_stock())  # Convert to int explicitly
    
    new_expiry = input(f"Expiry date (YYYY-MM-DD) [{existing_medicine.get_expiry_date()}]: ").strip()
    if not new_expiry:
        new_expiry = str(existing_medicine.get_expiry_date())
    
    # Validate expiry date format
    try:
        datetime.strptime(new_expiry, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD")
        return
    
    new_available_str = input(f"Available (y/n) [{'y' if existing_medicine.get_available() == 'y' else 'n'}]: ").strip().lower()
    if new_available_str and new_available_str in ['y', 'n']:
        new_available = new_available_str
    elif not new_available_str:
        new_available = existing_medicine.get_available()
    else:
        print("Invalid availability. Use 'y' or 'n'")
        return
    
    # Update the medicine
    success, message = service.update_medicine(med_id, new_name, new_type, new_price, new_stock, new_expiry, new_available)
    print(message)
    
    if success:
        print("\nUpdated medicine details:")
        updated_med = service.get_medicine_by_id(med_id)
        if updated_med:
            print(f"Name: {updated_med.get_name()}")
            print(f"Type: {updated_med.get_med_type()}")
            print(f"Price: {updated_med.get_price()}")
            print(f"Stock: {updated_med.get_stock()}")
            print(f"Expiry Date: {updated_med.get_expiry_date()}")
            print(f"Available: {'Yes' if updated_med.get_available() == 'y' else 'No'}")


def delete_medicine(service):
    """Delete medicine"""
    print("\n--- Delete Medicine ---")
    
    # Display all medicines first
    view_all_medicines(service)
    
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
