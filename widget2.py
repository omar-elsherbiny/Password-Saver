from PyQt5 import QtCore, QtGui, QtWidgets
import funcs

class Ui_Form(object):
    def setupUi(self, Form, acc, passw, passw_func):
        self.nhash=passw_func
        self.account=acc
        Form.setObjectName("Form")
        Form.resize(900, 800)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(25, 30, 850, 80))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaxLength(55)
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setGeometry(QtCore.QRect(25, 120, 280, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.deleteButton = QtWidgets.QPushButton(Form)
        self.deleteButton.setGeometry(QtCore.QRect(308, 120, 280, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName("deleteButton")
        self.clearButton = QtWidgets.QPushButton(Form)
        self.clearButton.setGeometry(QtCore.QRect(591, 120, 281, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.clearButton.setFont(font)
        self.clearButton.setObjectName("clearButton")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(25, 180, 850, 600))
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(70)
        self.tableWidget.setFont(font2)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(264)

        self.data=[]
        if funcs.check_read(self.account).split("|")[0] == str(self.nhash(passw, 'seed.env')):
            self.data=funcs.read(self.account, 'seed.env')
            self.tableWidget.setRowCount(len(self.data))
            for row in range(len(self.data)):
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(self.data[row]['name']))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(self.data[row][' password']))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(self.data[row][' username']))
            self.addButton.clicked.connect(self.add)
            self.deleteButton.clicked.connect(self.delete)
            self.clearButton.clicked.connect(self.show_popup)
            val=0
        else:
            self.lineEdit.setText("No Account")
            val=1

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        print(f"[Done with val={val}]\n")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", f"Password saver by osh -- {self.account}"))
        self.addButton.setText(_translate("Form", "Add"))
        self.deleteButton.setText(_translate("Form", "Delete"))
        self.clearButton.setText(_translate("Form", "Clear"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Password"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Username"))

    def add(self):
        text=str(self.lineEdit.text())
        splited=text.split(',')
        if len(splited)>=3 and len(text)>=3:
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            row=self.tableWidget.rowCount()-1
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(splited[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(splited[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(splited[2]))
            self.lineEdit.setText("")
            print(f"Added line in row={row}, with data={splited}")
            self.data.append({'name':splited[0], ' password':splited[1], ' username':splited[2]})
            funcs.update_write(self.account, self.data, 'seed.env')
    def delete(self):
        crow=self.tableWidget.currentRow()
        self.tableWidget.removeRow(crow)
        if len(self.data)>0:
            self.data.pop(crow)
        print(f"Deleted line in row={crow}")
        funcs.update_write(self.account, self.data, 'seed.env')

    def clear(self, i):
        if str(i.text()) == '&Yes':
            self.tableWidget.clearContents()
            self.data=[]
            funcs.update_write(self.account, None, 'seed.env')
            print(f"Cleared data")

    def show_popup(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Warning!")
        msg.setText("This will delete all data in your database.")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes |
                               QtWidgets.QMessageBox.Cancel)
        msg.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        msg.setInformativeText("Are you sure you want to continue?")

        msg.buttonClicked.connect(self.clear)
        print("[Initialized pop-up]")
        x=msg.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form, 'omar', '1', funcs.D7numhash)
    Form.show()
    sys.exit(app.exec_())
