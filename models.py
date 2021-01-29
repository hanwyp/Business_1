import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///Business.db?check_same_thread=False', echo=True)
Base = declarative_base()

from sqlalchemy import Column, Integer, String

class BasicInfo(Base):
    __tablename__ = 'BasicInfo'

    PeopleID = Column(Integer, primary_key=True, autoincrement=True)
    PeopleName = Column(String(20))
    PeopleSex = Column(String(4))
    PeopleNation = Column(String(10))
    PeopleAddress = Column(String(100))
    IdNumber = Column(String(18), index=True)
    PeopleValStart = Column(String(10))
    PeopleValEnd = Column(String(10))
    PicFront = Column(String(100))
    PicBack = Column(String(100))

    user = relationship('UserInfo', uselist=False, backref='BasicInfo')



    def __repr__(self):
        return "%s,%s,%s,%s" % (self.PeopleName, self.PeopleSex, self.PeopleNation, self.IdNumber)

class UserInfo(Base):
    __tablename__ = 'userInfo'

    userId = Column(Integer, primary_key=True, autoincrement=True)
    idNumber = Column(String, ForeignKey('BasicInfo.IdNumber'))
    peopleUser = Column(String)
    peoplePassword = Column(String(10))
    peoplePhone = Column(String(100))
    PhoneCheck = Column(String(18))
    wechat = Column(String(10))

    def __repr__(self):
        return "%s,%s,%s,%s" % (self.idNumber, self.peopleUser, self.peoplePassword, self.PhoneCheck)


if __name__ == '__main__':
    Base.metadata.create_all(engine)