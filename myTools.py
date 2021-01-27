#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :myTools.py
@Author  :keyin
@Time    :2021-01-26 11:17
"""

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import *
import os, shutil


engine = create_engine('sqlite:///Business_license.db?check_same_thread=False', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DBSession = sessionmaker(bind=engine)


# if __name__ == '__main__':
#
#     db_session = DBSession()
#     # 增
#     new_user = BasicInfo(PeopleName='张44',PeopleSex=True,PeopleNation='汉')
#     new_user.IdNumber = '120225198907083716'
#     db_session.add(new_user)
#     # 改
#     # res = session.query(user).filter(user.PeopleName=='张三').update({'PeopleName':'lisi'})
#     # res = db_session.query(BasicInfo).filter(BasicInfo.PeopleName == 'zhangsan')
#     # res.update({'IdNumber':'120225196205033598'})
#
#     db_session.commit()
#     db_session.close()

def my_save(new_card):
    db_session = DBSession()
    # new_card = BasicInfo()
    # new_card.PeopleName = name
    db_session.add(new_card)
    db_session.commit()
    db_session.close()

def my_find(Number):
    db_session = DBSession()
    data = db_session.query(BasicInfo).filter_by(IdNumber =Number).first()
    if (data is None):
        return True
    else:
        return False
    db_session.commit()
    db_session.close()

def my_updata(Number):
    db_session = DBSession()
    data = db_session.query(BasicInfo).filter_by(IdNumber=Number).first()
    # data = card
    db_session.commit()
    db_session.close()
    # return data



if __name__ == '__main__':
    # my_find('12022519820318392X')
    my_updata('12022519820318392X')