from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from gui import *
import csv
import re


class Logic(QMainWindow, Ui_MainWindow):
    """
    Class representing the logic for how the objects will work
    """
    def __init__(self) -> None:
        """
        Method to set the default text and values of a logic object
        """
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

    def log_in(self) -> None:
        """
        Method to log a user in to their account if it already exists
        """
        name = re.sub(' +', ' ', self.name_label.text().lower().strip())
        pin = str(self.pin_label.text())
        self.error_message.hide()

        if len(pin) != 4:
            self.error_message.show()
            self.error_message.setText('Please enter in a valid 4 digit PIN.')
            self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            return

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

    def create_account(self) -> None:
        """
        Method to create an account if a valid name and pin are entered
        """
        new_name = re.sub(' +', ' ', self.name_label.text().strip())
        new_pin = str(self.pin_label.text())
        self.error_message.hide()

        if not self.name_label.text().strip():
            self.error_message.show()
            self.error_message.setText('Please enter in a valid name.')
            self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            return

        if not self.pin_label.text().strip():
            self.error_message.show()
            self.error_message.setText('Please enter in a valid PIN.')
            self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            return

        if len(new_pin) != 4:
            self.error_message.show()
            self.error_message.setText('Please enter in a valid 4 digit PIN.')
            self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            return

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

    def check_for_account(self, name: str, pin: str) -> bool:
        """
        Method to check is an account already exists
        :param name: the name entered for the account
        :param pin: the PIN entered for the account
        :return: True if the account exists, False if it doesn't
        """
        with open('accounts.csv', 'r', newline='', encoding='utf-8') as csvfile:
            content = csv.reader(csvfile, delimiter=',')

            for row in content:
                if row and row[0].lower().strip() == name and row[1] == pin:
                    return True
        return False

    def deposit(self) -> bool:
        """
        Method to deposit an amount of money
        :return: False if the amount is less than or equal to 0, True if not
        """
        try:
            amount = float(self.amount_label.text())
            if amount <= 0:
                self.balance_display.setText('Please select a valid amount.')
                self.amount_label.clear()
                return False
            else:
                new_balance = self.get_balance() + amount
                self.set_balance(new_balance)
                self.update_balance(new_balance)
                self.balance_display.setText(f'Deposited ${amount:.2f}')
                return True
        except ValueError:
            self.balance_display.setText('Please select a valid amount.')
            self.amount_label.clear()

    def withdraw(self) -> bool:
        """
        Method to withdraw an amount of money
        :return: False if amount is less than or equal to 0 or greater than the balance, True if not
        """
        try:
            amount = float(self.amount_label.text())
            if amount <= 0 or amount > self.__account_balance:
                self.balance_display.setText('Please select a valid amount.')
                self.amount_label.clear()
                return False
            else:
                new_balance = self.get_balance() - amount
                self.set_balance(new_balance)
                self.update_balance(new_balance)
                self.balance_display.setText(f'Withdrew ${amount:.2f}')
                return True
        except ValueError:
            self.balance_display.setText('Please select a valid amount.')
            self.amount_label.clear()

    def get_balance(self) -> float:
        """
        Method to obtain the current account balance
        :return: the balance amount
        """
        self.balance_display.setText(f'Current balance is ${self.__account_balance:.2f}')
        self.amount_label.clear()
        return self.__account_balance

    def set_balance(self, value: float) -> None:
        """
        Method to set the balance of the account
        :param value: the new value of the balance
        """
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def update_balance(self, new_balance: float) -> None:
        """
        Method to update the balance of the csv file
        :param new_balance: the new value of the balance
        """
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
