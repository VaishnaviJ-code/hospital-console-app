from database.connection import DBConnection
from services.StaffLib import StaffLib

def admin_menu():
    while True:
        c=int(input("------------------WELCOME BACK ADMINISTRATOR----------------------------"
        "\n 1.ADD STAFF"
        "\n 2.DISPLAY ALL STAFFS"
        "\n 3.UPDATE STAFF"
        "\n 4.SEARCH STAFF"
        "\n 5.DISABLE STAFF"
        "\n 6.APPLY GST on products" 
        "\n 7.EXIT"
        "\n Enter your choice: "))
        match c:
            case 1:
                StaffLib.add_staff()
            case 2:
                StaffLib.display_all()
            # case 3:
            #     ProductManagentLib.update_product()
            # case 4:
            #     ProductManagentLib.search_product()
            # case 5:
            #     ProductManagentLib.disable_product()
            # case 6:
            #     ProductManagentLib.calc_gst()
            case 7:
                break
            case _:
                print("invalid option")
                