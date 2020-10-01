from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import sql_user, sql_pwd, sql_server, sql_port, sql_db

engine = create_engine(
    "mysql+mysqlconnector://%s:%s@%s:%s/%s"
    % (sql_user, sql_pwd, sql_server, sql_port, sql_db)
)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class CUSTOMJS(Base):
    __tablename__ = "customjs"
    file_uid = Column(String(20), primary_key=True)
    enable = Column(Integer(1))
    file_location = Column(String(255))
    desc = Column(String(255))


def uploadinfo(file_location, desc):
    session = DBSession()
    NewUpload = CUSTOMJS(enable=0, file_location=file_location, desc=desc)
    session.add(NewUpload)
    session.commit()
    session.close()
