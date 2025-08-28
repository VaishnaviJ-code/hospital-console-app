from models.staff import Staff

class Doctor(Staff):
    id_ini = 100

    def __init__(self, doctor_id, staff_id, dept_id, sp_id, consultation_fee,
                 staff_name=None, DOB=None, age=None, email=None, phone=None,
                 address=None, experience=None, joining_date=None, role_id=None,
                 username=None, pass_wrd=None, is_active=None, created_at=None, gender=None):
        
        # Call Staff constructor to set inherited fields
        super().__init__(
            staff_id=staff_id,
            staff_name=staff_name,
            DOB=DOB,
            age=age,
            email=email,
            phone=phone,
            address=address,
            experience=experience,
            joining_date=joining_date,
            role_id=role_id,
            username=username,
            pass_wrd=pass_wrd,
            is_active=is_active,
            created_at=created_at,
            gender=gender
        )

        # Doctor-specific fields
        self.__doctor_id = doctor_id
        self.__dept_id = dept_id
        self.__sp_id = sp_id
        self.__consultation_fee = consultation_fee

    # Doctor-specific getters/setters
    @property 
    def get_doc_id(self):
        return self.__doctor_id

    @get_doc_id.setter
    def set_doc_id(self, id):
        self.__doctor_id = id

    @property 
    def get_dept_id(self):
        return self.__dept_id

    @get_dept_id.setter
    def set_dept_id(self, id):
        self.__dept_id = id

    @property 
    def get_spcl_id(self):
        return self.__sp_id

    @get_spcl_id.setter
    def set_spcl_id(self, id):
        self.__sp_id = id

    @property 
    def get_consultation_fee(self):
        return self.__consultation_fee

    @get_consultation_fee.setter
    def set_consultation_fee(self, fee):
        self.__consultation_fee = fee
