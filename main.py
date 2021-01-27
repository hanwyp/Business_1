#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :main.py
@Author  :keyin
@Time    :2021-01-18 12:52
"""

import sys, os
from threading import Thread

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    print(os.environ['PATH'])

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QApplication, QMessageBox, QTableWidgetItem

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
        self.btnF.clicked.connect(lambda: self.openImg('Front'))
        self.btnB.clicked.connect(lambda: self.openImg('Back'))
        self.btnOK.clicked.connect(self.create_car)
        self.tab_view()
        # self.tabView.clicked.connect(self.tab_view)
        self.tableWidget.clicked.connect(self.addTxt)

    def addTxt(self):

        '''
         作用：双击事件监听，显示被选中的单元格
        '''
        # 打印被选中的单元格
        i_list = []
        for i in self.tableWidget.selectedItems():
            i_list.append(str(i.text()))
        print(i_list[2])
        data = my_find_re(i_list[2])
        self.txt_name.setText(data.PeopleName)
        self.txt_nation.setText(data.PeopleNation)
        self.txt_sex.setText(data.PeopleSex)
        self.txt_address.setText(data.PeopleAddress)
        self.txt_id_numer.setText(str(data.IdNumber))
        self.txt_start.setText(str(data.PeopleValStart))
        self.txt_end.setText(str(data.PeopleValEnd))
        self.imgName = data.PicFront
        self.imgNameB = data.PicBack
        print(self.imgName,self.imgNameB)
        self.read_flag = False

        if data.PicFront is not None:
            self.imgView(data.PicFront)

        else:
            self.imgView('none1.jpg')

        if data.PicBack is not None:
            self.imgView(data.PicBack)

        else:
            self.imgView('none.jpg')

    def imgView(self, new_file):
        path = os.path.abspath('.')
        new = os.path.join(path, 'DataImg', new_file)
        print(new_file[-5])

        if new_file[-5] == '1':
            self.lbl_Front.setPixmap(QPixmap(new))
            vbox = QVBoxLayout()
            vbox.addWidget(self.lbl_Front)
            self.setLayout(vbox)
            self.lbl_Front.setScaledContents(True)
        else:
            self.lbl_back.setPixmap(QPixmap(new))
            vbox = QVBoxLayout()
            vbox.addWidget(self.lbl_back)
            self.setLayout(vbox)
            self.lbl_back.setScaledContents(True)

            # self.txt_name.setText()

    def tab_view(self):
        items = read_tab()
        # print(len(items))
        if len(items) != 0:

            self.tableWidget.setRowCount(len(items))

            row = 0
            column = 0
            for item in items:
                for i in item:
                    row = 0
                    item = QTableWidgetItem(i)
                    # item = i
                    self.tableWidget.setItem(row, column, item)

                    column = column + 1

                row = row + 1

    def openImg(self, face):

        self.read_flag = True

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

    def pathAdd(self, new_car, num):
        """
        复制身份证图片，返回新的文件名
        :param new_car: 身份证类
        :param num: 文件后缀数字，‘1’代表正面，‘2’代表背面
        :return: 存储的文件名
        """
        path = os.path.abspath('.')
        new_file = new_car.PeopleName + new_car.IdNumber + '_' + num + '.jpg'
        new = os.path.join(path, 'DataImg', new_file)
        if num == '1':
            shutil.copyfile(self.imgName, new)
        else:
            shutil.copyfile(self.imgNameB, new)

        return new_file

    def create_car(self):



        new_car = BasicInfo()
        new_car.PeopleName = self.txt_name.text()
        new_car.PeopleSex = self.txt_sex.text()
        new_car.IdNumber = self.txt_id_numer.text()
        new_car.PeopleAddress = self.txt_address.text()
        new_car.PeopleNation = self.txt_nation.text()
        new_car.PeopleValStart = self.txt_start.text()
        new_car.PeopleValEnd = self.txt_end.text()


        if my_find(new_car.IdNumber):

            if len(self.imgName) != 0:
                new_car.PicFront = self.pathAdd(new_car, '1')
            if len(self.imgNameB) != 0:
                new_car.PicBack = self.pathAdd(new_car, '2')

            my_save(new_car)
        else:
            reply = QMessageBox.question(self, '信息', '已录入，更新吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                """
                将文件名复制给PicFront、PicBack
                """
                # if len(self.imgName) != 0:
                #     if len(self.imgName) != 0:
                #         new_car.PicFront = self.pathAdd(new_car, '1')
                #     if len(self.imgNameB) != 0:
                #         new_car.PicBack = self.pathAdd(new_car, '2')
                # if len(self.imgNameB) != 0:
                #     if len(self.imgName) != 0:
                #         new_car.PicFront = self.pathAdd(new_car, '1')
                #     if len(self.imgNameB) != 0:
                #         new_car.PicBack = self.pathAdd(new_car, '2')
                if self.read_flag:

                    if len(self.imgName) != 0:
                        new_car.PicFront = self.pathAdd(new_car, '1')
                    if len(self.imgNameB) != 0:
                        new_car.PicBack = self.pathAdd(new_car, '2')

                else:
                    new_car.PicFront = self.imgName
                    new_car.PicBack = self.imgNameB
                my_updata(new_car)
        self.tab_view()

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
