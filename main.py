import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget
from PyQt5.uic import loadUi
import sqlite3
import hashlib

# Import the main window class from mainwindow.py
from app import MainWindow

def create_connection():
    try:
        conn = sqlite3.connect("cameras.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.creataccount.clicked.connect(self.gotocreateacc)

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreateacc(self):
        create_acc = CreateAcc()
        widget.addWidget(create_acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.creataccbutton.clicked.connect(self.gotocreate)
        self.password_1.setEchoMode(QtWidgets.QLineEdit.Password)

        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS login_info (
                                   email TEXT PRIMARY KEY,
                                   password TEXT)''')
                conn.commit()
                print("Database and table created successfully.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            finally:
                conn.close()

    def loginfunction(self):
        email = self.email_2.text()
        password = self.password_1.text()

        if len(email) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")
        else:
            conn = create_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    query = 'SELECT password FROM login_info WHERE email = ?'
                    cur.execute(query, (email,))
                    result = cur.fetchone()

                    if result and result[0] == hash_password(password):
                        self.error.setText("Successfully logged in.")
                        # Load the main window and display it
                        main_window = MainWindow()
                        widget.addWidget(main_window)
                        widget.setCurrentIndex(widget.currentIndex() + 1)
                    else:
                        self.error.setText("Invalid email or password")

                except sqlite3.Error as e:
                    self.error.setText(f"Database error: {e}")
                finally:
                    conn.close()

    def gotocreate(self):
        create_acc = CreateAcc()
        widget.addWidget(create_acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        email = self.email.text()
        password = self.password.text()
        confirmpass = self.confirmpass.text()

        if len(email) == 0 or len(password) == 0 or len(confirmpass) == 0:
            self.error.setText("Please fill in all fields.")
        elif password != confirmpass:
            self.error.setText("Passwords do not match.")
        else:
            conn = create_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    query = 'INSERT INTO login_info (email, password) VALUES (?, ?)'
                    cur.execute(query, (email, hash_password(password)))
                    conn.commit()
                    self.error.setText("Successfully created account.")
                    print("Successfully created account with email:", email)
                    login = Login()
                    widget.addWidget(login)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                except sqlite3.IntegrityError:
                    self.error.setText("Account with this email already exists.")
                except sqlite3.Error as e:
                    self.error.setText(f"Database error: {e}")
                finally:
                    conn.close()

app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedWidth(1200)
widget.setFixedHeight(800)
widget.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print("Exiting with exception:", e)
