import sys, os
import threading
from myTools import *

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
        self.comEducationalBackground.currentIndexChanged.connect(self.sel)

    def sel(self):
        print(self.comEducationalBackground.currentText())



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    def ch():
        # info = BusinessLicense()
        # date_now = dateChange(window.de_Application.text())
        # info.busApplicationDate = date_now
        # print(info.busApplicationDate)
        # db_session = DBSession()
        #
        # db_session.add(info)
        # db_session.commit()
        # db_session.close()

        date_now = datetime.date.today()
        print(str(date_now))


    def delet():
        db_session = DBSession()
        data = db_session.query(BusinessLicense).all()

        # print(">>>>>>", data)

        for i in data:
            print(">>>>>",i)
            db_session.delete(i)
        db_session.commit()
        db_session.close()


    window.btnBusNew.clicked.connect(ch)
    # window.btnBusDel.clicked.connect(delet)

    # db_session = DBSession()
    #
    # db_session.add(info)
    # db_session.commit()
    # db_session.close()
    #
    sys.exit(app.exec_())

