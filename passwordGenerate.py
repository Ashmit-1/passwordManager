import random
import sqlite3
import encryption
from time import sleep

conn = sqlite3.connect("passkeys.db")
cursor = conn.cursor()

def generatePassword(n):
    wrd = ""
    for i in range(n):
        ran = chr(random.randrange(33, 126))
        wrd += ran
    for i in range(n//2):
        ran = random.randrange(0, 9)
        wrd += str(ran)
    return wrd
def passwords():
    myPassword = generatePassword(10)
    passList = list(myPassword)
    random.shuffle(passList)
    random.shuffle(passList)
    finalPass = ''
    for i in passList:
        finalPass += i
    print(f"\nYour password is: {str(finalPass)}")
    return str(finalPass)

def add_password():
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                    account TEXT NOT NULL,
                    passwrd TEXT NOT NULL
            )
        ''')
    account = input("You want to create password for: ")
    cursor.execute("SELECT * FROM passwords WHERE account = ?", (account,))
    if ( len(cursor.fetchall()) < 1):
        if(len(account) < 1):
            print("*" * 50)
            print("!! You didn't enter any name !!")
            print("*" * 50)
        else:
            cursor.execute("INSERT INTO passwords (account, passwrd) VALUES (?, ?)", (account, encryption.encryption(passwords())))
            conn.commit()
    else:
        print("*" * 70)
        print("Password for the account already exists !!\nTry with a different account or update password for existing account.")
        print("*" * 70)
        
def list_passwords():
    cursor.execute("SELECT * FROM passwords")
    print("ACCOUNT\t\t|\tPASSWORD")
    print("_" * 50)
    for row in cursor.fetchall():
        p_word = encryption.decryption(row[1])
        if (len(row[0]) < 8 and len(row[0]) > 0):
            print(f"{row[0]}\t\t|\t{p_word}")
        elif(len(row[0]) < 1):
            print(f"**NULL**\t|\t{p_word}")
        else:
            print(f"{row[0]}\t|\t{p_word}")

def update_password():
    try:
        old_account = input("Enter the account for which you want to change the password: ")
        cursor.execute("SELECT * FROM passwords WHERE account = ?", (old_account,))
        if ( len(cursor.fetchall()) < 1):
            print(f"!! You don't have passwords saved for account named \'{old_account}\' !! Try creating a new password")
        else:
            cursor.execute('''
            UPDATE passwords SET passwrd = ? WHERE account = ?''', (encryption.encryption(passwords()), old_account))
            conn.commit()
    except Exception as e:
        print("*" * 50)
        print("The entry does not exist !!")
        print("*" * 50)

def save_existing_password():
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                    account TEXT NOT NULL,
                    passwrd TEXT NOT NULL
            )
        ''')
    account = input("You want to save password for: ")
    cursor.execute("SELECT * FROM passwords WHERE account = ?", (account,))
    if ( len(cursor.fetchall()) < 1):
        if(len(account) < 1):
            print("*" * 50)
            print("!! You didn't enter any name !!")
            print("*" * 50)
        else:
            key = input("Enter the password for this account: ")
            cursor.execute('''
            INSERT INTO passwords (account, passwrd) VALUES (?, ?)
        ''',(account, encryption.encryption(key)))
            conn.commit()
    else:
        print("*" * 70)
        print("Password for the account already exists !!\nTry with a different account or update password for existing account.")
        print("*" * 70)

def delete_password():
    try:
        account = input("Enter the account for which you want to delete the password:  ")
        cursor.execute('''
        SELECT * FROM passwords WHERE account = ?
    ''',(account, ))
        if(len(cursor.fetchall()) < 1):
            print(f"!! You don't have passwords saved for account named \'{account}\' !!")
        else:
            cursor.execute("DELETE FROM passwords WHERE account = ?",(account, ))  
            conn.commit()
            print("*" * 50)
            print("Password deleted succesfully")
            print("*" * 50)
    except:
        print("!! ERROR !!")  
        

def main():
    try:
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                        account TEXT NOT NULL,
                        passwrd TEXT NOT NULL
                )
            ''')
        cursor.execute("SELECT * FROM passwords")
        if(len(cursor.fetchall()) < 1):
            encryption.generate_keys()
    except Exception as e:
        print("!!ERROR!!")
    while True:
        print()
        print("*********  WELCOME TO PASSWORD MANAGER  *********")
        print("--MENU--")
        sleep(0.5)
        print("1. Generate Passwords")
        print("2. Save an Existing Password")
        print("3. List Passwords")
        print("4. Delete a Password")
        print("5. Delete All Passwords")
        print("6. Update Existing Password")
        print("7. Exit App")
        choice = input("Enter choice: ")
        if (choice == "1"):
            try:
                add_password()
            except:
                print("!! ERROR !!")
        elif (choice == "2"):
            try:
                save_existing_password()
            except:
                print("!! ERROR !!")
        elif (choice == "3"):
            try:
                print("*" * 50)
                list_passwords()
                print("*" * 50)
            except Exception as e:
                print(e)
                print("No password found !! Create some atfirst")
                print("*" * 50)

        elif (choice == "4"):
            try:
                delete_password()
            except:
                print("!! ERROR !!")
        elif (choice == "5"):
            try:
                cursor.execute("DROP TABLE passwords")
                print("*" * 50)
                print("All Passwords Deleted Successfully")
                print("*" * 50)
            except:
                print("*" * 50)
                print("!! Add some passwords atfirst !!")
                print("*" * 50)
        elif (choice == "6"):
            try:
                update_password()
            except:
                print("!! ERROR !!")
        elif (choice == "7"):
            conn.close()
            break
        else:
            print("!! Enter correct choice !!")
        
if __name__ == "__main__":
    main()
