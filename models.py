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
    license = relationship("BusinessLicense")



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
    educationalBackground = Column(String, default='-1', server_default='-1')

    def __repr__(self):
        return "%s,%s,%s,%s" % (self.idNumber, self.peopleUser, self.peoplePassword, self.PhoneCheck)

#  business license
class BusinessLicense(Base):
    __tablename__ = 'businessLicense'

    busId = Column(Integer, primary_key=True, autoincrement=True)   # id
    busIdNumber = Column(String, ForeignKey('BasicInfo.IdNumber'))  # 身份证号
    busCreditCode = Column(String)  # 信用代码
    busDesignation = Column(String) # 名称
    busType = Column(Integer)   # 类型
    busOperator = Column(String)    # 经营者姓名
    busScope = Column(String)  # 经营范围
    busOrganization = Column(String)   # 组织形式
    busApplicationDate = Column(Date)  # 申请日期
    busSite = Column(String)   # 经营场所
    busFund = Column(String)   # 注册资金
    busFmployeesNumber = Column(String)    # 从业人数
    busInspection = Column(Date)    # 年检日期






if __name__ == '__main__':
    Base.metadata.create_all(engine)