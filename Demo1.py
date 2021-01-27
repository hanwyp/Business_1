import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

print(sqlalchemy.__version__)

engine = create_engine('sqlite:///Business_license.db?check_same_thread=False', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DBSession = sessionmaker(bind=engine)

from sqlalchemy import Column, Integer, String


class BasicInfo(Base):
    __tablename__ = 'BasicInfo'

    PeopleID = Column(Integer, primary_key=True, autoincrement=True)
    PeopleName = Column(String(20))
    PeopleSex = Column(BOOLEAN)
    PeopleNation = Column(String(10))
    PeopleAddress = Column(String(100))
    IdNumber = Column(String(18))
    PeopleValStart = Column(String(10))
    PeopleValEnd = Column(String(10))
    PicFront = Column(String(100))
    PicBack = Column(String(100))

    def __repr__(self):
        return "%s,%s,%s,%s" % (self.PeopleName, self.PeopleSex, self.PeopleNation, self.IdNumber)


if __name__ == '__main__':

    db_session = DBSession()
    # 增
    new_user = BasicInfo(PeopleName='张44',PeopleSex=True,PeopleNation='汉')

    new_user.IdNumber = '120225198907083716'
    db_session.add(new_user)
    # 改
    # res = session.query(user).filter(user.PeopleName=='张三').update({'PeopleName':'lisi'})
    # res = db_session.query(BasicInfo).filter(BasicInfo.PeopleName == 'zhangsan')
    # res.update({'IdNumber':'120225196205033598'})

    db_session.commit()
    db_session.close()