from tkinter import *
from tkinter import messagebox
import sql_users 

root = Tk()
root.title("SMART KEY")
# root.geometry('850x700')

frame_1 = LabelFrame(root, text="Entrance", padx=200, pady=20, labelanchor=N)
frame_1.grid(row=0,column=0, padx=10, pady=10)

def user_del():
   
    global frame_delete_usr
    frame_options.grid_forget()

    frame_delete_usr = LabelFrame(frame_PIN_panel, text='Delete User', padx=30, pady=10, labelanchor=N )
    
    label_usr_name = Label(frame_delete_usr, text='Enter username to delete')
    name_entry = Entry(frame_delete_usr, width=35, borderwidth=3)

    frame_delete_usr.grid(row=2, column=0, sticky=N)
    label_usr_name.grid(row=0 , column=0)
    name_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    
    def cancel_del_usr():
        frame_delete_usr.grid_forget()
        admin_menu()

    def delete_user_sql():
        # u funkicji sam definirao da vrati -1 ako ne postoji
        # BOLJE DA SE MOZDA POZIVA ONA POSEBNA FUNKCIJA - sql_users.user_exist()
        user_exist = sql_users.delete_user(name_entry.get())
        
        if user_exist == -1:
            notification = messagebox.showerror("Error", "Username does NOT exist !")
            if notification == 'ok':
                name_entry.delete(0, END)
        else:
            notification = messagebox.askquestion("User Deleted", " USER DELETED !\n\n Delete Another User ?")
            
            if notification == 'yes':
                name_entry.delete(0, END)
            else:
                cancel_del_usr()


    delete_usr = Button(frame_delete_usr, text='Delete', padx=5, pady=5, command=delete_user_sql )
    cancel_delete = Button(frame_delete_usr, text='Cancel', padx=5, pady=5, command=cancel_del_usr )###
    
    delete_usr.grid(row=3, column=1)
    cancel_delete.grid(row=3, column=0)


def edit_user():
    global frame_edit_usr
    frame_options.grid_forget()

    frame_edit_usr = LabelFrame(frame_PIN_panel, text='Edit User', padx=30, pady=10, labelanchor=N )
    
    label_usr_name = Label(frame_edit_usr, text='Enter username to edit')
    name_entry1 = Entry(frame_edit_usr, width=35, borderwidth=3)

    frame_edit_usr.grid(row=2, column=0, sticky=N)
    label_usr_name.grid(row=0 , column=0)
    name_entry1.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # sve cancel fukcije su mogle i sa lambdom u samom buttonu
    def cancel_edit_usr():
        frame_edit_usr.grid_forget()
        admin_menu()
        
    
    def update_usr_info():
       
        usr_exst = sql_users.user_exist_username(name_entry1.get())
       
        if usr_exst == None:
            notification = messagebox.showerror("Error", " Username does NOT exist !")
            if notification == 'ok':
                name_entry1.delete(0, END)

        else:
            frame_edit_usr.grid_forget()
            # global frame_edit_usr_1
            frame_edit_usr_1 = LabelFrame(frame_PIN_panel, text='Edit User', padx=30, pady=10, labelanchor=N )
            
            label_usr_name = Label(frame_edit_usr_1, text='New username')
            name_entry_2 = Entry(frame_edit_usr_1, width=35, borderwidth=3)
            name_entry_2.insert(0, name_entry1.get() )
            
            label_usr_pass = Label(frame_edit_usr_1, text='New password (PIN)')
            pass_entry_2 = Entry(frame_edit_usr_1, width=35, borderwidth=3)
            

            frame_edit_usr_1.grid(row=2, column=0, sticky=N)

            label_usr_name.grid(row=0 , column=0)
            label_usr_pass.grid(row=2 , column=0)

            name_entry_2.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
            pass_entry_2.grid(row=3 , column=0)


            def save_changes():

                sql_users.update_user(name_entry1.get(), name_entry_2.get(), int(pass_entry_2.get()))

                notification = messagebox.askquestion("Changes saved", " Edit new user?")
                if notification == 'yes':
                    frame_edit_usr_1.grid_forget()
                    edit_user()
                else:
                    frame_edit_usr_1.grid_forget()
                    admin_menu()




            edit_usr_name = Button(frame_edit_usr_1, text='Save changes', padx=5, pady=5, command=save_changes ) ###
            cancel_edit = Button(frame_edit_usr_1, text='Cancel', padx=5, pady=5, command=lambda:[frame_edit_usr_1.grid_forget(), admin_menu()])
            
            edit_usr_name.grid(row=4, column=1)
            cancel_edit.grid(row=4, column=0)




            




    edit_usr_name = Button(frame_edit_usr, text='Edit User', padx=5, pady=5, command=update_usr_info )
    # edit_usr_pass = Button(frame_edit_usr, text='Edit PIN', padx=5, pady=5)
    cancel_edit = Button(frame_edit_usr, text='Cancel', padx=5, pady=5, command=cancel_edit_usr)
    
    edit_usr_name.grid(row=3, column=2)
    # edit_usr_pass.grid(row=3, column=1)
    cancel_edit.grid(row=3, column=0)


    



def add_user():

    global frame_add_usr
    frame_options.grid_forget()


    frame_add_usr = LabelFrame(frame_PIN_panel, text='Add User', padx=30, pady=10, labelanchor=N )
    
    label_usr_name = Label(frame_add_usr, text='New Username')
    name_entry = Entry(frame_add_usr, width=35, borderwidth=3)

    label_usr_pass = Label(frame_add_usr, text='PIN (4 numbers)')
    pass_entry = Entry(frame_add_usr, width=35, borderwidth=3)

    frame_add_usr.grid(row=2, column=0, sticky=N)
    label_usr_name.grid(row=0 , column=0)
    name_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    label_usr_pass.grid(row=2 , column=0)
    pass_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    
    def cancel_add_usr():
        frame_add_usr.grid_forget()
        admin_menu()
    
    def save_usr(): # uzima novi username i password(pin) i sprema u dictionary
        # users[int(password)] = username ######

        user_exist = sql_users.insert_user(name_entry.get(), int(pass_entry.get()))  # returns -1 ako vec postoji passwrd
        if user_exist == -1:
            notification = messagebox.showerror("Error", "Provided PIN already exists !")
            if notification == 'ok':
                pass_entry.delete(0, END)
                # add_user()

        else:
            response = messagebox.askquestion("User Created", " USER CREATED !\n\n Add New User ?")
            
            if response == 'yes':
                name_entry.delete(0, END)
                pass_entry.delete(0, END)
                # add_user()
            else:
                cancel_add_usr()


    save_new_usr = Button(frame_add_usr, text='Save', padx=5, pady=5, command=save_usr)
    cancel_new_usr = Button(frame_add_usr, text='Cancel', padx=5, pady=5, command=cancel_add_usr )
    
    save_new_usr.grid(row=4, column=1)
    cancel_new_usr.grid(row=4, column=0)

 
    



def list_of_users():
    global list_frame
    frame_options.grid_forget()
    list_frame = LabelFrame(frame_PIN_panel, text=' List of Users ', padx=35, pady=10, labelanchor=N)
    list_frame.grid(row=2, column=0, sticky=N, padx=10, pady=10) 
    
    users = sql_users.all_users()
    
    for usr in users:
        Label(list_frame, text=usr[0]).pack()    # [0] jer je usr tuple --> ('Admin',) 
    
    ok_button = Button(frame_PIN_panel, text='OK', padx=30, pady=5, command=lambda: [list_frame.grid_forget(), ok_button.grid_forget(), admin_menu()])
    # ok_button = Button(list_frame, text='OK', padx=5, pady=5, command=lambda: [list_frame.grid_forget(), admin_menu()])
    
    ok_button.grid(row=2, column=1)
    # ok_button.pack()



def admin_menu():
    
    global frame_options
    
    frame_options = LabelFrame(frame_PIN_panel, text='Options' , padx=45, pady=30, labelanchor='n')
    frame_options.grid(row=1, column=0, padx=10, pady=10, sticky=N) 
    
    # Option Buttons
    button_usrs_list= Button(frame_options, text='List of Users', padx=16, pady=10, command=list_of_users)
    button_usrs_edit= Button(frame_options, text='Edit Users', padx=20, pady=10, command=edit_user)
    button_usrs_add = Button(frame_options, text='Add Users', padx=21, pady=10, command=add_user)
    button_usrs_delete = Button(frame_options, text='Delete Users', padx=13, pady=10, command=user_del)

    # Grid Option Buttons
    button_usrs_list.grid(row=0, column=0)
    button_usrs_edit.grid(row=0, column=1)
    button_usrs_add.grid(row=1, column=0)
    button_usrs_delete.grid(row=1, column=1)

    


def enter_pin():
    
    # Pin Panel Frame    
    global frame_PIN_panel
   
    frame_PIN_panel = LabelFrame(root, text='PIN panel', padx=50, pady=20, labelanchor=N)
    frame_PIN_panel.grid(row=1, column=0, sticky=N, padx=10, pady=10)

    # PIN & INFO
    global frame_keyboard

    frame_keyboard = LabelFrame(frame_PIN_panel, text='Enter your password', padx=30, pady=50, labelanchor=N)
    frame_keyboard.grid(row=0, column=0, padx=5, pady=10)
    

    e = Entry (frame_keyboard, width=35, borderwidth=3)
    e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)



    def button_add(number):
        # e.delete(0,END)
        current = e.get()
        e.delete(0, END)
        e.insert(0,str(current) + str(number))
        return
    
    def button_clear():
        e.delete(0,END)

    def enter():
        
        check_usr = sql_users.user_exist(int(e.get()))  # vraca username ovisno o upisanom PINu, None-ne postoji
        
        if check_usr == 'Admin':
            
            button_clear()
            frame_keyboard.grid_forget() 
            global label_welcome_admin
            
            label_welcome_admin = Label(frame_PIN_panel, text = 'WELCOME ADMIN !', padx=5, pady=7)
            label_welcome_admin.grid(row=0, column=0)
            admin_menu() 
        
        elif check_usr == None:
             # user does not exist / incorrect PIN
            button_clear()
            e.insert(0, 'INCORRECT PIN')
       
        else:                                       # user koji nije Admin
            
            button_clear()
            frame_keyboard.grid_forget()
            
            try:                               # zaboravio sam zasto je ovdje try, valjda se logira nakon admina
                frame_options.grid_forget()
            except NameError:  
                pass

            global label_welcome_usr
            label_welcome_usr = Label(frame_PIN_panel, text = (f'Welcome Home {check_usr} !').upper(), padx=5, pady=10)
            label_welcome_usr.grid(row=0, column=0)

         
    
    # Define Buttons
    button1= Button(frame_keyboard, text='1', padx=40, pady=20, command=lambda: button_add(1))
    button2= Button(frame_keyboard, text='2', padx=40, pady=20, command=lambda: button_add(2))
    button3= Button(frame_keyboard, text='3', padx=40, pady=20, command=lambda: button_add(3))
    button4= Button(frame_keyboard, text='4', padx=40, pady=20, command=lambda: button_add(4))
    button5= Button(frame_keyboard, text='5', padx=40, pady=20, command=lambda: button_add(5))
    button6= Button(frame_keyboard, text='6', padx=40, pady=20, command=lambda: button_add(6))
    button7= Button(frame_keyboard, text='7', padx=40, pady=20, command=lambda: button_add(7))
    button8= Button(frame_keyboard, text='8', padx=40, pady=20, command=lambda: button_add(8))
    button9= Button(frame_keyboard, text='9', padx=40, pady=20, command=lambda: button_add(9))
    button0= Button(frame_keyboard, text='0', padx=40, pady=20, command=lambda: button_add(0))
    button_c = Button(frame_keyboard, text='Clear', padx=30,pady=20, command=button_clear)
    buttonEnter = Button (frame_keyboard, text='OK', padx=35,pady=20, command=enter)

    # Grid Buttons
    button1.grid(row=3,column=0)
    button2.grid(row=3,column=1)
    button3.grid(row=3,column=2)

    button4.grid(row=2,column=0)
    button5.grid(row=2,column=1)
    button6.grid(row=2,column=2)

    button7.grid(row=1,column=0)
    button8.grid(row=1,column=1)
    button9.grid(row=1,column=2)

    button0.grid(row=4,column=0)
    button_c.grid(row=4,column=1)
    buttonEnter.grid(row=4,column=2)

# ZVONO I PIN 
click = 1  # pojavi se/brise poruka svaki put kad se klikne 
def bell_ring():
    global click, msg
    if click % 2 == 1:
        msg = Label(frame_1,text=f'\nPlease wait...')
        msg.grid(row=1,column=0,columnspan=2)
    else:
        msg.destroy()
    click += 1
    

image_in_button = PhotoImage(file='icons/zvono.png').subsample(9)
image_in_button2 = PhotoImage(file='icons/keypad.png').subsample(9)

bell = Button (frame_1, image=image_in_button, padx=20, pady=20, command=bell_ring)
enter_pin = Button (frame_1, image=image_in_button2, padx=20, pady=20, command=enter_pin)

bell.grid(row=0,column=0)
enter_pin.grid(row=0,column=1)


root.mainloop()