import funkcije as f

def main():
    while True:

        f.options_menu()
        option = int(input('\n Choose an option\n>> '))

        if option == 1:
            f.create_dictionary()
        elif option == 2:
            f.load_orgs_from_json()
            f.wait()
        elif option == 3:
            f.specific_org_details()
        elif option == 4:
            f.edit_org_info()
        elif option == 5:
            f.delete_organization()
        elif option == 6:
            quit()
        else:
            print('\nOption does not exist. Please try again')
            f.wait()


main()
