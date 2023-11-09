from PyQt5 import QtCore, QtGui, QtWidgets
from widget2 import Ui_Form
import funcs
from pass_val import passval

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.nhash=funcs.D7numhash
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 755)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(20, 550, 421, 151))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.loginButton.setFont(font)
        self.loginButton.setObjectName("loginButton")
        self.signupButton = QtWidgets.QPushButton(self.centralwidget)
        self.signupButton.setGeometry(QtCore.QRect(460, 550, 421, 151))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.signupButton.setFont(font)
        self.signupButton.setObjectName("signupButton")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(10, 0, 880, 100))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label1.setFont(font)
        self.label1.setAutoFillBackground(False)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label1")
        self.Box = QtWidgets.QGroupBox(self.centralwidget)
        self.Box.setGeometry(QtCore.QRect(25, 200, 850, 330))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Box.setFont(font)
        self.Box.setTitle("")
        self.Box.setFlat(False)
        self.Box.setObjectName("Box")
        self.userLine = QtWidgets.QLineEdit(self.Box)
        self.userLine.setGeometry(QtCore.QRect(270, 40, 550, 70))
        self.userLine.setMaxLength(35)
        self.userLine.setFrame(True)
        self.userLine.setClearButtonEnabled(True)
        self.userLine.setObjectName("userLine")
        self.passLine = QtWidgets.QLineEdit(self.Box)
        self.passLine.setGeometry(QtCore.QRect(270, 180, 550, 70))
        self.passLine.setMaxLength(35)
        self.passLine.setObjectName("passsLine")
        self.passLine.setClearButtonEnabled(True)
        self.label3 = QtWidgets.QLabel(self.Box)
        self.label3.setGeometry(QtCore.QRect(30, 40, 220, 70))
        self.label3.setObjectName("label3")
        self.label4 = QtWidgets.QLabel(self.Box)
        self.label4.setGeometry(QtCore.QRect(30, 180, 220, 70))
        self.label4.setObjectName("label4")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(175, 100, 550, 60))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label2.setFont(font)
        self.label2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label2.setObjectName("label2")
        self.label2.setStyleSheet(u"font-size: 18pt;\n""border: solid;\n""border-color:black;\n""border-width: 1px;")
        MainWindow.setCentralWidget(self.centralwidget)
        self.lcdNumber = QtWidgets.QLCDNumber(self.Box)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QtCore.QRect(505, 260, 315, 55))
        self.lcdNumber.setDigitCount(9)

        self.loginButton.clicked.connect(self.login)
        self.signupButton.clicked.connect(self.signup)
        self.passLine.textChanged.connect(self.update_val)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        print("[Initialized app]\n")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Password saver by osh"))
        self.loginButton.setText(_translate("MainWindow", "Login"))
        self.signupButton.setText(_translate("MainWindow", "Sign Up"))
        self.label1.setText(_translate("MainWindow", "Welcome to your password saver!"))
        self.userLine.setPlaceholderText(_translate("MainWindow", "ex: Bob2005"))
        self.passLine.setPlaceholderText(_translate("MainWindow", "ex: password123"))
        self.label3.setText(_translate("MainWindow", "Username:"))
        self.label4.setText(_translate("MainWindow", "Password:"))
        self.label2.setText(_translate("MainWindow", "Please enter your account or sign up"))

    def openwindow(self, acc, passw):
        self.window=QtWidgets.QMainWindow()
        self.ui=Ui_Form()
        print('\n[Initializing window...]')
        self.ui.setupUi(self.window, acc, passw, self.nhash)
        MainWindow.hide()
        self.window.show()
    def login(self):
        user=str(self.userLine.text())
        passw=str(self.passLine.text())
        if len(user)>0 and len(passw)>0:
            self.userLine.setPlaceholderText("")
            self.passLine.setPlaceholderText("")
            self.userLine.setText("")
            self.passLine.setText("")
            passx=funcs.check_read(user)
            print(f"Login attempt from user:[{user}]\n\t({self.nhash(passw, 'seed.env')})  ({passx})")
            if passx == None:
                self.label2.setText("Account not found")
                print("Login failed")
            else:
                passw+=funcs.check_read(user).split("|")[1]
                if passx.split("|")[0] == str(self.nhash(passw, 'seed.env')):
                    self.openwindow(user, passw)
                else:
                    self.label2.setText("Wrong password")
                    print("Login failed--password error")
    def signup(self):
        user=str(self.userLine.text())
        passw=str(self.passLine.text())
        if len(user)>0 and len(passw)>0:
            if funcs.check_read(user)==None:
                self.userLine.setPlaceholderText("")
                self.passLine.setPlaceholderText("")
                self.userLine.setText("")
                self.passLine.setText("")
                salt=funcs.get_salt()
                passw+=salt
                hashed_passw=str(self.nhash(passw, 'seed.env'))+"|"+salt
                print(f"Sign-up attempt from user:[{user}]\n\t({passw}))  ({hashed_passw})")
                funcs.write(user, hashed_passw)
                self.openwindow(user, passw)
            else:
                self.label2.setText("Username already taken")
                print(f"Sign-up Failed")
    def update_val(self):
        text = passval(str(self.passLine.text()))
        self.lcdNumber.display(text)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
