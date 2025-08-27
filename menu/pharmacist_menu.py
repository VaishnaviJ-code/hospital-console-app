from models.pharmacist import Medicine
from services.pharmacistservice import PharmacistService
from datetime import date, datetime

def pharmacist_menu():
    service = PharmacistService()

    while True:
        print("\n--- Pharmacy Management System ---")
        print("1. Add Medicine")
        print("2. View All Medicines")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # --- Take medicine details from user ---
            med_id = input("Enter medicine ID: ")
            name = input("Enter medicine name: ")
            med_type = input("Enter medicine type (Tablet/Syrup/etc): ")
            price = float(input("Enter price: "))
            stock = int(input("Enter stock quantity: "))
            expiry_str = input("Enter expiry date (YYYY-MM-DD): ")

          # Convert expiry date string → datetime.date
            try:
                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
            except ValueError:
                print(" Invalid date format. Use YYYY-MM-DD.")
                continue
            available_str = input("Is medicine available? (Y/N): ").strip().upper()
            available = True if available_str == "Y" else False
                # --- Create Medicine object ---
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

        elif choice == "2":
            medicines = service.dao.display_all_medicines()
            if not medicines:
                print("No medicines found.")
            else:
                print("\n--- All Medicines ---")
                for med in medicines:
                    print(f"ID: {med.get_med_id()}, Name: {med.get_name()}, Type: {med.get_med_type()}, Price: {med.get_price()}, Stock: {med.get_stock()}, Expiry: {med.get_expiry_date()}, Available: {med.get_available()}")

        elif choice == "3":
            print("Exiting...")
            break