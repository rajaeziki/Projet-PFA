import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication,QWidget
from PyQt5.uic import loadUi
import sqlite3
from PyQt5 import QtWidgets


class Login(QDialog):
    def __int__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.creataccbutton.clicked.connect(self.gotocreate)
    # here tp out the password like point
        self.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
    def loginfunction(self):
        email = self.email_2.text()
        password = self.password_2.text()

        if len(email)==0 or len(password)==0:
            self.error.setText("please input all fields .")

        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE email =\''+email+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            if result_pass == password:
                print("Successfully logged in.")
                self.error.setText("")

            else :
                self.error.setText("invalid email or password")
    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.setCurrentIndex()+1)


    # if i want to use anather page
       # login = Login()
      #  widget.addWidget(login)
       # widget.setCurrentIndex(widget.currentIndex()+1)


class CreateAcc(QDialog):
    def __int__(self):
        super(CreateAcc, self).__init__()
        loadUi("creatacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
    def createaccfunction(self):
        email = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            print("Succesfully created acc with email:" emaail,"andpassword:",password)
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget
widget .addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)

widget.show()
app.exec_()







