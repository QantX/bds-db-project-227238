# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
import sys
import LoginWindow
import DB
import MainWindow
import bcrypt
import logging
from logging.handlers import TimedRotatingFileHandler


class DbApp(QtWidgets.QMainWindow, MainWindow.Ui_Dialog):

    def __init__(self, parent=None):
        super(DbApp, self).__init__(parent)
        self.setupUi(self)
        self.create_Button.clicked.connect(self.createData)
        self.read_Button.clicked.connect(self.readData)
        self.update_Button.clicked.connect(self.updateData)
        self.tableWidget_2.cellClicked.connect(self.CRUDtableClicked)
        self.delete_Button.clicked.connect(self.deleteData)
        self.filter_Button.clicked.connect(self.filterData)
        self.comboBox.currentIndexChanged.connect(self.filterChanged)
        self.execute_Button_1.clicked.connect(self.multipleQuery)
        self.execute_Button_2.clicked.connect(self.runSqlInjection)
        self.recreate_Button.clicked.connect(self.recreateDummy)
        self.refresh_Button.clicked.connect(self.refreshTable)
        self.execute_Button_3.clicked.connect(self.runSqlInjection2)
        self.tabWidget.currentChanged.connect(self.switchedTab)
        self.Db = DB.DBAccess()
        self.readData()


    def createData(self):
        self.info_label_1.setText("")
        if self.textEdit.toPlainText() == '' or self.textEdit_2.toPlainText() == '' or self.textEdit_3.toPlainText() == '' or self.textEdit_4.toPlainText() == '' or self.textEdit_5.toPlainText() == '' or self.textEdit_6.toPlainText() == '' or not self.textEdit_2.toPlainText().isdigit() or not self.textEdit_3.toPlainText().isdigit() or not self.textEdit_4.toPlainText().isdigit():
            self.info_label_1.setText("Missing or incorrect values!")
            return

        create = self.Db.InsertData("INSERT INTO mydb.product (id_product, name, price, discount, in_stock, gender, season) VALUES (DEFAULT,'" + self.textEdit.toPlainText() + "'," + self.textEdit_2.toPlainText() + "," + self.textEdit_3.toPlainText() + "," + self.textEdit_4.toPlainText() + ",'" + self.textEdit_5.toPlainText() + "','" + self.textEdit_6.toPlainText() + "')")
        self.info_label_1.setText("Successfuly created " + str(create) + " rows")


    def readData(self):
        self.tableWidget_2.verticalHeader().hide()


        read = self.Db.QueryData("SELECT * FROM mydb.product")
        self.tableWidget_2.setRowCount(len(read))
        self.tableWidget_2.setColumnCount(len(read[0]))
        for row in range(len(read)):
            for column in range(len(read[row])):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(read[row][column])))
        self.info_label_1.setText("Successfuly loaded " + str(len(read)) + " rows from table mydb.Product")
        self.tableWidget_2.setHorizontalHeaderLabels(['id_product', 'name', 'price', 'discount', 'in_stock', 'gender', 'season'])

    def CRUDtableClicked(self):
        row = self.tableWidget_2.selectedItems()[0].row()
        self.textEdit_7.setText(self.tableWidget_2.item(row,0).text())
        self.textEdit.setText(self.tableWidget_2.item(row, 1).text())
        self.textEdit_2.setText(self.tableWidget_2.item(row, 2).text())
        self.textEdit_3.setText(self.tableWidget_2.item(row, 3).text())
        self.textEdit_4.setText(self.tableWidget_2.item(row, 4).text())
        self.textEdit_5.setText(self.tableWidget_2.item(row, 5).text())
        self.textEdit_6.setText(self.tableWidget_2.item(row, 6).text())


    def updateData(self):
        print(self.textEdit_2.toPlainText())
        self.info_label_1.setText("")
        if self.textEdit_7.toPlainText() == '' or self.textEdit.toPlainText() == '' or self.textEdit_2.toPlainText() == '' or self.textEdit_3.toPlainText() == '' or self.textEdit_4.toPlainText() == '' or self.textEdit_5.toPlainText() == '' or self.textEdit_6.toPlainText() == '' or not self.textEdit_2.toPlainText().isdigit() or not self.textEdit_3.toPlainText().replace(".", "").isdigit() or not self.textEdit_4.toPlainText().isdigit() or not self.textEdit_7.toPlainText().isdigit():
            self.info_label_1.setText("Missing or incorrect values!")
            return
        update = self.Db.InsertData("UPDATE mydb.product SET name = '" + self.textEdit.toPlainText() + "', price = " + self.textEdit_2.toPlainText() + ", discount = " + self.textEdit_3.toPlainText() + ", in_stock = " + self.textEdit_4.toPlainText() + ", gender = '" + self.textEdit_5.toPlainText() + "', season = '" + self.textEdit_6.toPlainText() + "' WHERE id_product =" + self.textEdit_7.toPlainText() + ";")
        self.info_label_1.setText("Successfuly updated " + str(update) + " rows from table mydb.Product")
        self.readData()

    def switchedTab(self):
        print(self.tabWidget.currentIndex())
        match self.tabWidget.currentIndex():
            case 0:
               self.readData()
            case 1:
                self.detailedView()
            case 2:
                return
            case 3:
                self.filterSetup()
            case 4:
                self.refreshTable()
            case _:
                return

    def deleteData(self):
        self.info_label_1.setText("")
        if self.textEdit_7.toPlainText() == '' or not self.textEdit_7.toPlainText().isdigit():
            self.info_label_1.setText("Missing or incorrect ID!")
        delete = self.Db.InsertData("DELETE from mydb.product WHERE id_product = " + self.textEdit_7.toPlainText() + ";")
        self.info_label_1.setText("Successfuly deleted " + str(delete) + " rows from table mydb.Product")
        self.readData()

    def detailedView(self):
        self.tableWidget.verticalHeader().hide()
        tablecolumns = []
        columns = self.Db.QueryData(
            "SELECT column_name from information_schema.columns WHERE table_schema = 'mydb' AND table_name = 'user';")
        tablecolumns = list(columns)
        columns = self.Db.QueryData(
            "SELECT column_name from information_schema.columns WHERE table_schema = 'mydb' AND table_name = 'order';")
        tablecolumns += list(columns)
        columns = self.Db.QueryData(
            "SELECT column_name from information_schema.columns WHERE table_schema = 'mydb' AND table_name = 'membership';")
        tablecolumns += list(columns)
        columns = self.Db.QueryData(
            "SELECT column_name from information_schema.columns WHERE table_schema = 'mydb' AND table_name = 'address';")
        tablecolumns += list(columns)
        self.tableWidget.setHorizontalHeaderLabels(list(map(''.join, tablecolumns)))

        detView = self.Db.QueryData('''SELECT * FROM mydb.user as usr
        inner join mydb.order as ord on usr.id_user = ord.id_user
        inner join mydb.membership as mbs on usr.id_membership = mbs.id_membership
        inner join mydb.address as ads on usr.id_user = ads.id_address;''')
        self.tableWidget.setRowCount(len(detView))
        self.tableWidget.setColumnCount(len(detView[0]))
        for row in range(len(detView)):
            for column in range(len(detView[row])):
                self.tableWidget.setItem(row,column,QTableWidgetItem(str(detView[row][column])))

    def filterChanged(self):
        self.comboBox_2.clear()
        columns = self.Db.QueryData("SELECT column_name from information_schema.columns WHERE table_schema = 'mydb' AND table_name = '" + self.comboBox.currentText() + "';")
        for column in list(columns):
            self.comboBox_2.addItem(column[0])
        print(columns)


    def filterSetup(self):
        self.tableWidget_4.verticalHeader().hide()
        self.comboBox.clear()
        self.comboBox_2.clear()
        tables =  self.Db.QueryData("SELECT table_name from information_schema.tables WHERE table_schema = 'mydb'")
        for table in list(tables):
            self.comboBox.addItem(table[0])
        self.filterChanged()

    def filterData(self):

        self.tableWidget_4.clear()
        if self.textEdit_8.toPlainText().isdigit():
            filter = self.Db.QueryData("SELECT * FROM mydb." + self.comboBox.currentText() + " WHERE " + self.comboBox_2.currentText() + " = " + self.textEdit_8.toPlainText() + ";")
        elif self.textEdit_8.toPlainText() == '':
            filter = self.Db.QueryData("SELECT * FROM mydb." + self.comboBox.currentText() + ";")
        else:
            filter = self.Db.QueryData("SELECT * FROM mydb." + self.comboBox.currentText() + " WHERE " + self.comboBox_2.currentText() + " = '" + self.textEdit_8.toPlainText() + "';")
        if len(filter) == 0:
            self.tableWidget_4.clear()
            return

        self.tableWidget_4.setHorizontalHeaderLabels([self.comboBox_2.itemText(i) for i in range(self.comboBox_2.count())])
        self.tableWidget_4.setRowCount(len(filter))
        self.tableWidget_4.setColumnCount(len(filter[0]))
        for row in range(len(filter)):
            for column in range(len(filter[row])):
                self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(filter[row][column])))

    def multipleQuery(self):
        transaction = []
        if self._checkBox.isChecked():
            transaction.append("UPDATE mydb.product SET name = 'NITEBALL' WHERE id_product = 2")

        if self._checkBox_2.isChecked():
            transaction.append("INSERT INTO mydb.product (id_product, name, price, discount, in_stock, gender, season) VALUES (DEFAULT, 'test', 'badvalue', 20, 10, 'test', 'test');")

        if self._checkBox_3.isChecked():
            transaction.append("DELETE FROM mydb.product WHERE price > 550 ")

        multiQ = self.Db.QueryTransaction(transaction)
        if multiQ == None:
            self.label_3.setText("Transaction Failed, all changes rolled back")
        else:
            self.label_3.setText("Transaction completed succesfully")
        print(multiQ)


    def runSqlInjection2(self):
        self.label_2.setText("SQL INJECTION SIMULATION")
        if self.textEdit_10.toPlainText() == '':
            return
        if len(self.Db.QueryData("SELECT * from information_schema.tables WHERE table_schema = 'mydb' and table_name = 'users'")) == 0:
            self.label_2.setText("Table mydb.users does not exist")
            return
        self.tableWidget_5.verticalHeader().hide()
        injection = self.Db.QueryData("SELECT * from mydb.users WHERE item_e = " + self.textEdit_10.toPlainText() + ";" )
        print(injection)
        self.tableWidget_5.setRowCount(len(injection))
        self.tableWidget_5.setColumnCount(len(injection[0]))
        for row in range(len(injection)):
            for column in range(len(injection[row])):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(injection[row][column])))
        self.tableWidget_5.setHorizontalHeaderLabels(['column_1', 'column_2', 'column_3', 'column_4', 'column_5'])

    def runSqlInjection(self):
        self.label_2.setText("SQL INJECTION SIMULATION")
        if self.textEdit_9.toPlainText() == '':
            return
        if len(self.Db.QueryData(
                "SELECT * from information_schema.tables WHERE table_schema = 'mydb' and table_name = 'users'")) == 0:
            self.label_2.setText("Table mydb.users does not exist")
            return
        execute = self.Db.InsertData("INSERT INTO mydb.users VALUES ('test', 'test', 'test', 'test'," + self.textEdit_9.toPlainText() + ")")
        print(execute)


    def refreshTable(self):
        self.label_2.setText("SQL INJECTION SIMULATION")
        if len(self.Db.QueryData("SELECT * from information_schema.tables WHERE table_schema = 'mydb' and table_name = 'users'")) == 0:
            self.label_2.setText("Table mydb.users does not exist")
            return
        self.tableWidget_5.verticalHeader().hide()
        refresh = self.Db.QueryData("SELECT * from mydb.users")
        print(refresh)
        self.tableWidget_5.setRowCount(len(refresh))
        self.tableWidget_5.setColumnCount(len(refresh[0]))
        for row in range(len(refresh)):
            for column in range(len(refresh[row])):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(refresh[row][column])))
        self.tableWidget_5.setHorizontalHeaderLabels(['column_1', 'column_2', 'column_3', 'column_4', 'column_5'])

    def recreateDummy(self):
        self.label_2.setText("SQL INJECTION SIMULATION")
        create = self.Db.InsertData("""CREATE TABLE IF NOT EXISTS mydb.users
    (
    item_a character varying(20) COLLATE pg_catalog."default" NOT NULL,
    item_b character varying(30) COLLATE pg_catalog."default" NOT NULL,
    item_c character varying(15) COLLATE pg_catalog."default" NOT NULL,
    item_d character varying(20) COLLATE pg_catalog."default" NOT NULL,
    item_e integer NOT NULL);
    INSERT INTO mydb.users VALUES 
    ('test', 'test', 'test', 'test', 20), 
    ('test', 'test', 'test', 'test', 30),
    ('test', 'test', 'test', 'test', 15),
    ('test', 'test', 'test', 'test', 1)""")
        print(create)


    def show_state(self, value):
        cb = self.sender()
        if cb.isChecked():
            state = cb.text()


class DbLogin(QtWidgets.QMainWindow, LoginWindow.Ui_Dialog):

    def __init__(self, parent=None):
        super(DbLogin, self).__init__(parent)
        self.setupUi(self)


def loginClicked(lF,aF,Db):

    lF.login_error_Label.setText("")
    if lF.lineEdit.text() == '' or lF.LoginInput.toPlainText() == '':
        lF.login_error_Label.setText("Login and Password must be filled")
        return


    pwd = lF.lineEdit.text()
    hashedResult = Db.QueryData("SELECT password FROM mydb.user WHERE login = '"+ lF.LoginInput.toPlainText() + "'")

    print(hashedResult)
    if len(hashedResult) == 0:
        lF.login_error_Label.setText("Incorrect Login or Password")
        return
    if bcrypt.checkpw(bytes(pwd,'UTF-8'), bytes(hashedResult[0][0],'UTF-8')):
        Db.CloseConnection()
        lF.hide()
        aF.show()
    else:
        lF.login_error_Label.setText("Incorrect Login or Password")

def main():
    logger = logging.getLogger('dbApplication')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logname = "dbApplication.log"
    handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
    handler.suffix = "%Y-%m-%d"
    logger.addHandler(handler)
    Db = DB.DBAccess()
    app = QApplication(sys.argv)
    loginForm = DbLogin()
    appForm = DbApp()
    loginForm.login_Button.clicked.connect(lambda: loginClicked(loginForm,appForm,Db))
    loginForm.show()
    app.exec_()

if __name__ == '__main__':
    main()