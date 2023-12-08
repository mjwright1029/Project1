from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from gui import *
import csv
import re


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__account_balance = 0.0

        self.amount_label.hide()
        self.deposit_button.hide()
        self.withdraw_button.hide()
        self.balance_button.hide()
        self.balance_display.hide()
        self.error_message.hide()

        font_1 = QFont()
        font_1.setPointSize(25)

        self.name_title.setFont(font_1)
        self.name_title.setText('First & Last Name: ')

        self.pin_title.setFont(font_1)
        self.pin_title.setText('4 Digit PIN: ')

        self.login_button.clicked.connect(self.log_in)
        self.create_button.clicked.connect(self.create_account)

        self.deposit_button.clicked.connect(self.deposit)
        self.withdraw_button.clicked.connect(self.withdraw)
        self.balance_button.clicked.connect(self.get_balance)

    def log_in(self, ):
        name = re.sub(' +', ' ', self.name_label.text().lower().strip())
        pin = str(self.pin_label.text())
        self.error_message.hide()

        with open('accounts.csv', 'r', newline='', encoding='utf-8') as csvfile:
            content = csv.reader(csvfile, delimiter=',')

            for row in content:
                if row and row[0].lower().strip() == name and row[1] == pin:
                    balance = float(row[2])
                    self.set_balance(balance)
                    self.amount_label.show()
                    self.deposit_button.show()
                    self.withdraw_button.show()
                    self.balance_button.show()
                    self.balance_display.show()
                    self.error_message.show()

                    self.error_message.hide()
                    self.name_title.hide()
                    self.name_label.hide()
                    self.pin_title.hide()
                    self.pin_label.hide()
                    self.login_button.hide()
                    self.create_button.hide()
                    break

            else:
                self.error_message.show()
                self.error_message.setText('There is no account with that information. Please create an account.')
                self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                return

    def create_account(self):
        new_name = re.sub(' +', ' ', self.name_label.text().strip())
        new_pin = self.pin_label.text()
        self.error_message.hide()

        if self.check_for_account(new_name, new_pin):
            self.error_message.show()
            self.error_message.setText('This account already exists, please log in instead.')
            self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            return

        with open('accounts.csv', 'a', newline='', encoding='utf-8') as csvfile:
            content = csv.writer(csvfile, delimiter=',')
            content.writerow([new_name, new_pin, 0.0])

        self.amount_label.show()
        self.deposit_button.show()
        self.withdraw_button.show()
        self.balance_button.show()
        self.balance_display.show()
        self.error_message.show()

        self.error_message.hide()
        self.name_title.hide()
        self.name_label.hide()
        self.pin_title.hide()
        self.pin_label.hide()
        self.login_button.hide()
        self.create_button.hide()

    def check_for_account(self, name, pin):
        with open('accounts.csv', 'r', newline='', encoding='utf-8') as csvfile:
            content = csv.reader(csvfile, delimiter=',')

            for row in content:
                if row and row[0].lower().strip() == name and row[1] == pin:
                    return True
        return False


    def deposit(self):
        amount = float(self.amount_label.text())
        if amount <= 0:
            self.balance_display.setText('Please select a higher amount.')
            self.amount_label.clear()
            return False
        else:
            new_balance = self.get_balance() + amount
            self.set_balance(new_balance)
            self.update_balance(new_balance)
            self.set_balance(self.get_balance() + amount)
            self.balance_display.setText(f'Deposited ${amount:.2f}')
            return True

    def withdraw(self):
        amount = float(self.amount_label.text())
        if amount <= 0 or amount > self.__account_balance:
            self.balance_display.setText('Please select a smaller amount.')
            self.amount_label.clear()
            return False
        else:
            new_balance = self.get_balance() - amount
            self.set_balance(new_balance)
            self.update_balance(new_balance)
            self.set_balance(self.get_balance() - amount)
            self.balance_display.setText(f'Withdrew ${amount:.2f}')
            return True

    def get_balance(self):
        self.balance_display.setText(f'Current balance is ${self.__account_balance:.2f}')
        self.amount_label.clear()
        return self.__account_balance

    def set_balance(self, value):
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def update_balance(self, new_balance):
        name = re.sub(' +', ' ', self.name_label.text().lower().strip())
        pin = self.pin_label.text()

        rows = []
        with open('accounts.csv', 'r', newline='', encoding='utf-8') as csvfile:
            content = csv.reader(csvfile, delimiter=',')
            for row in content:
                if row and row[0].lower().strip() == name and row[1] == pin:
                    row[2] = str(new_balance)
                rows.append(row)

        with open('accounts.csv', 'w', newline='', encoding='utf-8') as csvfile:
            content = csv.writer(csvfile, delimiter=',')
            content.writerows(rows)


