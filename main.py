import sqlite3
import getpass
import datetime
import os, sys
import time

__now = datetime.datetime.now()

connection = sqlite3.connect('passwords.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    ID INTEGER PRIMARY KEY,
    name_of_password VARCHAR,
    username VARCHAR,
    password VARCHAR,
    date_of_created TEXT
)
""")

connection.commit()
connection.close()


class passwords:
    def __init__(self, id_num=-1, name_of_password="",username="", password="", date_of_created=""):
        self.id_num = id_num
        self.username = username
        self.name_of_password = name_of_password
        self.password = password
        self.date_of_created = date_of_created
        self.connection = sqlite3.connect("passwords.db")
        self.cursor = self.connection.cursor()

    def load_passwords(self, id_num, name_of_password):
        self.cursor.execute("""
        SELECT * FROM passwords 
        WHERE name_of_password = '{}'        
        """.format(id_num, name_of_password))

        result = self.cursor.fetchone()

        self.id_num = id_num
        self.name_of_password = result[1]
        self.password = result[2]
        self.date_of_created = result[3]

    def insert_pwd(self):
        self.cursor.execute("""
        INSERT INTO passwords VALUES
        ({}, '{}', '{}', '{}', '{}')
        """.format(self.id_num, self.name_of_password, self.username, self.password, self.date_of_created))

        self.connection.commit()
        self.connection.cursor()


#checking enyered password is correct or not

class db_pwd:
    def __init__(self, ID=-1):
        self.ID = ID
        self.connection = sqlite3.connect("passwords.db")
        self.cursor = self.connection.cursor()

    def load_passwords(self, ID):
        self.cursor.execute("""
        SELECT * FROM db_password 
        WHERE ID = {}
        """.format(ID))

        result = self.cursor.fetchone()
        self.password = result[1]
        self.date_of_created = result[2]

        self.log_pwd = self.password

        return self.log_pwd

        self.connection.commit()
        self.connection.close()

#end checking password

#mainactivity

def mainactivity():

    class main:
        def __init__(self, URL="", usern="", pawd="", now=""):
            self.usern = usern
            self.URL = URL
            self.pawd = pawd
            self.now = now

            self.connection = sqlite3.connect("passwords.db")
            self.cursor = self.connection.cursor()

        def showpasswords(self):
            self.cursor.execute("SELECT * FROM passwords")
            self.result = self.cursor.fetchall()

            l = len(self.result)

            i = 1


            if l == 0:
                print("you have no saved passwords")
            else:
                while i <= l:
                    self.cursor.execute("""
                    SELECT * FROM passwords 
                    WHERE ID = {}
                    """.format(i))
                    result = self.cursor.fetchone()

                    _id = result[0]
                    _pwd_name = result[1]
                    _pawd_usrn = result[2]
                    _pawd = result[3]
                    _date = result[4]

                    print("                                  ")
                    print("___", i ,"___")
                    print("                 ")
                    print("Account Name or site URL:",_pwd_name)
                    print("Username of", _pwd_name , ":" , _pawd_usrn)
                    print("Password of", _pawd_usrn, ":", _pawd)
                    print("Date of created:", _date)
                    print("_____________________________________________________________________________________________________________")

                    i += 1

                print("   ")
                print("""
                            [01] Edit information.
                            [02] Delete Password.
                """)




            print("   ")
            print("               ")
            print("     [00] Back.")
            print("     [99] Exit.")
            print("         ")

            iput = input("Enter no:")

            if iput == "0" or iput == "00":
                mainactivity()
            elif iput == "9" or iput == "99":
                print("Good Bye!")
            elif iput == "01" or iput == "1":
                connection = sqlite3.connect('passwords.db')
                cursor = connection.cursor()

                print("""
                    [01] Edit Username.
                    [02] Edit Password.
                """)

                _input = input("Enter No")

                if _input == "01" or _input == "1":
                    _id = input("[##]Enter ID of password you want to edit:")

                    _username = input("Enter new user name:")

                    print("""
                        [01]Save and exit.
                        [02]Discard.
                    """)

                    choice = input('Enter no:')

                    if choice == "01" or choice == "1":
                        try:
                            cursor.execute("""
                            UPDATE passwords 
                            SET username = '{}'
                            WHERE ID = {}
                            """.format(_username, _id))
                            print("Saved!")
                        except:
                            print("Something went wrong changes dosen't save.")
                        mainactivity()

                    elif choice == "02" or choice == "2":
                        mainactivity()

                elif _input == "02" or _input == "2":
                    _id = input("[##]Enter ID of password you want to edit:")

                    _pwd = getpass.getpass(prompt='Enter new password:')
                    _re_p = getpass.getpass(prompt='Verify new password:')

                    if _pwd == _re_p:
                        print("""
                                [01]Save and exit.
                                [02]Discard.
                        """)

                        choice = input('Enter no:')

                        if choice == "01" or choice == "1":
                            try:
                                cursor.execute("""
                                UPDATE passwords 
                                SET password = '{}'
                                WHERE ID = {}
                                """.format(_pwd, _id))
                                print("Saved!")
                            except:
                                print("Something went wrong changes dosen't save.")
                            mainactivity()

                        elif choice == "02" or choice == "2":
                            mainactivity()
                    else:
                        print("Two passwords dosen't match.")

                connection.commit()
                connection.close()

            elif iput == "02" or iput == "2":
                connection = sqlite3.connect('passwords.db')
                cursor = connection.cursor()

                _del = input("[##]Enter Id of password you want to delete:")

                chice = input("Are you sure you want to delete this (y/n):")

                if chice == "y" or chice == "Y":
                    try:
                        cursor.execute("""
                        DELETE FROM passwords WHERE id = {}
                        """.format(_del))
                        print("Deleted!")
                        mainactivity()
                    except:
                        print("something went wrong can't delete..")
                elif chice == "n" or chice == "N":
                    mainactivity()
                else:
                    print("wrong input..")
                    mainactivity()

                connection.commit()
                connection.close()


            else:
                print("wrong input.....")
                mainactivity()

            return l


        def AddNew(self, URL, usern,  pawd, now):
            self.cursor.execute("SELECT * FROM passwords")
            self.result = self.cursor.fetchall()

            l = len(self.result) + 1

            ID = l

            def check():
                try:
                    p1 = passwords(ID, URL, usern, pawd, now)
                    p1.insert_pwd()
                    return True
                except sqlite3.OperationalError:
                    return False

            if check() == True:
                print("password added succssefully")
            else:
                print("Somthing went wrong")

            print(
                "_____________________________________________________________________________________________________________")
            print("   ")
            print("     [00] Back.")
            print("     [99] Exit.")
            print("         ")

            iput = input("Enter no:")

            if iput == "0" or iput == "00":
                mainactivity()
            elif iput == "9" or iput == "99":
                print("Good Bye!")


        def Searchpassword(self, s_usern="", s_URL=""):
            if s_usern == "not_valid":
                try:
                    self.cursor.execute("""
                    SELECT * FROM passwords 
                    WHERE name_of_password = '{}'
                    """.format(s_URL))

                    D_result = self.cursor.fetchone()

                    U_s_id = D_result[0]
                    U_s_pwd_name = D_result[1]
                    U_s_pawd_usrn = D_result[2]
                    U_s_pawd = D_result[3]
                    U_s_d = D_result[4]

                    print("                                  ")
                    print("___", U_s_id, "___")
                    print("                 ")
                    print("Account Name or site URL:", U_s_pwd_name)
                    print("Username of", U_s_pwd_name, ":", U_s_pawd_usrn)
                    print("Password of", U_s_pawd_usrn, ":", U_s_pawd)
                    print("Date of created:", U_s_d)
                    print("_____________________________________________________________________________________________________________")

                except:
                    print("ERROR!")
            elif s_URL == "not_valid":
                try:
                    self.cursor.execute("""
                    SELECT * FROM passwords 
                    WHERE username = '{}'
                    """.format(s_usern))

                    result = self.cursor.fetchone()

                    s_id = result[0]
                    s_pwd_name = result[1]
                    s_pawd_usrn = result[2]
                    s_pawd = result[3]
                    s_d = result[4]

                    print("                                  ")
                    print("___", s_id, "___")
                    print("                 ")
                    print("Account Name or site URL:", s_pwd_name)
                    print("Username of", s_pwd_name, ":", s_pawd_usrn)
                    print("Password of", s_pawd_usrn, ":", s_pawd)
                    print("Date of created:", s_d)
                    print("_____________________________________________________________________________________________________________")


                except:
                    print("ERROR!")


            self.connection.commit()
            self.connection.close()

    print("""
        [01]Show all saved passwords.
        [02]Add new password.
        [03]Search password.
        
        [00] Exit.
    """)

    input_no = input("Enter No:")

    p_show = main()

    if input_no == "01" or input_no == "1":
        p_show.showpasswords()

    elif input_no == "02" or input_no == "2":
        URL = input("[##]Enter name of website or name of account:")
        usern = input("[##]Enter username of that account:")
        befor_pawd = getpass.getpass(prompt='[##]Enter password:')
        re_pawd = getpass.getpass(prompt='[##]Verify you entered password:')

        if befor_pawd == re_pawd:
            p_show.AddNew(URL, usern,  re_pawd, __now)
        else:
            time.sleep(5)
            print("Two passwords dosen't match, Try again....")

    elif input_no == "03" or input_no == "3":
        serach_usern = input("Enter Username (press ENTER to skip):")

        if len(serach_usern) == 0:
            serach_URL = input("Enter URL or name of account:")
            serach_usern = "not_valid"
            p_show.Searchpassword(serach_usern, serach_URL)
        else:
            serach_URL = "not_valid"
            p_show.Searchpassword(serach_usern, serach_URL)

    elif input_no == "00" or input_no == "0":
        print("Good Bye")

    else:
        print("wrong input, Try Again...")
        mainactivity()


#end mainactivity

input_password = getpass.getpass(prompt='[@@]Enter your Password (press ENTER to skip):')

#get password

if len(input_password) == 0:
    usr_type = input("[00]Are you new user (y/n):")
    if usr_type == "y" or usr_type == "Y":

        pwd = getpass.getpass(prompt='Enter Password:')
        re_pwd = getpass.getpass(prompt='Verify you entered Password:')

        if pwd == re_pwd:
            connection = sqlite3.connect('passwords.db')
            cursor = connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS db_password (
                ID INTEGER PRIMARY KEY,
                password VARCHAR,
                date_of_created DATE
            )
            """)

            connection.commit()

            _ID = 1
            __now = datetime.datetime.now()

            cursor.execute("""
            INSERT INTO db_password VALUES
            ({}, '{}', '{}')
            """.format(_ID, re_pwd, __now))

            connection.commit()
            connection.close()

            log_p = getpass.getpass(prompt='[@@]Enter your Password:')

            i = 5
            while log_p != re_pwd:
                time.sleep(i)
                log_p = getpass.getpass(prompt='[@@]Try Again:')
                i += 2

            mainactivity()

    elif usr_type == "n" or usr_type == "n":
            os.system("python main.py")
    else:
            print("Wrong input........#")

elif len(input_password) != 0:
    try:
        db = db_pwd(1)
        y = db.load_passwords(1)
    except:
        print("Your new user or your database was lost please try again as new user..")

    i = 1
    while  y != input_password:
        input_password = getpass.getpass(prompt='[@@]Try Again:')
        time.sleep(i)
        i += 2

    if y == input_password:
        mainactivity()
    else:
        print("Wrong password, Try again...")
        os.system("python main.py")
else:
    print("Wrong password or something went wrong")
    os.system("python main.py")