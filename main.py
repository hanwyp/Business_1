#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :main.py
@Author  :keyin
@Time    :2021-01-18 12:52
"""

import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    print(os.environ['PATH'])

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QApplication, QMessageBox

from MainWindow import *
from AipOcr import *
from myTools import *
from models import *
import shutil



class Window(Ui_MainWindow, QMainWindow):

    imgName = ''
    imgNameB = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnF.clicked.connect(lambda: self.openImg('Front'))
        self.btnB.clicked.connect(lambda: self.openImg('Back'))
        self.btnOK.clicked.connect(self.create_car)


    def openImg(self, face):

        # return (card.name, card.sex, card.nation, card.ID_numer, card.address)
        # print(str)
        if face == 'Front':

            self.imgName, imgType = QFileDialog.getOpenFileName()
            self.lbl_Front.setPixmap(QPixmap(self.imgName))

            vbox = QVBoxLayout()
            vbox.addWidget(self.lbl_Front)
            self.setLayout(vbox)
            self.lbl_Front.setScaledContents(True)

            aip = CardAip(self.imgName)
            card = aip.getinfo(face)

            self.txt_name.setText(card.name)
            self.txt_sex.setText(card.sex)
            self.txt_id_numer.setText(card.ID_numer)
            self.txt_address.setText(card.address)
            self.txt_nation.setText(card.nation)

        if face == 'Back':
            self.imgNameB, imgType = QFileDialog.getOpenFileName()
            self.lbl_back.setPixmap(QPixmap(self.imgNameB))
            vbox = QVBoxLayout()
            vbox.addWidget(self.lbl_back)
            self.setLayout(vbox)
            self.lbl_back.setScaledContents(True)

            aip = CardAip(self.imgNameB)
            card = aip.getinfo(face)
            self.txt_start.setText(card.start)
            self.txt_end.setText(card.end)
    def create_car(self):

        new_car = BasicInfo()
        new_car.PeopleName=self.txt_name.text()
        new_car.PeopleSex = self.txt_sex.text()
        new_car.IdNumber = self.txt_id_numer.text()
        new_car.PeopleAddress = self.txt_address.text()
        new_car.PeopleNation = self.txt_nation.text()
        new_car.PeopleValStart = self.txt_start.text()
        new_car.PeopleValEnd = self.txt_end.text()


        if my_find(new_car.IdNumber):

            if len(self.imgName)!=0:
                path = os.path.abspath('.')
                new = os.path.join(path,'DataImg',new_car.PeopleName+new_car.IdNumber+'_1.jpg')
                shutil.copyfile(self.imgName, new)
                new_car.PicFront = new
            if len(self.imgNameB)!=0:
                new_2 = os.path.join(path,'DataImg',new_car.PeopleName+new_car.IdNumber+'_2.jpg')
                shutil.copyfile(self.imgNameB,new_2)
                new_car.PicBack = new_2

            my_save(new_car)
        else:
            reply = QMessageBox.question(self,'信息', '已录入，更新吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print('daoci-------------------------------')
                if len(self.imgName) != 0:
                    path = os.path.abspath('.')
                    new = os.path.join(path, 'DataImg', new_car.PeopleName + new_car.IdNumber + '_1.jpg')
                    shutil.copyfile(self.imgName, new)
                    new_car.PicFront = new
                    print(new_car.PicFront)
                if len(self.imgNameB) != 0:
                    new_2 = os.path.join(path, 'DataImg', new_car.PeopleName + new_car.IdNumber + '_2.jpg')
                    shutil.copyfile(self.imgNameB, new_2)
                    new_car.PicBack = new_2
                    print(new_car.PicBack)
                my_updata(new_car.IdNumber)
            else:
                print('no---------------')


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
