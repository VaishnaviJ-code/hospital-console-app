from database.connection import DBConnection
from services.StaffLib import StaffLib

def main():
    while True:
        c=int(input("------------------WWELCOME BACK ADMINISTRATOR----------------------------"
        "\n 1.ADD STAFF"
        "\n 2.DISPLAY ALL STAFFS"
        "\n 3.UPDATE STAFF"
        "\n 4.SUSPEND STAFF"
        "\n 5.ENABLE STAFF"
        "\n 6.EXIT"
        "\n Enter your choice: "))
        match c:
            case 1:
                StaffLib.add_staff()
            case 2:
                StaffLib.display_all()
            case 3:
                while True:
                    cup=int(input("------------------UPDATE----------------------------"
                    "\n 1.UPDATE NAME"
                    "\n 2.UPDATE EMAIL"
                    "\n 3.UPDATE ROLE"
                    "\n 4.UPDATE PHONE NUMBER"
                    "\n 5.UPDATE ADDRESS"
                    "\n 6.UPDATE USERNAME"
                    "\n 7.UPDATE PASSWORD"
                    "\n 8.EXIT"
                    "\n Enter your choice: "))
                    match cup:
                        case 1:
                            StaffLib.update_staff_name()
                        case 2:
                            StaffLib.update_staff_email()
                        case 3:
                            StaffLib.update_staff_role()
                        case 4:
                            StaffLib.update_staff_phno()
                        case 5:
                            StaffLib.update_staff_addrs()
                        case 6:
                            StaffLib.update_staff_username()
                        case 7:
                            StaffLib.update_staff_passwrd()
                        case 8:
                            break
                        case _:
                            print("invalid option")
            case 4:
                StaffLib.suspend_staff()
            case 5:
                StaffLib.enable_staff()
            case 7:
                break
            case _:
                print("invalid option")
                


if __name__ == "__main__":
    main()