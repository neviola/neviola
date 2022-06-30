class Organization:
    
    def __init__(self, name, id_number, contact_num, employees = None, customers = None):
        self.name = name
        self.id_number = id_number
        self.contact_num = contact_num        
        if employees is None:
            self.employees = []
        else:
            self.employees = employees
        if customers is None:
            self.customers = []
        else:
            self.customers = customers

    def organization_info(self):
        print(f'Name of Organization: {self.name}\nOrganization ID: {self.id_number}\nContact Number: {self.contact_num}')
        print(f'List of Empoloyees:\n{self.employees}\nList of Customers:\n{self.customers}')
    
    def organization_to_txt(self):
        return f'{self.name}, {self.id_number}, {self.contact_num}, {self.employees}, {self.customers}'
    
    def __str__(self):
        return f'{self.name} {self.id_number}'



# org = Organization('algebra', '1515', '59155555', ['marko', 'marin'], ['mario', 'luka'])
# lista = [org]
# org.organization_info()
# print(lista)