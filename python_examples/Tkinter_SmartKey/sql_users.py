import sqlite3

conn = sqlite3.connect('Smart_Key.db')

cursor = conn.cursor()

# sqlite3.OperationalError: table 'xx' already exists -- sql IF NOT EXISTS
cursor.execute(""" CREATE TABLE IF NOT EXISTS Users (
                    username TEXT NOT NULL,
                    password INTEGER NOT NULL UNIQUE 
                                                 )""")


# kad je conn u context manageru ne treba .commit ...
def insert_user(username, password):
    with conn:
        try:
            cursor.execute('''INSERT INTO Users 
                             VALUES (:username, :password)''', {'username': username, 'password':password})
        except sqlite3.IntegrityError:
            return -1 #'Password already exists'


# return list of tuples all usernames
def all_users(): 
    cursor.execute('SELECT username FROM Users')
    return cursor.fetchall()


def update_user(username, new_username, new_password):
    # provjera postoji li stari username, updatea sa novim
    with conn:
        cursor.execute('''UPDATE Users 
                        SET username = :new_username, password = :new_pass
                        WHERE username = :user''', {'new_username':new_username, 'new_pass': new_password, 'user':username})


def delete_user(username):
    # provjera postoji li user
    cursor.execute('SELECT * FROM Users WHERE username = :user', {'user':username})
    ime = cursor.fetchone()
    
    if ime is None:
        return -1   
    
    else: # ako postoji username
        with conn:
            cursor.execute(' DELETE FROM Users WHERE username = :user', {'user':username})


def user_exist(password):
    # Ako postoji returns tuple, ako NE postoji --> None
    cursor.execute('SELECT username FROM Users WHERE password = :password', {'password':password})
    ime = cursor.fetchone()

    if ime != None:             # [0] jer je tuple pa vraca samo element u njemu -- username
        return ime[0]           # iz nekog razloga ne radi cursor.fetchone()[0] u if statementu      
    else:
        return ime              # returns None
                         


def user_exist_username(username):
    
    cursor.execute('SELECT * FROM Users WHERE username = :user', {'user' :username})
    ime = cursor.fetchone()
    return ime                  # returns None ako ne postoji




