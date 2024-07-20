# Developed By : <PRIYANSHUL SHARMA>
# My blog https://priyanshul.is-a.dev/


import mysql.connector as pymysql
import random

passwrd = None
db = None  
C = None


def base_check():
    check=0
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('Show databases')
    Result=cursor.fetchall()
    for r in Result:
        for i in r:
            if i=='bank':
                cursor.execute('Use bank')
                check=1
    if check!=1:
        create_database()

def table_check():
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('Show databases')
    Result=cursor.fetchall()
    for r in Result:
        for i in r:
            if i=='bank':
                cursor.execute('Use bank')
                cursor.execute('show tables')
                result=cursor.fetchall()
                if len(result)<=1:
                    create_tables()
                else:
                    print('      Booting systems...')
                    
                
def create_database():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS bank")
        db.commit()
        db.close()
        try:
            print("Database 'bank' created successfully.")
        except:
            print(f"Error creating database: {str(e)}")
    except pymysql.Error as e:
        print(f"Error creating database: {str(e)}")

def create_tables():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd, database="bank")
        cursor = db.cursor()

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                NAME VARCHAR(255),
                ACNO INT PRIMARY KEY,
                BBALANCE FLOAT CHECK (BBALANCE>1000.0)
            )
        """)
            
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password (
                NAME VARCHAR(255),
                ACNO INT PRIMARY KEY CHECK(ACNO>100000),
                PASSWORD VARCHAR(255) UNIQUE
            )
        """)
        db.commit()
        db.close()
        try:
            print("Tables 'accounts' and 'password' created successfully.")
        except pymysql.Error as e:
            print(f"Error creating tables: {str(e)}")
    except pymysql.Error as e:
        print(f"Error creating tables: {str(e)}")

def QR():
    Result = C.fetchall()
    for r in Result:
        print(r)

def CReg():
    N = input("Enter Name: ")
    AC = random.randint(100000,999999)
    BB = float(input("Enter Initial Bank Balance: "))
    if BB>1000:
        PP = input("Enter Account Password:")
        data = (N, AC, BB)
        adata = (N, AC, PP)
        ldata = (N, AC, 'NO', 0, 0, 0, 0)
        SQL = "INSERT INTO accounts (NAME, ACNO, BBALANCE) VALUES (%s, %s, %s)"
        SQL2 = "INSERT INTO password (NAME, ACNO, PASSWORD) VALUES (%s, %s, %s)"
        try:
            C.execute(SQL, data)
            C.execute(SQL2, adata)
            db.commit()
            print('Account successfully created...')
            print('Your Account details:',data,'Please save this information to avail future services')
        except pymysql.Error as e:
            print(f"Error generated: {str(e)}")
    else:
        print('Balance below minimum Limit...Minimum Deposit Required!')
        CReg()

def D():
    
    C.execute("SELECT * FROM accounts")
    QR()
    
def Sort():
    Sort_On = input("SORT ON[NAME,ACNO, BBALANCE]::: ")
    AOD = input("Asc: Ascending Order , Desc: Descending Order:::")
    SQL = "SELECT * FROM ACCOUNTS ORDER BY " + Sort_On + " " + AOD
    try:
        C.execute(SQL)
        QR()
    except:
        print("Wrong Column or Order")

        
def Search():
    Search_on = input("SEARCH ON[ACNO OR NAME]:::")
    if Search_on =='NAME':
        VAL = input("Search Value:")
        SQL = "SELECT * FROM ACCOUNTS WHERE " + Search_on + " = " + "'" + VAL + "'"
    elif Search_on =='ACNO':
        VAL = input("Search Value:")
        SQL = "SELECT * FROM ACCOUNTS WHERE " + Search_on + " = " + VAL
    try:
        C.execute(SQL)
        print("RECORD FOUND")
        QR()
    except:
        print("Value not found or Incorrect Search_on Value")
        
def Delete():
    
    Col = input("Column[NAME,ACNO,BBALANCE]:::")
    if Col.upper()=='NAME':
        Val = input("Value:::")
        SQL = "DELETE FROM ACCOUNTS WHERE " + Col + " " + "=" + " " + Val
        
    else:
        Sign = input("Comparison Value[>,=,<(etc.)]:::")
        Val = input("Value:::")
        SQL = "DELETE FROM ACCOUNTS WHERE " + Col + " " + Sign + " " + Val
        
    try:
        C.execute(SQL)
        D()
    except:
        print("Wrong Input Values or Record Not found")
        
def Edit():
    while True:
        Set_Col = input("SET Column[NAME,ACNO,BBALANCE]:::")
        Set_Condition = input("SET CONDITION: ")
        Where_Col = input("WHERE Column[NAME,ACNO,BBALANCE]:::")
        Where_Condition = input("Where CONDITION: ")
        SQL = "UPDATE ACCOUNTS SET " + Set_Col + Set_Condition + " WHERE " + Where_Col + " " + Where_Condition
        print(SQL)
        Con = input("Confirm(Y/N): ")
        if Con=='Y':
            C.execute(SQL)
            D()
            break
        else:
            print("Try Again")
            
def Transact():
    db = pymysql.connect(host="localhost", user="root", password=passwrd, database="bank")
    cursor = db.cursor()
    while True:
        print("Select W :withdrawing, D :depositing, X:EXIT::: ")
        a=input()
        Acno=(input('RE-ENTER YOUR ACCOUNT NO.:'))
        SQL= "select BBALANCE from accounts where Acno" + "=" + Acno
        cursor.execute(SQL)
        Result=cursor.fetchall()
        for i in Result:
            for j in i:
                money=j
        print(Result)
        if a=="W":
            N=int(input("enter the amount you want to withdraw"))
            if (money-N)>=1000.0:
                SQL = "UPDATE ACCOUNTS SET BBALANCE= BBALANCE-"+" " +str(N)+ " " + "WHERE ACNO=" + " " + Acno
                C.execute(SQL)
                print('TRANSACTION SUCCESSFULL')
                Check()
                db.commit()
                break
            else:
                print('Minimum Deposit Limit breched... \n Transaction failed')
                
        elif a=="D":
            M=int(input("enter the amount you want to deposit"))
            SQL = "UPDATE ACCOUNTS SET BBALANCE= BBALANCE+" + " " + str(M) + " " + "WHERE ACNO=" + " " + Acno
            C.execute(SQL)
            print('TRANSACTION SUCCESSFULL')
            Check()
            db.commit()
            break
        elif a=='X':
            break
        else:
            print("Wrong input, try again")
            
def Check():
    Acno=(input('ENTER YOUR ACCOUNT NO. TO CHECK YOUR BALANCE:'))
    SQL= 'SELECT BBALANCE FROM ACCOUNTS WHERE ACNO='+Acno ;
    C.execute(SQL)
    QR()


def main():
    global passwrd
    passwrd = input("Enter password for mysql: ")

    base_check()

    table_check()
    
    global db, C
    db = pymysql.connect(host="localhost", user="root", password=passwrd, database="bank")
    C = db.cursor()
    while True:
        Log = input("For Bank Employees : A, For User : U ::: ")
        if Log == "A" or Log == 'a':
            P = input("ENTER PASSWORD: ")
            if P == '12345':
                print("LOGIN SUCCESSFUL")
                while True:
                    AMenu = input('''C:Customer Registration, D:Display Accounts,S:Sort,SE:Search,DEL:Delete,X:Break :::''')
                    if AMenu.upper() == 'C':
                        CReg()
                    elif AMenu.upper() == 'D':
                        D()
                    elif AMenu.upper() =='S':
                        Sort()
                    elif AMenu.upper() =='SE':
                        Search()
                    elif AMenu.upper() =='DEL':
                        Delete()
                    elif AMenu.upper() == 'E':
                        Edit()
                    elif AMenu.upper() == 'X':
                        break
                    else:
                        print("Wrong Input")
                        main()
                    

        elif Log == "U" or Log == "u":
            Log = input("Register as a New User : R, Login: L ::: ")
            if Log in "Rr":
                CReg()
            elif Log in 'Ll':
                Acno = input("Enter Account Number:")
                P = input("Enter Password:")
                SQL = 'SELECT PASSWORD FROM password WHERE ACNO = %s'
                C.execute(SQL, (Acno,))
                S = C.fetchall()
                if S and P == S[0][0]:
                    print('LOGIN SUCCESSFUL')
                    while True:
                        Menu = input('''T: TRANSACTION, C: CHECK BANK BALANCE, X: EXIT:::''')
                        if Menu.upper() == "T":
                            Transact()
                        elif Menu.upper() =="C":
                            Check()
                        elif Menu.upper() == 'X':
                            break


if __name__ == "__main__":
    main()
    

