class Test:
    def __init__(self,test_id, test_name, description, price, status):
        self.test_id = test_id
        self.test_name = test_name
        self.description = description
        self.price = price
        self.status = status

    def __str__(self):
        return f"ID: {self.test_id}, Name: {self.test_name}, Price: {self.price}, Status: {self.status}"