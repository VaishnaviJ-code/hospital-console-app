from datetime import date

class Staff:
    id_ini = 1000
    
    def __init__(self, staff_id=None, staff_name=None, DOB=None, age=None, email=None, 
                 phone=None, address=None, experience=None, joining_date=None, 
                 role_id=None, username=None, pass_wrd=None, is_active=None, 
                 created_at=None, gender=None):
        
        self.__staff_id = staff_id
        self.__staff_name = staff_name
        self.__DOB = DOB
        self.__age = self.age_calc() if DOB else age
        self.__email = email
        self.__phone = phone
        self.__address = address
        self.__experience = experience
        self.__joining_date = joining_date if joining_date else date.today()
        self.__role_id = role_id
        self.__username = username if username else email
        self.__pass_wrd = pass_wrd if pass_wrd else self.passwrd_gen()
        self.__is_active = is_active
        self.__created_at = created_at if created_at else date.today()
        self.__gender = gender

    # Getters (using @property)
    @property
    def get_staff_id(self):
        return self.__staff_id

    @property
    def get_staff_name(self):
        return self.__staff_name

    @property
    def get_DOB(self):
        return self.__DOB

    @property
    def get_age(self):
        return self.__age

    @property
    def get_email(self):
        return self.__email

    @property
    def get_phone(self):
        return self.__phone

    @property
    def get_address(self):
        return self.__address

    @property
    def get_experience(self):
        return self.__experience

    @property
    def get_date_joining(self):
        return self.__joining_date

    @property
    def get_role_id(self):
        return self.__role_id

    @property
    def get_username(self):
        return self.__username

    @property
    def get_passwrd(self):
        return self.__pass_wrd

    @property
    def get_is_active(self):
        return self.__is_active

    @property
    def get_created_at(self):
        return self.__created_at

    @property
    def get_gender(self):
        return self.__gender

    # Setters
    @get_staff_id.setter
    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    @get_staff_name.setter
    def set_staff_name(self, name):
        self.__staff_name = name

    @get_DOB.setter
    def set_DOB(self, dob):
        self.__DOB = dob
        self.__age = self.age_calc()  # Recalculate age when DOB changes

    @get_email.setter
    def set_email(self, email):
        self.__email = email
        if not self.__username:  # Set username to email if not already set
            self.__username = email

    @get_phone.setter
    def set_phone(self, phone):
        self.__phone = phone

    @get_address.setter
    def set_address(self, address):
        self.__address = address

    @get_experience.setter
    def set_experience(self, experience):
        self.__experience = experience

    @get_date_joining.setter
    def set_date_joining(self, joining_date):
        self.__joining_date = joining_date

    @get_role_id.setter
    def set_role_id(self, role_id):
        self.__role_id = role_id

    @get_username.setter
    def set_username(self, username):
        self.__username = username

    @get_is_active.setter
    def set_is_active(self, is_active):
        self.__is_active = is_active

    @get_gender.setter
    def set_gender(self, gender):
        self.__gender = gender

    def age_calc(self):
        """Calculate age from date of birth"""
        if not self.__DOB:
            return None
        today = date.today()
        return today.year - self.__DOB.year - ((today.month, today.day) < (self.__DOB.month, self.__DOB.day))

    def passwrd_gen(self):
        """Generate password from name"""
        if not self.__staff_name:
            return "default2025"
        return self.__staff_name[:3].upper() + "2025"

    def __str__(self):
        return (f"Staff ID: {self.__staff_id} | Name: {self.__staff_name} | "
                f"Age: {self.__age} | Username: {self.__username} | "
                f"Password: {self.__pass_wrd} | Email: {self.__email} | "
                f"Role ID: {self.__role_id} | Active: {self.__is_active} | "
                f"Created: {self.__created_at}")
