from Organization import Organization
from Employees import Employee
from Customer import Customer
import os
import msvcrt as m
import json


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def new_title(title):
    clear_screen()
    print('-' * 65)
    print(f'\t\t\t {(title).upper()}')
    print('-' * 65)
    print()


# 1a
def create_dictionary():
    with open('Organization_info.json') as f:
        organization_dict = json.load(f)     
        
    new_org_list = add_organization()               # stvaram novu listu instanci organization
    
    for org in new_org_list:                        # za svaku instancu organization u toj listi
       
        new_emps_list = []                          # lista dictionarya employee instanci za svaku instancu organization
        new_cstmrs_list = []
        for emp in org.employees:
            new_emp = {
                    "fname": emp.fname,
                    "lname": emp.lname,
                    "contact": emp.contact_num,
                    "id": emp.id_number,
                    "salary": emp.salary
            }
            new_emps_list.append(new_emp)           
        
        for cstmr in org.customers:
            new_cstmr = {
                    "fname": cstmr.fname,
                    "lname": cstmr.lname,
                    "contact": cstmr.contact_num
            }
            new_cstmrs_list.append(new_cstmr)
       
        # stvara novi dictonary za svaku org, appenda se na ucitani dict iz jsona pa ponovo pise u json sve zajedno
        new_org = {
            "name": org.name,
            "id": org.id_number,
            "contact": org.contact_num,
            "employees": new_emps_list,
            "customers": new_cstmrs_list
        }
        organization_dict['organization'].append(new_org)      # dodaje se svaki novi rjecnik iz nove liste instanci 'organization' 
   
    with open('Organization_info.json', 'w') as f:             # sada rjecnik sa dodanim organizacijama pretvaram u json
        json.dump(organization_dict, f, indent=4)
    

def add_organization():    # stvara i returna listu instanci organization

    organizations_list = []    
    
    while True:
        new_title('ADD NEW ORGANIZATION')
        org_name = input(' Name of organization: ')
        org_id = input(' ID of organization: ')
        org_contact = input(' Contact number of organization: ')
        
        emps_list = add_emp()       # reminder, ove liste su izvan scopea onih u pozvanim funkicijama, samo se isto zovu
        custmr_list = add_custmr()

        org_instance = Organization(org_name, org_id, org_contact, emps_list, custmr_list )
        organizations_list.append(org_instance)

        print('\n Organization added successfully!\n ')
        option = input(' [a] Add new organization  |  [Enter] Save and Return to main menu\n >> ')
        if option == 'a':
            continue
        else:
            return organizations_list


# 1b
def add_emp():                      # stvara i returna listu employeea za svaku instancu organization
   
    emps_list = []

    while True:
        new_title('ADD NEW EMPLOYEE')    
        print('\t\tEmployees information...\n')
        emp_fname = input(' First name: ')
        emp_lname = input(' Last name: ')
        emp_id = int(input(' ID of employee [int]: '))
        emp_contact = input(' Contact number: ')
        emp_salary = float(input(' Salary [€/y]: '))

        emp_instance = Employee(emp_fname, emp_lname, emp_contact, emp_id, emp_salary)
       
        emps_list.append(emp_instance)
        print('\n Employee Added!\n')

        option = input(' [a] Add another Employee  |  [Enter] Countinue to customers\n >> ')
        if option == 'a':
            continue
        else:
            return emps_list

# 1c
def add_custmr():
    
    custmr_list = []

    while True:
        new_title('ADD NEW CUSTOMER')
        print('\t\tCustomer information...\n')
        custmr_fname = input(' First name: ')
        custmr_lname = input(' Last name: ')
        custmr_contact = input(' Contact number: ')

        custmr_instance = Customer(custmr_fname, custmr_lname, custmr_contact)
        custmr_list.append(custmr_instance)
        print('\n Customer Added!\n')

        option = input(' [a] Add another Customer  |  [Enter] Countinue to finish up\n >> ')
        
        if option == 'a':
            continue
        else:
            return custmr_list


def wait():
    print('\nPress any button to countinue...\n')
    m.getch()


# 2
def load_orgs_from_json(title='list of managed organizations'):

    new_title(title)
    try:
        with open('Organization_info.json') as f:
            data = json.load(f)
        
        print(' \t Name\t\t ID\n')
        for org in data['organization']:
            print(f'\t{org["name"]}\t\t {org["id"]}')
        return data

    except FileNotFoundError:
        print(' File does not exist!')
        wait()
        # load_orgs_from_json()


def specific_org_print(data, specific_org_name):                 # args - data dict i trazena organizacija
    try:
        for i in range(len(data['organization'])+1):             # +1 ako ne nade -->indexError --> ponovi/izađi
            if data['organization'][i]['name'] == specific_org_name:
                org = data['organization'][i]                    # za laksi pristup u printu

                print (f"\n\n  Organization: {org['name'].upper()}\t ID: {org['id']}\t Contact: {org['contact']} ")

                print('\n\n\t Employees info\n')
                for emp in org['employees']:
                    print(f"\t Name: {emp['fname']} {emp['lname']}\t ID: {emp['id']}\t Salary: {emp['salary']}€\t Phone: {emp['contact']}")

                print('\n\n\t Customers info\n')
                for cstmr in org['customers']:
                    print(f"\t Name: {cstmr['fname']} {cstmr['lname']}\t Phone: {cstmr['contact']}")

                return org                                       # print pa izlazi iz petlje, ne javlja IndexError
                                              
    except IndexError:
        print('\n Entered organization does not exist.\n')
        return -1

# 3
def specific_org_details():

    data = load_orgs_from_json('organization information')
    print()
    specific_org_name = input(' Enter name of the organization for more information\n >> ')
    new_title('informaion details')    ###
    specific_org_print(data, specific_org_name)

    option = input('\n\n [a] Try again  |  [Enter] Return to main menu\n >> ')
    if option == 'a':
        specific_org_details()
    else:
        return 


# 4 EDIT INFO

def edit_org_info():
    data = load_orgs_from_json('edit organization information')   # povlaci data dict iz json

    specific_org_name = input('\n Enter name of the organization to edit information\n >> ')

    org = specific_org_print(data, specific_org_name )
    if org == -1:                                                                                                       # -1 ako je exception, ne postoji org
        option = input('\n\n [y] Try again  |  [Enter] Return to main menu\n >> ')          
        if option == 'y':
            edit_org_info()
        else:
            return

    def edit_organization_emp():
        while True:
            new_title('list of employees')
            print('\n Employees\n\n')
            # printa sve emp za odabranu org
            for emp in org['employees']:              # = in data['organization'][i]['employees']
                print(
                    f"\t Name: {emp['fname']} {emp['lname']}\t ID: {emp['id']}\t Salary: {emp['salary']}€\t Phone: {emp['contact']} ")

            option = input('\n (a) Add employee | (d) Delete employee | (e) Edit employee | (s) Return/Save\n >>')  # izlazi iz edit_org == 4
            
            if option == 'e':    

                spec_emp_id = int(input('\n Enter ID of the employee to edit information\n >> '))

                try:
                    for i in range(len(org['employees']) + 1):        # +1 ako ne nade ->indexError -> ponovi/izađi
                        if org['employees'][i]['id'] == spec_emp_id:  # prolazi kroz svaki emp i provjerava ID
                            emp_spec = org['employees'][i]            # sada imam odabrani employee za edit
                            break

                    def emp_info_print():
                        print(
                            f"\n Name: {emp_spec['fname']} {emp_spec['lname']}\t ID: {emp_spec['id']}\t Salary: {emp_spec['salary']}€\t Phone: {emp_spec['contact']}")

                    while True: 
                        new_title('edit employee info')
                        emp_info_print()
                        print('\n What do you want to edit?\n')
                        emp_option = input(
                            ' (1) First name | (2) Last name | (3) ID | (4) Salary | (5) Phone | (s) Save employee info\n >> ')

                        if emp_option == '1':
                            new_fname = input('\n New First name\n >> ')
                            emp_spec['fname'] = new_fname
                            print('\n Employee First name updated!')
                            wait()
                        elif emp_option == '2':
                            new_lname = input('\n New Last name\n >> ')
                            emp_spec['lname'] = new_lname
                            print('\n Employee Last name updated!')
                            wait()
                        elif emp_option == '3':
                            new_emp_id = int(input('\n New ID for employee\n >> '))
                            emp_spec['id'] = new_emp_id
                            print('\n Employee ID name updated!')
                            wait()
                        elif emp_option == '4':
                            new_salary = float(input('\n New Salary amount for employee\n >> '))
                            emp_spec['salary'] = new_salary
                            print('\n Employee Salary amount updated!')
                            wait()
                        elif emp_option == '5':
                            new_phone = input('\n New Phone number for employee\n >> ')
                            emp_spec['contact'] = new_phone
                            print('\n Employee Phone number updated!')
                            wait()
                        elif emp_option == 's':
                            break
                        else:
                            print(' Option does not exist.\n')
                            wait()
                            continue

                except IndexError:
                    print('\n Entered employee does not exist.\n')
                    option = input('\n\n [y] Try again  |  [Enter] Return to editing organization\n >> ')
                    if option == 'y':
                        continue
                    else:
                        break
                    	
            elif option =='a':
                print('\n Add new employee\n')
                fname = input(' Enter First name: ')
                lname = input(' Enter Last name: ')
                id = int(input(' Enter ID: '))
                salary = float(input(' Enter Salary [€/y]: '))
                contact = input(' Enter phone number: ')
                new_emp = {
                    "fname": fname,
                    "lname": lname,
                    "contact": contact,
                    "id": id,
                    "salary": salary
                }
                org['employees'].append(new_emp)
                print('\n New employee added! ')
                wait()

            elif option == 'd':
                print('\n Delete existing employee\n')
                id = int(input(' Enter ID of the employee: '))
                try:
                    for i in range(len(org['employees'])+1):                
                        if org['employees'][i]['id'] == id :
                            del org['employees'][i]
                            print('\n Employee deleted')
                            wait()
                            break          
                except IndexError:
                    print('\n Entered employee does not exist.\n')
                    wait()
                        
            else:
                break


    def edit_organization_cstmr():
        while True:
            new_title('list of customers')
            print('\n Customers\n\n')
            for cstmr in org['customers']:  # org vec imam odozgo
                print(f"\t Name: {cstmr['fname']} {cstmr['lname']}\t Phone: {cstmr['contact']} ")
           
            # izlazi iz edit_org == 4
            option = input('\n (a) Add customer | (d) Delete customer | (e) Edit customer | (s) Return/Save\n >>')  
            
            #### add, delete customer, edit, save
            
            if option == 'e':
                
                cstmr_fname, cstmr_lname = input('\n Enter full name of the customer to edit information\n >>').split(
                    ' ')

                try:
                    for i in range(len(org['customers']) + 1):
                        if org['customers'][i]['fname'] == cstmr_fname and org['customers'][i]['lname'] == cstmr_lname:
                            cstmr_spec = org['customers'][i]
                            break

                    def cstmr_info_print():
                        print(f"\t Name: {cstmr_spec['fname']} {cstmr_spec['lname']}\t Phone: {cstmr_spec['contact']} ")

                    cstmr_info_print()

                    while True:
                        new_title('edit customer info')
                        cstmr_info_print()
                        print('\n What do you want to edit?\n')
                        cstmr_option = int(
                            input(' (1) First name | (2) Last name | (3) Phone | (4) Save customer info\n >> '))

                        if cstmr_option == 1:
                            new_fname = input('\n New First name\n >> ')
                            cstmr_spec['fname'] = new_fname
                            print('\n Customer First name updated!')
                            wait()
                        elif cstmr_option == 2:
                            new_lname = input('\n New Last name\n >> ')
                            cstmr_spec['lname'] = new_lname
                            print('\n Customer Last name updated!')
                            wait()
                        elif cstmr_option == 3:
                            new_phone = input('\n New Phone number for customer\n >> ')
                            cstmr_spec['contact'] = new_phone
                            print('\n Customer Phone number updated!')
                            wait()
                        elif cstmr_option == 4:
                            break
                        else:
                            print('\n Option does not exist.\n')
                            wait()
                            continue

                except IndexError:
                    print('\n Entered customer does not exist.\n')
                    option = input('\n [y] Try again  |  [Enter] Return to editing organization\n >> ')
                    if option == 'y':
                        continue
                    else:
                        break
            
            elif option == 'a':
                print('\n Add new customer\n')
                fname = input(' Enter First name: ')
                lname = input(' Enter Last name: ')
                contact = input(' Enter phone number: ')
                new_cstmr = {
                    "fname": fname,
                    "lname": lname,
                    "contact": contact
                }
                org['customers'].append(new_cstmr)
                print('\n New customer added! ')
                wait()

            elif option == 'd':
                print('\n Delete existing customer\n')
                fname = input(' Enter First name of the customer: ')
                lname = input(' Enter Last name of the customer: ')
                try:
                    for i in range(len(org['customers'])+1):                
                        if org['customers'][i]['fname'] == fname and org['customers'][i]['lname'] == lname:
                            del org['customers'][i]
                            print('\n Customer deleted')
                            wait()
                            break          
                except IndexError:
                    print('\n Entered customer does not exist.\n')
                    wait()
            
            else:
                break
    
    while True:
        new_title('edit organization information')
        specific_org_print(data, specific_org_name )   
        print('\n\n What do you want to edit?\n')
        edit_org = input(' (1) Name | (2) ID | (3) Contact | (4) Employees | (5) Customers | (s) Save Changes\n >> ')

        if edit_org == '1':
            new_name = input('\n New name of the organization\n >>')
            org['name'] = new_name                       # data['organization'][i]['name'] = new_name
            specific_org_name = new_name              
            # print(' Organization name updated!\n')
        elif edit_org == '2':
            new_id = int(input('\n New id of the organization\n >>'))
            org['id'] = new_id
            # print(' Organization id updated!\n')
        elif edit_org == '3':
            new_contact = input('\n New contact of the organization\n >>')
            org['contact'] = new_contact
            # print(' Organization contact updated!\n')
        elif edit_org == '4':                                                  
            edit_organization_emp()
        elif edit_org == '5':                                                  
            edit_organization_cstmr()
        elif edit_org == 's':
            with open('Organization_info.json', 'w') as f:      # sada rjecnik sa updated organizacijama pretvaram u json
                json.dump(data, f, indent=4)
            break
        else:
            print(' Option does not exist\n')
            wait()
            continue


    option = input('\n\n [e] Edit new organization  |  [Enter] Return to main menu\n >> ')
    if option == 'e':
        edit_org_info()
    else:
        return


# 5
def delete_organization():
    new_title('delete organization')

    with open('Organization_info.json') as f:
        data = json.load(f)
    print(' \t Name\t\t ID\n')
    
    for org in data['organization']:
        print(f'\t{org["name"]}\t\t {org["id"]}')

    to_delete = input('\n Enter name of the organization to delete\n >> ')
    try:
        for i in range(len(data['organization'])+1):                # brise sve info i organizaciju
            if data['organization'][i]['name'] == to_delete:
                del data['organization'][i]
                print(' Organization deleted!\n')
                break
        
    except IndexError as e:
        # print(e)
        print(' Entered organiazation does not exist.\n')
   
    with open('Organization_info.json', 'w') as f:                  # pise novi json sa izbrisanim
        json.dump(data, f, indent=4)

    option = input(' [d] Delete/try again  |  [Enter] Return to main menu\n >> ')
    if option == 'd':
        delete_organization()
    else:
        return 



def options_menu():
    clear_screen()
    print('_' * 65)
    print()
    print('\t\t\t MAIN MENU')
    print('_' * 65)
    print()
    print('''
 1. ADD ORGANIZATION
 2. LIST OF ORGANIZATIONS
 3. DISPLAY SPECIFIC ORGANIZATION
 4. EDIT ORGANIZATION INFO
 5. DELETE ORGANIZATION
 6. EXIT''')
