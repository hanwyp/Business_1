#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :loginMain.py
@Author  :keyin
@Time    :2021-01-21 11:23
"""
from PyQt5 import QtCore
from PyQt5.Qt import *
from login import *

class Window(Ui_login,QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)





if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    import sys
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())