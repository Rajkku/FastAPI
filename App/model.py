from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Teacher(Base):
    __tablename__ = "teacherlist"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    subject = Column(String)
    Hashpassword = Column(String)


class Table(Base):
    __tablename__ = "STUDENT_LIST"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(Integer)
    address = Column(String)
    owner = Column(Integer, ForeignKey("teacherlist.id"))
