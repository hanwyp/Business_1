import sys, os
import threading

from PyQt5.QtCore import QThread, pyqtSignal

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    print(os.environ['PATH'])

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QApplication, QMessageBox, QTableWidgetItem, QPushButton, QLineEdit
from PyQt5 import *


from MainWindow import *
from AipOcr import *
from myTools import *
from models import *
import shutil

class Window(Ui_MainWindow, QMainWindow):
    imgName = ''
    imgNameB = ''
    read_flag = True

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.btnF.clicked.connect(lambda: self.openimg_trF('Front'))
        # self.btnB.clicked.connect(lambda: self.openimg_trB('Back'))
        # self.btnOK.clicked.connect(self.create_car)
        # self.tab_view()
        # # self.tabView.clicked.connect(self.tab_view)
        # self.tableWidget.clicked.connect(self.addTxt)




if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    # window.setEnabled()
    # for i in  window.base_info.findChildren(QLineEdit):
    #     i.setEnabled(True)

    # for i in window.base_info.findChildren(QPushButton):
    #     i.setEnabled(False)

    # window.btnNew.setEnabled(True)
    QFileDialog.getOpenFileName(filter='*.jpg;*.png')

    sys.exit(app.exec_())

