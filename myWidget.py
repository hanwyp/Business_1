#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :myWidget.py
@Author  :keyin
@Time    :2021-01-30 9:22
"""

from PyQt5.Qt import *


class myLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit()
