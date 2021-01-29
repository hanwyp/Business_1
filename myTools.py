#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    :myTools.py
@Author  :keyin
@Time    :2021-01-26 11:17
"""


import sqlalchemy

from models import *


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

if __name__ == '__main__':
    db_session = DBSession()
    # user = BasicInfo(PeopleName='z42s', IdNumber='54815812223')
    # print(user)
    # userinfo = UserInfo(PhoneCheck='9896654452',idNumber=user.IdNumber)
    # print(userinfo)
    # db_session.add(user)
    # db_session.add(userinfo)
    # data = db_session.query(BasicInfo).filter(BasicInfo.IdNumber=='120225198207143589').delete()
    db_session.query(UserInfo).filter(UserInfo.idNumber=='120225198207143589').delete()
    # print(data)
    # data.delete()
    # print(data)


    db_session.commit()
    db_session.close()
