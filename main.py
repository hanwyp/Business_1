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

from PyQt5.Qt import *

from MainWindow import *
from AipOcr import *
from myTools import *
from models import *
import shutil


class myThread(QThread):
    trigger = pyqtSignal(object)  # 自定义一个信号，object是要返回给回调函数的返回值的Type

    def __init__(self, imgName, face):
        super(myThread, self).__init__()
        self.imgName = imgName
        self.face = face

    def run(self):
        aip = CardAip(self.imgName)
        card = aip.getinfo(self.face)
        self.trigger.emit(card)


class Window(Ui_MainWindow, QMainWindow):
    imgName = ''
    imgNameB = ''
    read_flag = True

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.tab_view()
        # self.btnF.clicked.connect(lambda: self.openimg_trF('Front'))
        # self.btnB.clicked.connect(lambda: self.openimg_trB('Back'))
        self.btnOK.clicked.connect(self.create_car)
        self.btnNew.clicked.connect(self.btnNew_click)
        self.btnEdit.clicked.connect(self.btnEdit_click)
        self.btnDel.clicked.connect(self.del_click)
        self.btnCancel.clicked.connect(self.cancel_click)
        self.lbl_Front.clicked.connect(lambda: self.openimg_trF('Front'))
        self.lbl_back.clicked.connect(lambda: self.openimg_trB('Back'))
        self.btnBus.clicked.connect(lambda: self.btnBus_click(self.txt_id_numer.text()))

        self.tableWidget.clicked.connect(self.addTxt)
        # self.base_info.currentChanged.connect(lambda: self.btnBus_click(self.txt_id_numer.text()))

    def setup_ui(self):
        self.setupUi(self)
        self.tab_view()

    def Edit_ui(self):
        for i in self.base_info.findChildren(QLineEdit):
            i.setEnabled(True)
        self.btnOK.setEnabled(True)
        self.btnNew.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.tableWidget.setEnabled(False)
        # self.btnB.setEnabled(True)
        # self.btnF.setEnabled(True)
        self.btnCancel.setEnabled(True)
        self.lbl_Front.setEnabled(True)
        self.lbl_back.setEnabled(True)
        self.comEducationalBackground.setEnabled(True)

    def save_ui(self):
        for i in self.base_info.findChildren(QLineEdit):
            i.setEnabled(False)
        self.btnOK.setEnabled(False)
        self.btnNew.setEnabled(True)
        self.btnEdit.setEnabled(False)
        self.tableWidget.setEnabled(True)
        # self.btnB.setEnabled(False)
        # self.btnF.setEnabled(False)
        self.btnCancel.setEnabled(False)
        self.lbl_Front.setEnabled(False)
        self.lbl_back.setEnabled(False)
        self.comEducationalBackground.setEnabled(False)

    def new_ui(self):
        for i in self.base_info.findChildren(QLineEdit):
            i.setEnabled(True)
            i.setText('')
        self.btnOK.setEnabled(True)
        self.btnNew.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.tableWidget.setEnabled(False)
        # self.btnB.setEnabled(True)
        # self.btnF.setEnabled(True)
        self.btnCancel.setEnabled(True)
        self.lbl_Front.setEnabled(True)
        self.lbl_back.setEnabled(True)
        self.comEducationalBackground.setCurrentIndex(-1)
        self.comEducationalBackground.setEnabled(True)

        # self.lbl_Front.clear()
        self.lbl_Front.setText('头像面')
        # self.lbl_back.clear()
        self.lbl_back.setText('国徽面')



        """
        path = os.path.abspath('.')
        self.imgName = os.path.join(path, 'DataImg', 'none.jpg')
        self.imgNameB = os.path.join(path, 'DataImg', 'none.jpg')

        self.lbl_Front.setPixmap(QPixmap(self.imgName))

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl_Front)
        self.setLayout(vbox)
        self.lbl_Front.setScaledContents(True)

        self.lbl_back.setPixmap(QPixmap(self.imgNameB))

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl_back)
        self.setLayout(vbox)
        self.lbl_back.setScaledContents(True)
        """

    def del_ui(self):
        pass

    def cancel_ui(self):
        # self.new_ui()
        for i in self.base_info.findChildren(QLineEdit):
            i.setEnabled(False)
            # i.setText('')
        self.btnOK.setEnabled(False)
        self.tableWidget.setEnabled(True)
        self.btnNew.setEnabled(True)
        self.btnCancel.setEnabled(False)
        self.lbl_Front.setEnabled(True)
        self.lbl_back.setEnabled(True)
        self.lbl_Front.setEnabled(False)
        self.lbl_back.setEnabled(False)
        self.comEducationalBackground.setEnabled(False)

        db_session = DBSession()
        data = db_session.query(UserInfo).filter_by(idNumber=self.txt_id_numer.text()).first()
        db_session.close()
        if data is not None:
            self.comEducationalBackground.setCurrentIndex(int(data.educationalBackground))

    def btnNew_click(self):
        self.new_ui()

    def btnEdit_click(self):
        self.Edit_ui()

    def btnBus_click(self, idNumber):

        self.txt_busIdNumber.setText(idNumber)
        self.txt_busSelect.setText(idNumber)
        self.tabWidget.setCurrentIndex(1)

    def del_click(self):
        db_session = DBSession()
        name = self.txt_name.text()
        number = self.txt_id_numer.text()
        if number != '' and name != '':
            db_session.query(UserInfo).filter(UserInfo.idNumber == number).delete()
            db_session.query(BasicInfo).filter(BasicInfo.IdNumber == number).delete()
            db_session.commit()
        db_session.close()
        self.tab_view()
        self.new_ui()
        self.save_ui()

    def cancel_click(self):
        self.cancel_ui()

    def openimg_trF(self, face):
        if self.openImg(face):
            self.mbt = myThread(self.imgName, face)  # 定义线程，self.imgName和face是参数
            self.mbt.trigger.connect(self.viewF)  # 定义线程结束后执行那个函数，参数是信号发送emit后的值
            self.mbt.start()

    def openimg_trB(self, face):
        if self.openImg(face):
            self.mbt2 = myThread(self.imgNameB, face)
            self.mbt2.trigger.connect(self.viewB)  # 定义线程结束后执行那个函数，参数是信号发送emit后的值
            self.mbt2.start()

    def addTxt(self):

        '''
         作用：鼠标单击事件监听，显示被选中的单元格
        '''
        # 打印被选中的单元格
        i_list = []
        for i in self.tableWidget.selectedItems():
            i_list.append(str(i.text()))
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
        self.read_flag = False

        if data.PicFront is not None:
            self.imgView(data.PicFront)

        else:
            self.imgView('none1.jpg')

        if data.PicBack is not None:
            self.imgView(data.PicBack)

        else:
            self.imgView('none.jpg')

        if self.txt_name is not None:
            self.btnEdit.setEnabled(True)

        db_session = DBSession()
        user_data = db_session.query(UserInfo).filter_by(idNumber=data.IdNumber).first()
        # user_data = UserInfo()
        db_session.close()

        if user_data is not None:
            self.txt_wechat.setText(str(user_data.wechat))
            self.txt_check.setText(str(user_data.PhoneCheck))
            self.txt_Phone.setText(str(user_data.peoplePhone))
            self.btnDel.setEnabled(True)
            self.comEducationalBackground.setCurrentIndex(int(user_data.educationalBackground))
        else:
            self.txt_wechat.setText(None)
            self.txt_check.setText(None)
            self.txt_Phone.setText(None)

    def imgView(self, new_file):
        path = os.path.abspath('.')
        new = os.path.join(path, 'DataImg', new_file)

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
            self.imgName, _ = QFileDialog.getOpenFileName(filter='*.jpg;*.png')

            if self.imgName != '':

                self.lbl_Front.setPixmap(QPixmap(self.imgName))

                vbox = QVBoxLayout()
                vbox.addWidget(self.lbl_Front)
                self.setLayout(vbox)
                self.lbl_Front.setScaledContents(True)
                return True
            else:
                return False

        if face == 'Back':
            self.imgNameB, imgType = QFileDialog.getOpenFileName(filter='*.jpg;*.png')
            if self.imgName != '':

                self.lbl_back.setPixmap(QPixmap(self.imgNameB))
                vbox = QVBoxLayout()
                vbox.addWidget(self.lbl_back)
                self.setLayout(vbox)
                self.lbl_back.setScaledContents(True)
                return True
            else:
                return False

    def viewF(self, card):
        if card is not None:
            self.txt_name.setText(card.name)
            self.txt_sex.setText(card.sex)
            self.txt_id_numer.setText(card.ID_numer)
            self.txt_address.setText(card.address)
            self.txt_nation.setText(card.nation)

    def viewB(self, card):
        if card is not None:
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

    # 身份信息保存、更新
    def create_car(self):

        new_car = BasicInfo()
        user = UserInfo()
        new_car.PeopleName = self.txt_name.text()
        new_car.PeopleSex = self.txt_sex.text()
        new_car.IdNumber = self.txt_id_numer.text()
        new_car.PeopleAddress = self.txt_address.text()
        new_car.PeopleNation = self.txt_nation.text()
        new_car.PeopleValStart = self.txt_start.text()
        new_car.PeopleValEnd = self.txt_end.text()

        user.idNumber = self.txt_id_numer.text()
        user.peoplePhone = self.txt_Phone.text()
        user.PhoneCheck = self.txt_check.text()
        user.wechat = self.txt_wechat.text()
        user.educationalBackground = self.comEducationalBackground.currentIndex()

        if len(new_car.PeopleName) != 0:
            if my_find(new_car.IdNumber):

                if len(self.imgName) != 0:
                    new_car.PicFront = self.pathAdd(new_car, '1')
                if len(self.imgNameB) != 0:
                    new_car.PicBack = self.pathAdd(new_car, '2')

                my_save(new_car, user)
                # self.save_ui()
            else:
                reply = QMessageBox.question(self, '信息', '已录入，更新吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    """
                    将文件名复制给PicFront、PicBack
                    """
                    if self.read_flag:

                        if len(self.imgName) != 0:
                            new_car.PicFront = self.pathAdd(new_car, '1')
                        if len(self.imgNameB) != 0:
                            new_car.PicBack = self.pathAdd(new_car, '2')

                    else:
                        new_car.PicFront = self.imgName
                        new_car.PicBack = self.imgNameB
                    my_updata(new_car, user)

            self.tab_view()

        else:
            QMessageBox.question(self, '信息', '必须有姓名！', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        self.save_ui()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
