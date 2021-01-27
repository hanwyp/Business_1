import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class BasicInfo(Base):
    __tablename__ = 'BasicInfo'

    PeopleID = Column(Integer, primary_key=True, autoincrement=True)
    PeopleName = Column(String(20))
    PeopleSex = Column(String(4))
    PeopleNation = Column(String(10))
    PeopleAddress = Column(String(100))
    IdNumber = Column(String(18))
    PeopleValStart = Column(String(10))
    PeopleValEnd = Column(String(10))
    PicFront = Column(String(100))
    PicBack = Column(String(100))

    def __repr__(self):
        return "%s,%s,%s,%s" % (self.PeopleName, self.PeopleSex, self.PeopleNation, self.IdNumber)
