from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import mysql.connector

import database as database_db

from PyQt5.uic import loadUiType

ui, _ = loadUiType('laptop.ui')
login, _ = loadUiType('login.ui')


class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.handle_login)
        self.signup_pushButton.clicked.connect(self.add_new_user)

    def add_new_user(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()
        full_name = self.user_full_name_lineEdit.text()
        email = self.email_lineEdit.text()
        password = self.password_signup_lineEdit.text()
        password_confirm = self.password_confirm_signup_lineEdit.text()

        if password == password_confirm:
            cursor.execute('''
                        INSERT INTO user(fullname , email , password)
                        VALUES (%s , %s ,%s)
                    ''', (full_name, email, password))
            db.commit()
            MainApp.message_box(self, 'User Added!')

            self.user_full_name_lineEdit.setText('')
            self.email_lineEdit.setText('')
            self.password_signup_lineEdit.setText('')
            self.password_confirm_signup_lineEdit.setText('')
        else:
            self.wrong_password_label.setText('The Passwords Are Not Match!l')

    def handle_login(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        username = self.user_name_lineEdit.text()
        password = self.password_lineEdit.text()

        sql = "SELECT * FROM user"
        cursor.execute(sql)
        data = cursor.fetchall()

        for row in data:
            if username == row[1] and password == row[3]:
                MainApp.message_box(self, 'You Are In!')
                self.window_main = MainApp()
                self.close()
                self.window_main.show()
            else:
                self.sure_label.setText('Make Sure You Enter Your Username And Password Correctly')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.create_database()
        self.button_handler()
        self.ui_changes_handler()
        self.show_all_laptops()

        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

    def ui_changes_handler(self):
        self.tabWidget.tabBar().setVisible(False)

    def button_handler(self):
        self.laptop_recommedation_pushButton.clicked.connect(self.open_laptop_tab)
        self.insert_pushButton.clicked.connect(self.open_insert_tab)
        self.edit_section_pushButton.clicked.connect(self.open_edit_tab)
        self.users_pushButton.clicked.connect(self.open_user_tab)

        self.add_pushButton.clicked.connect(self.add_new_laptop)
        self.search_pushButton.clicked.connect(self.search_laptop)
        self.edit_pushButton.clicked.connect(self.edit_laptop)
        self.delete_pushButton.clicked.connect(self.delete_laptop)
        self.find_search_pushButton.clicked.connect(self.recommendation)
        self.find_reset_pushButton.clicked.connect(self.reset)

        self.hdd_checkBox.stateChanged.connect(self.hdd_checkbox_check)
        self.ssd_checkBox.stateChanged.connect(self.ssd_checkbox_check)

        self.addUser_pushButton.clicked.connect(self.add_new_user)
        self.login_pushButton_Edit.clicked.connect(self.login_user)
        self.esitUser_pushButton.clicked.connect(self.edit_user)
        self.deleteUser_pushButton.clicked.connect(self.delete_user)

    def hdd_checkbox_check(self):
        self.find_hdd_lineEdit.setEnabled(True)

    def ssd_checkbox_check(self):
        self.find_ssd_lineEdit.setEnabled(True)

    def create_database(self):
        database_db

    # ============================================== Oen Tab ========================================

    def open_laptop_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_insert_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_edit_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_user_tab(self):
        self.tabWidget.setCurrentIndex(3)

    # ============================================== Add Laptop =====================================

    def recommendation(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        brand = self.find_brand_lineEdit.text()
        model = self.find_model_lineEdit.text()
        cpu_brand = self.find_cpu_brand_lineEdit.text()
        cpu_bm = self.find_cp_brand_modofier__lineEdit.text()
        cpu_model = self.find_cpu_model_lineEdit.text()
        sd_ram = self.find_ram_lineEdit.text()
        ram_capacity = self.find_ram_capacity_lineEdit.text()
        display = self.find_display_lineEdit.text()
        graphic_card = self.find_graphi_card_lineEdit.text()
        graphic_card_rs = self.find_graphi_card_ram_size_lineEdit.text()
        hdd = self.find_hdd_lineEdit.text()
        ssd = self.find_ssd_lineEdit.text()

        sql = '''SELECT brand , model , cpu_brand , cpu_bm , cpu_model , sd_ram , ram_capacity , display ,
             graphic_card , graphic_card_rs , hdd , ssd , description FROM laptop
             WHERE (brand = %s OR model = %s OR cpu_brand = %s OR cpu_bm = %s OR cpu_model = %s OR sd_ram = %s OR
              ram_capacity = %s OR display = %s OR graphic_card = %s OR graphic_card_rs = %s OR hdd = %s OR ssd = %s)'''
        cursor.execute(sql, [(brand), (model), (cpu_brand), (cpu_bm), (cpu_model), (sd_ram),
                             (ram_capacity), (display), (graphic_card), (graphic_card_rs), (hdd), (ssd)])

        data = cursor.fetchall()
        print(data)
        if data is None:
            self.show_all_laptops()
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
            db.close()

    def show_all_laptops(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        cursor.execute('''
            SELECT brand , model , cpu_brand , cpu_bm , cpu_model , sd_ram , ram_capacity , display ,
             graphic_card , graphic_card_rs , hdd , ssd , description FROM laptop
        ''')

        data = cursor.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
        db.close()

    def reset(self):
        self.show_all_laptops()

    def add_new_laptop(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        brand = self.brand_lineEdit.text()
        model = self.model_lineEdit.text()
        cpu_brand = self.cpu_brand_lineEdit.text()
        cpu_bm = self.cpu_brand_modifier_lineEdit.text()
        cpu_model = self.cpu_model_lineEdit.text()
        sd_ram = self.ram_lineEdit.text()
        ram_capacity = self.ram_capacity_lineEdit.text()
        graphic_card = self.graphic_card_lineEdit.text()
        graphic_card_rs = self.graphic_card_ram_size_lineEdit.text()
        display = self.display_lineEdit.text()
        hdd = self.hdd_lineEdit.text()
        ssd = self.ssd_lineEdit.text()
        description = self.description_textEdit.toPlainText()

        cursor.execute('''
            INSERT INTO laptop (brand , model , cpu_brand , cpu_bm , cpu_model , sd_ram , ram_capacity , display ,
             graphic_card , graphic_card_rs , hdd , ssd , description)
             VALUES (%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s )
        ''', (
            brand, model, cpu_brand, cpu_bm, cpu_model, sd_ram, ram_capacity, display, graphic_card, graphic_card_rs,
            hdd, ssd, description))
        db.commit()
        db.close()
        self.message_box("Laptop Information Added!")
        self.show_all_laptops()

        self.brand_lineEdit.setText("")
        self.model_lineEdit.setText("")
        self.cpu_brand_lineEdit.setText("")
        self.cpu_brand_modifier_lineEdit.setText("")
        self.cpu_model_lineEdit.setText("")
        self.ram_lineEdit.setText("")
        self.ram_capacity_lineEdit.setText("")
        self.graphic_card_lineEdit.setText("")
        self.graphic_card_ram_size_lineEdit.setText("")
        self.display_lineEdit.setText("")
        self.hdd_lineEdit.setText("")
        self.ssd_lineEdit.setText("")
        self.description_textEdit.setPlainText("")

    # ============================================== Add Laptop =====================================
    def search_laptop(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        original_brand = self.search_brand_lineEdit.text()
        original_model = self.search_model_lineEdit.text()
        try:
            sql = '''SELECT * FROM laptop WHERE (brand= %s AND model=%s)'''
            cursor.execute(sql, [(original_brand), (original_model)])
            data = cursor.fetchone()
            if data is not None:
                self.edit_brand_lineEdit.setText(data[1])
                self.edit_model_lineEdit.setText(data[2])
                self.edit_cpu_brand_lineEdit.setText(data[3])
                self.edit_cpu_brand_modifier_lineEdit.setText(data[4])
                self.edit_cpu_model_lineEdit.setText(data[5])
                self.edit_ram_lineEdit.setText(data[6])
                self.edit_ram_capacity_lineEdit.setText(data[7])
                self.edit_graphic_card_lineEdit.setText(data[9])
                self.edit_graphic_card_ram_size_lineEdit.setText(data[10])
                self.edit_display_lineEdit.setText(data[8])
                self.edit_hdd_lineEdit.setText(data[11])
                self.edit_ssd_lineEdit.setText(data[12])
                self.edit_description_textEdit.setPlainText(data[13])
        except ValueError:
            self.message_box("Record does not exist!")

    # ============================================== Edit Laptop =====================================

    def edit_laptop(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        original_brand = self.search_brand_lineEdit.text()
        original_model = self.search_model_lineEdit.text()

        brand = self.edit_brand_lineEdit.text()
        model = self.edit_model_lineEdit.text()
        cpu_brand = self.edit_cpu_brand_lineEdit.text()
        cpu_bm = self.edit_cpu_brand_modifier_lineEdit.text()
        cpu_model = self.edit_cpu_model_lineEdit.text()
        ram = self.edit_ram_lineEdit.text()
        ram_capacity = self.edit_ram_capacity_lineEdit.text()
        graphic_card = self.edit_graphic_card_lineEdit.text()
        graphic_card_rs = self.edit_graphic_card_ram_size_lineEdit.text()
        display = self.edit_display_lineEdit.text()
        hdd = self.edit_hdd_lineEdit.text()
        ssd = self.edit_ssd_lineEdit.text()
        description = self.edit_description_textEdit.toPlainText()

        cursor.execute('''
            UPDATE laptop SET brand = %s , model = %s , cpu_brand = %s , cpu_bm = %s , cpu_model = %s , sd_ram = %s ,
             ram_capacity = %s , display = %s , graphic_card = %s , graphic_card_rs = %s ,  hdd = %s , ssd = %s ,
            description = %s
            WHERE (brand = %s AND model = %s)
        ''', (
            brand, model, cpu_brand, cpu_bm, cpu_model, ram, ram_capacity, display, graphic_card, graphic_card_rs, hdd,
            ssd, description, original_brand, original_model))
        db.commit()
        db.close()
        self.message_box("information Updated!")
        self.show_all_laptops()

    # ============================================== delete Laptop =====================================

    def delete_laptop(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        original_brand = self.search_brand_lineEdit.text()
        original_model = self.search_model_lineEdit.text()

        warning = QMessageBox.warning(self, "Delete Laptop", "Are You Sure You want to Delete This Laptop Information?",
                                      QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM laptop WHERE (brand = %s AND model = %s)'''
            cursor.execute(sql, [(original_brand), (original_model)])
            db.commit()
            db.close()
            self.message_box("Laptop information Deleted!")
            self.show_all_laptops()

            self.search_brand_lineEdit.setText("")
            self.search_model_lineEdit.setText("")
            self.edit_brand_lineEdit.setText("")
            self.edit_model_lineEdit.setText("")
            self.edit_cpu_brand_lineEdit.setText("")
            self.edit_cpu_brand_modifier_lineEdit.setText("")
            self.edit_cpu_model_lineEdit.setText("")
            self.edit_ram_lineEdit.setText("")
            self.edit_ram_capacity_lineEdit.setText("")
            self.edit_graphic_card_lineEdit.setText("")
            self.edit_graphic_card_ram_size_lineEdit.setText("")
            self.edit_display_lineEdit.setText("")
            self.edit_hdd_lineEdit.setText("")
            self.edit_ssd_lineEdit.setText("")
            self.edit_description_textEdit.setPlainText("")

    # ============================================== Add New User =====================================

    def add_new_user(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        full_name = self.username_lineEdit.text()
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()
        password_confirm = self.passwordConfig_lineEdit.text()

        if password == password_confirm:
            cursor.execute('''
                        INSERT INTO user(fullname , email , password)
                        VALUES (%s , %s ,%s)
                    ''', (full_name, email, password))
            db.commit()
            self.message_box('User Added!')

            self.username_lineEdit.setText('')
            self.email_lineEdit.setText('')
            self.password_lineEdit.setText('')
            self.passwordConfig_lineEdit.setText('')
        else:
            self.wrong_password_label.setText('The Passwords Are Not Match!l')

    def login_user(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        username = self.username_lineEdit_edit_login.text()
        password = self.password_lineEdit_edit_login.text()

        sql = "SELECT * FROM user"
        cursor.execute(sql)
        data = cursor.fetchall()

        for row in data:
            if username == row[1] and password == row[3]:
                self.message_box('You Are In!')
                self.editUser_groupBox.setEnabled(True)

                self.username_lineEdit_edit.setText(row[1])
                self.email_lineEdit_edit.setText(row[2])
                self.password_lineEdit_edit.setText(row[3])

    def edit_user(self):
        fullname = self.username_lineEdit_edit.text()
        email = self.email_lineEdit_edit.text()
        password = self.password_lineEdit_edit.text()
        password_confirm = self.passwordConfig_lineEdit_edit.text()

        if password == password_confirm:
            db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
            cursor = db.cursor()

            original_username = self.username_lineEdit_edit_login.text()
            cursor.execute('''
                        UPDATE user SET fullname =%s , email =%s , password =%s WHERE fullname =%s
                    ''', (fullname, email, password, original_username))
            db.commit()

            self.message_box('Data Updated Successfully!')

            self.username_lineEdit_edit.setText('')
            self.email_lineEdit_edit.setText('')
            self.password_lineEdit_edit.setText('')
            self.passwordConfig_lineEdit_edit.setText('')
            self.editUser_groupBox.setEnabled(False)
        else:
            self.message_box('Invalid Information!')

    def delete_user(self):
        db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@', database='laptop')
        cursor = db.cursor()

        user_original_username = self.username_lineEdit_edit_login.text()
        warning = QMessageBox.warning(self, 'Delete User', 'Are You Sure You Want to Delete This User?',
                                      QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM user WHERE fullname=%s'''
            cursor.execute(sql, [(user_original_username)])
            db.commit()
            db.close()
            self.message_box('User Deleted!')

            self.username_lineEdit_edit.setText('')
            self.email_lineEdit_edit.setText('')
            self.password_lineEdit_edit.setText('')
            self.passwordConfig_lineEdit_edit.setText('')

            self.username_lineEdit_edit_login.setText('')
            self.password_lineEdit_edit_login.setText('')

    def message_box(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)

        msg.exec()


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
