#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :auxMain.py
@Author  :keyin
@Time    :2021-02-05 17:00
"""
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
@File    :main.py
@Author  :keyin
@Time    :2021-01-18 12:52
"""

import sys
from PyQt5.Qt import *


from auxiliary import *
from AipOcr import *
from myTools import *
from models import *
import shutil





class Window(Ui_Form, QWidget):

    desktop = QGuiApplication.primaryScreen()

    def __init__(self):
        super().__init__()
        self.setup_ui()


    def setup_ui(self):
        self.setupUi(self)
        desktop = QGuiApplication.primaryScreen().availableGeometry()
        # PyQt5.QtCore.QRect(0, 0, 1920, 1040)
        x = desktop.width()
        y = desktop.height()


        x1 = self.frameGeometry().width()
        y1 = self.frameGeometry().height()
        self.move(x-x1,y-y1-40)


        # self.move(self.desktop.availableGeometry().width()-self.width(),self.desktop.availableGeometry().height()-self.height())
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)





if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
