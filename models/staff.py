from datetime import date

class Staff:
    id_ini=1000
    def __init__(self,staff_id=None,staff_name=None,DOB=None,age=None,email=None,phone=None,address=None,experience=None,
                 joining_date=None,role_id=None,username=None,pass_wrd=None,is_active=None,created_at=None,gender=None):
        self.__staff_id=staff_id
        self.__staff_name=staff_name
        self.__DOB=DOB
        self.__age=Staff.age_calc(self)
        self.__email=email
        self.__phone=phone
        self.__address=address
        self.__experience=experience
        self.__joining_date=joining_date if joining_date else date.today()
        self.__role_id=role_id
        self.__username=username
        self.__pass_wrd=Staff.passwrd_gen(self)
        self.__is_active=is_active
        self.__created_at=date.today()
        self.__gender=gender
    
    @property
    def get_staff_id(self):
        return self.__staff_id
    @get_staff_id.setter
    def set_staff_id(self,id):
        self.__staff_id=id

    @property
    def get_staff_name(self):
        return self.__staff_name
    @get_staff_name.setter
    def set_staff_name(self,name):
        self.__staff_name=name

    @property
    def get_DOB(self):
        return self.__DOB
    @get_DOB.setter
    def set_DOB(self,dob):
        self.__DOB=dob
    
    @property
    def get_age(self):
        return self.__age
    @get_age.setter
    def set_age(self,age):
        self.__age=age
    
    @property
    def get_email(self):
        return self.__email
    @get_email.setter
    def set_email(self,email):
        self.__email=email

    @property
    def get_phone(self):
        return self.__phone
    @get_phone.setter
    def set_phone(self,phn):
        self.__phone=phn
    
    @property
    def get_address(self):
        return self.__address
    @get_address.setter
    def set_address(self,addr):
        self.__address=addr

    @property
    def get_experience(self):
        return self.__experience
    @get_experience.setter
    def set_experience(self,exp):
        self.__experience=exp
    
    @property
    def get_staff_id(self):
        return self.__staff_id
    @get_staff_id.setter
    def set_staff_id(self,id):
        self.__staff_id=id

    @property
    def get_date_joining(self):
        return self.__joining_date
    @get_date_joining.setter
    def set_date_joining(self,date):
        self.__joining_date=date

    @property
    def get_role_id(self):
        return self.__role_id
    @get_role_id.setter
    def set_role_id(self,id):
        self.__role_id=id

    @property
    def get_username(self):
        return self.__username
    @get_username.setter
    def set_username(self,name):
        self.__username=name
    
    @property
    def get_passwrd(self):
        return self.__pass_wrd
    @get_passwrd.setter
    def set_passwrd(self,pw):
        self.__pass_wrd=pw

    @property
    def get_is_active(self):
        return self.__is_active
    @get_is_active.setter
    def set_is_active(self,status):
        self.__is_active=status
    
    @property
    def get_created_at(self):
        return self.__created_at
    
    @property
    def get_gender(self):
        return self.__gender
    @get_gender.setter
    def set_gender(self,gen):
        self.__gender=gen

    def __str__(self):
        return f"id: {self.__staff_id}| age: {self.__age}| username: {self.__username} | passwrd: {self.__pass_wrd} |created on: {self.__created_at}"

    
    # @staticmethod
    # def staff_id_gen():
    #     id=Staff.id_ini+1
    #     id_fin="EMP"+str(id) 
    #     return id_fin
    
    def age_calc(self):
        dob=self.get_DOB
        td = date.today()
        age= 0
        if dob:
              age = td.year-dob.year-((td.month, td.day) < (dob.month, dob.day))
        return age
    
    def passwrd_gen(self):
        name=self.get_staff_name
        passwrd=''
        if name:    
                passwrd=name[:3]+"2025"
        return passwrd

# emp=Staff("None","jothis",date(2003, 3, 21),"None","ksjothis@gmail.com","9446635761","hjsahsja",5,"10/12/2024",2,"None","None","y","None","M")
# print(emp)