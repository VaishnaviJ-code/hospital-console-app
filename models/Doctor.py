from models.staff import Staff
class Doctor(Staff):
    id_ini=100

    
    def __init__(self, doctor_id, staff_id, dept_id, sp_id, consultation_fee):
        self.__doctor_id = doctor_id
        self.__staff_id =  staff_id
        self.__dept_id = dept_id
        self.__sp_id = sp_id
        self.__consultation_fee = consultation_fee

    @property 
    def get_doc_id(self):
        return self.__doctor_id
    @get_doc_id.setter
    def set_doc_id(self,id):
        self.__doctor_id=id

    @property 
    def get_staff_id(self):
        return self.__staff_id
    @get_staff_id.setter
    def set_staff_id(self,id):
        self.__staff_id=id

    @property 
    def get_dept_id(self):
        return self.__dept_id
    @get_dept_id.setter
    def set_dept_id(self,id):
        self.__dept_id=id

    @property 
    def get_spcl_id(self):
        return self.__sp_id
    @get_spcl_id.setter
    def set_spcl_id(self,id):
        self.__sp_id=id

    @property 
    def get_consultation_fee(self):
        return self.__consultation_fee
    @get_consultation_fee.setter
    def set_consultation_fee(self,fee):
        self.__consultation_fee=fee

    # def __str__(self):
    #     return f"Dr. {self.name} | Email: {self.email} | Phone :{self.phone}"
    
    # @staticmethod
    # def doctor_id_gen():
    #     Doctor.id_ini+=1
    #     id="DR"+str(Doctor.id_ini) 
    #     return id