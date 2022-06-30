from Customer import Customer

class Employee(Customer):
    def __init__(self, fname, lname, contact_num, id_number, salary):
        super().__init__(fname, lname, contact_num)
        self.id_number = id_number
        self.salary = salary

    @property            # nisam koristio
    def email(self):    
        return f'{(self.fname).lower()}.{(self.lname).lower()}@email.com'
    
    @property
    def fullname(self):
        return f'{self.fname} {self.lname}'

    def employee_info(self):
        print(f' Name: {self.fullname}\n ID:{self.id_number}\n Contact: {self.contact_num} | {self.email}\n Salary: {self.salary}€')

    def __str__(self):
        return f'{self.fullname}'

