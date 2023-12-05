from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)