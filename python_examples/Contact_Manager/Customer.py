class Customer:
    def __init__(self, fname, lname, contact_num):
        self.fname = fname
        self.lname = lname
        self.contact_num = contact_num

    def customer_info(self):
        print(f'{self.fname} {self.lname}  {self.contact_num}')
    
    def fullname(self):
        return f'{self.fname} {self.lname}'

    def __repr__(self):
        return f'{self.fullname()}'
    
    def __str__(self):
        return f'{self.fullname()}'

