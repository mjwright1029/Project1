from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.amount_label.hide()
        self.deposit_button.hide()
        self.withdraw_button.hide()
        self.balance_button.hide()
        self.balance_display.hide()

        font = QFont()
        font.setPointSize(30)

        self.name_title.setFont(font)
        self.name_title.setText('NAME: ')

        self.pin_title.setFont(font)
        self.pin_title.setText('PIN: ')