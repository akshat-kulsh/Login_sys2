from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:akshat0509@localhost/login_sys"
Base = declarative_base()
engine = create_engine(DB_URL, pool_recycle=3600,
                       connect_args={'connect_timeout': 60})


session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'user_table'
    idusers = Column(Integer,primary_key=True)
    username = Column(String(30))
    email = Column(String(30))
    pssword = Column(String(100))
    p_id = Column(Integer)

class adUnit(Base):
    __tablename__ = 'ad_Unit'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey(User.idusers))
    page_name = Column(String(30))
    adUnitSize = Column(String(40))
    adLink = Column(String(100))