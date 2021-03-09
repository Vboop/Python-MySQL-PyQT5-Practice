  
import sys , re , os
import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

USERS = []
EMAILS = []

###################################################################################################################

# Login 

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        attempt = f"{email} {password}"
        self.checkusers()
        if attempt in USERS:
            print("Successfull Login")
            USERS.clear()
            self.gotodashboard()
        else:
            USERS.clear()
            self.reset()
    
    def reset(self):
        login = Login()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(login)
  
    def checkusers(self):
        db.getConnection() 
        db.cursor.execute("SELECT * FROM Users")
        for x in db.cursor:
            e = str(x).split('\'')[1]
            p = str(x).split('\'')[3]
            user = f"{e} {p}"
            USERS.append(user)
        db.closeConnection()

    def gotodashboard(self):
        dashboard = Menu()
        widget.addWidget(dashboard)
        widget.setFixedWidth(960)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

###################################################################################################################

# Create Account

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)


    def createaccfunction(self):
        email = self.email.text()
        password = self.password.text()
        if self.password.text() == self.confirmpass.text():
            self.checkemails()
            if email in EMAILS:
                print("User Already Exists")
                EMAILS.clear()
                self.reset()
            else:
                EMAILS.clear()
                print("User Has Been Created")
                db.uLog(email , password)
                self.gotologin()

    def reset(self):
        createacc = CreateAcc()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(createacc)                
            
    def checkemails(self):
        db.getConnection() 
        db.cursor.execute("SELECT * FROM Users")
        for x in db.cursor:
            e = str(x).split('\'')[1]
            EMAILS.append(e)
        db.closeConnection()

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def deleteuser(self):
        pass

###################################################################################################################

# Menu

class Menu(QDialog):
    def __init__(self):
        super(Menu,self).__init__()
        loadUi("dashboard.ui",self)
        self.transbutton.clicked.connect(self.gototrans)
        self.notesbutton.clicked.connect(self.gotonotes)
        self.logoutbutton.clicked.connect(self.gotologin)

    
    def gototrans(self):
        transactions = Transactions()
        widget.addWidget(transactions)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotonotes(self):
        notes = Notes()
        widget.addWidget(notes)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotologin(self):
        print("Logging out")
        login = Login()
        widget.addWidget(login)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

###################################################################################################################

# Transactions

class Transactions(QDialog):
    def __init__(self):
        super(Transactions,self).__init__()
        loadUi("transactions.ui",self)
        self.menubutton.clicked.connect(self.gotodashboard)
        self.logbutton.clicked.connect(self.addTransactionLog)
        self.checklogsbutton.clicked.connect(self.gototransactionsview)

        
    def gotodashboard(self):
        dashboard = Menu()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def reset(self):
        transactions = Transactions()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(transactions) 

    def addTransactionLog(self):
        date = self.datefield.text()
        balance = self.balancefield.text()
        received = self.receivedfield.text()
        isValid = re.match('^[0123]\d/[01][012]/[2][0][2][1]$' , date)
        if len(balance) > 0 or len(received) > 0:
            if not isValid:
                self.reset()
            try:
                prevBal = db.getPreviousBal()
                balance = float(self.balancefield.text())
                received = float(self.receivedfield.text())
                spent = float(round((prevBal + received) - balance , 2))
                db.tLog(date , received , spent , balance)
                self.gototransactionsview()
            except:
                print("Somethin Aint Right O.o")
                self.reset()
        print("Empty Fields")
        self.reset()
        

    def gototransactionsview(self):
        transactionsview = TransactionsView()
        widget.addWidget(transactionsview)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def deletetransactions(self):
        pass

###################################################################################################################

# Transactions Amend

class TransactionsView(QDialog):
    def __init__(self):
        super(TransactionsView,self).__init__()
        loadUi("transactionsview.ui",self)
        self.transactionsBtn.clicked.connect(self.gototransactions)
        self.deleteBtn.clicked.connect(self.deletetransactions)
        self.transactionsViewBtn.clicked.connect(self.viewtransactions)


    def gototransactions(self):
        transactions = Transactions()
        widget.addWidget(transactions)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def viewtransactions(self):
        db.showTransactionTableValues()

    def deletetransactions(self):
        print("Ill figure it out later -_-")

###################################################################################################################

# Notes 

class Notes(QDialog):
    def __init__(self):
        super(Notes,self).__init__()
        loadUi("notes.ui",self)
        self.menuBtn.clicked.connect(self.gotodashboard)
        self.notesViewBtn.clicked.connect(self.gotonotesview)
        self.notesSaveBtn.clicked.connect(self.saveNote)


    def gotodashboard(self):
        dashboard = Menu()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotonotesview(self):
        notesview = NotesView()
        widget.addWidget(notesview)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def reset(self):
        notes = Notes()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(notes) 

    def saveNote(self):
        title = str(self.notesTitle.text())
        notes = str(self.notesText.toPlainText())
        if len(title) > 0 and len(notes) > 0:
            try:
                db.nLog(title , notes)
                self.gotonotesview()
            except:
                print("Somethin Aint Right O.o")
                self.reset()
        if len(title) == 0 and len(notes) == 0:
            print("Nothing to Save!")
        elif len(title) == 0:
            print("Title Field is Empty!")
        elif len(notes) == 0:
            print("Notes Field is Empty!")
        else:
            print("Log Successful!")

###################################################################################################################

# Notes Amend

class NotesView(QDialog):
    def __init__(self):
        super(NotesView,self).__init__()
        loadUi("notesview.ui",self)
        self.notesBtn.clicked.connect(self.gotonotes)
        self.deleteBtn.clicked.connect(self.deletenotes)
        self.notesViewBtn.clicked.connect(self.viewnotes)


    def gotonotes(self):
        notes = Notes()
        widget.addWidget(notes)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def viewnotes(self):
        db.showNotesTableValues()

    def deletenotes(self):
        print("Ill figure it out later -_-")

###################################################################################################################

# Database 

class Database():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = os.environ.get('dbPassword')
        self.dataBase = 'sqlDatabase'
        self.cursor = None
        self.connection = None

##########################################

# Database Connections 

    def getConnection(self):
        self.connection = mysql.connector.connect(
        host = self.host,
        user = self.user,
        password =f"{self.password}",
        database= self.dataBase
		)
        self.cursor = self.connection.cursor()


    def closeConnection(self):
        self.connection.close()

##########################################

# Adding and Deleting Fields  

    def addTransactionsTable(self):
        self.getConnection()
        self.cursor.execute("CREATE TABLE Transactions (LOGDATE VARCHAR(10) , REC DECIMAL(10,2) , SPENT DECIMAL(10,2) , BAL DECIMAL(10,2) , LOGID INT PRIMARY KEY AUTO_INCREMENT)")
        self.closeConnection()


    def addNotesTable(self):
        self.getConnection()
        self.cursor.execute("CREATE TABLE Notes ( TITLE VARCHAR(30) NOT NULL , NOTES VARCHAR(8000) NOT NULL , LOGID INT PRIMARY KEY AUTO_INCREMENT)")
        self.closeConnection()


    def addUsersTable(self):
        pass

##########################################

# Adding and Deleting Values

    def uLog(self , email , password):
        self.getConnection()
        self.cursor.execute("INSERT INTO Users (EMAIL , PWORD) VALUES (%s , %s)" , (email , password))
        self.connection.commit()
        print(f"\nUser Created : {email} , {password}\n")
        self.closeConnection()


    def tLog(self , date , rec , spent , bal):
        self.getConnection()
        self.cursor.execute("INSERT INTO Transactions (LOGDATE , REC , SPENT , BAL) VALUES (%s , %s , %s , %s)" , (date , rec , spent , bal))
        self.connection.commit()
        print(f"\nLogged {date} , {rec} , {spent} , {bal}\n")
        self.closeConnection()
    

    def nLog(self , title , notes):
        self.getConnection()
        self.cursor.execute("INSERT INTO Notes (TITLE , NOTES) VALUES (%s , %s)" , (title , notes))
        print("Note Added!")
        self.connection.commit()
        self.closeConnection()


    def uDel(self):
        pass

    def tDel(self):
        pass

    def nDel(self):
        pass

##########################################

# Viewing Fields

    def showDatabases(self):
        self.getConnection()
        self.cursor.execute('SHOW DATABASES')
        dbs = self.cursor.fetchall()
        print(dbs)
        self.closeConnection()


    def showTransactionTableFields(self):
        self.getConnection()
        self.cursor.execute("DESCRIBE Transactions")
        for x in self.cursor:
            print(x)
        self.closeConnection()


    def showNotesTableFields(self):
        self.getConnection()
        self.cursor.execute("DESCRIBE Notes")
        for x in self.cursor:
            print(x)
        self.closeConnection()


    def showUserTableFields(self):
        self.getConnection()
        self.cursor.execute("DESCRIBE Users")
        for x in self.cursor:
            print(x)
        self.closeConnection()

##########################################

# Viewing Values

    def showTransactionTableValues(self):
        self.getConnection()
        self.cursor.execute("SELECT * FROM Transactions")
        for x in self.cursor:
            d = str(x).split('\'')[1]
            r = str(x).split('\'')[3]
            s = str(x).split('\'')[5]
            b = str(x).split('\'')[7]
            print(f"Date : {d} | Reveived : {r} | Spent : {s} | Balance : {b}")
        self.closeConnection()


    def showUserTableValues(self):
        self.getConnection()
        self.cursor.execute("SELECT * FROM Users")
        for x in self.cursor:
            e = str(x).split('\'')[1]
            p = str(x).split('\'')[3]
            print(f"Email : {e} | Password : {p}")
        self.closeConnection()


    def showNotesTableValues(self):
        self.getConnection()
        self.cursor.execute("SELECT * FROM Notes")
        for x in self.cursor:
            t = str(x).split('\'')[1]
            n = str(x).split('\'')[3]
            i = str(x).split('\'')[4].split(',')[1].strip().split(')')[0]
            print(f"Title : {t} | Text : {n} | ID : {i}")
        self.closeConnection()


    def getPreviousBal(self):
        self.getConnection()
        self.cursor.execute("SELECT BAL FROM Transactions ORDER BY LOGID DESC LIMIT 1")
        for x in self.cursor:
            x = float(str(x).split('\'')[1])
            return x
        self.closeConnection()


    def getEmails(self):
        self.getConnection()
        self.cursor.execute("SELECT EMAIL FROM Users")
        for x in self.cursor:
            print(x)
            USERS.append(str(x))
        self.closeConnection()


    def getUsers(self):
        self.getConnection()
        self.cursor.execute("SELECT EMAIL,PWORD FROM Users")
        for x in self.cursor:
            USERS.append(str(x))
        self.closeConnection()




db = Database()
app = QApplication(sys.argv)
login = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()