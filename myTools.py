#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :myTools.py
@Author  :keyin
@Time    :2021-01-26 11:17
"""


import sqlalchemy

from models import *
from datetime import datetime


# engine = create_engine('sqlite:///Business_license.db?check_same_thread=False', echo=True)
engine = create_engine('sqlite:///Business.db?check_same_thread=False', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DBSession = sessionmaker(bind=engine)




def my_save(new_card, user):
    db_session = DBSession()
    db_session.add(new_card)
    db_session.add(user)
    db_session.commit()
    db_session.close()

def my_find(Number):
    db_session = DBSession()
    data = db_session.query(BasicInfo).filter_by(IdNumber=Number).first()

    db_session.close()

    if (data is None):
        return True
    else:
        return False

def my_find_re(Number):
    db_session = DBSession()
    data = db_session.query(BasicInfo).filter_by(IdNumber=Number).first()
    db_session.close()
    return data

def my_updata( card, user):
    db_session = DBSession()
    data = db_session.query(BasicInfo).filter_by(IdNumber=card.IdNumber).first()
    user_data = db_session.query(UserInfo).filter_by(idNumber=card.IdNumber).first()

    data.PeopleName = card.PeopleName
    data.PeopleSex = card.PeopleSex
    data.PeopleNation = card.PeopleNation
    data.IdNumber = card.IdNumber
    data.PeopleAddress = card.PeopleAddress
    data.PeopleValStart = card.PeopleValStart
    data.PeopleValEnd = card.PeopleValEnd
    data.PicFront = card.PicFront
    data.PicBack = card.PicBack

    if user_data is not None:

        user_data.wechat = user.wechat
        user_data.PhoneCheck = user.PhoneCheck
        user_data.peoplePhone = user.peoplePhone
        user_data.idNumber = user.idNumber
        user_data.educationalBackground = user.educationalBackground

    db_session.commit()
    db_session.close()

def read_tab():
    db_session = DBSession()
    data = db_session.query(BasicInfo).order_by(BasicInfo.PeopleID.desc()).all()

    if data is not None:
        data_list=[]
        for item in data:
            item_list = []
            item_list.append(item.PeopleName)
            item_list.append(item.PeopleNation)
            item_list.append(str(item.IdNumber))
            data_list.append(item_list)
        return data_list

    # db_session.commit()
    db_session.close()

def bus_save(info):
    pass

def dateChange(date):
    expiration_year = int(date[:4])
    expiration_month = int(date[5:7])
    expiration_date = int(date[8:10])
    expiration_date = datetime(expiration_year, expiration_month, expiration_date)
    return expiration_date

if __name__ == '__main__':

    info = BusinessLicense()
    info.busCreditCode = '92120225MA0742Q49U'
    info.busDesignation = '天津市蓟州区志静兴养殖场'
    info.busIdNumber = '120224197311231510'

    print(info)
    db_session = DBSession()
    # db_session.query(BusinessLicense).filter(BusinessLicense.busId==1).delete()
    # db_session.query(BusinessLicense).filter(BusinessLicense.busIdNumber=='120224197311231510').delete()
    #
    db_session.add(info)
    db_session.commit()
    db_session.close()

