from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import sql_user, sql_pwd, sql_server, sql_port, sql_db
from untils import hash256

engine = create_engine(
    "mysql+mysqlconnector://%s:%s@%s:%s/%s"
    % (sql_user, sql_pwd, sql_server, sql_port, sql_db)
)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    account = Column(String(20), primary_key=True)
    pwd = Column(String(255))
    role = Column(String(20))
    nickname = Column(String(20))
    avatar = Column(String(255))
    gamemode = Column(String(20))


# QueryUser
def QueryUser(account):
    session = DBSession()
    query_user = None
    try:
        query_user = session.query(User).filter(User.account == account).one()
        session.close()
    except:
        pass
    return query_user


# Register
def Register(account, pwd, nickname):
    session = DBSession()
    RegisterUser = User(
        account=account,
        pwd=hash256(pwd),
        role="user",
        nickname=nickname,
        avatar="defualt_avatar",
        gamemode="survival",
    )
    session.add(RegisterUser)
    session.commit()
    session.close()


# Login
def Login(account, pwd):
    session = DBSession()
    pwd = hash256(pwd)
    query_user = session.query(User).filter(User.account == account).one()
    session.close()
    if query_user.pwd == pwd:
        return {
            "account": query_user.account,
            "role": query_user.role,
            "nickname": query_user.nickname,
            "avatar": query_user.avatar,
            "gamemode": query_user.gamemode,
        }
    else:
        return False


# Rest Pwd
def RestPwd(account, pwd):
    session = DBSession()
    query_user = session.query(User).filter(User.account == account).one()
    query_user.pwd = hash256(pwd)
    session.commit()
    session.close()


# Update Avatar
def UpdateAvatar(account, avatar):
    session = DBSession()
    query_user = session.query(User).filter(User.account == account).one()
    query_user.avatar = avatar
    session.commit()
    session.close()


# Update Nickname
def UpdateNickname(account, nickname):
    session = DBSession()
    query_user = session.query(User).filter(User.account == account).one()
    query_user.nickname = nickname
    session.commit()
    session.close()


# Change Role
def ChangeRole(account, role):
    session = DBSession()
    query_user = session.query(User).filter(User.account == account).one()
    query_user.role = role
    session.commit()
    session.close()


# Change Gamemde
def ChangeGamemod(account, gamemode):
    session = DBSession()
    query_user = session.query(User).filter(User.account == account).one()
    query_user.gamemode = gamemode
    session.commit()
    session.close()


# Get Users (Using page and page size)
def GetUsers(page, pagesize):
    session = DBSession()
    query_user = session.query(User).offset((page - 1) * pagesize).limit(pagesize).all()
    session.close()
    result = []
    for single_user in query_user:
        result.append(
            {
                "account": single_user.account,
                "role": single_user.role,
                "nickname": single_user.nickname,
                "avatar": single_user.avatar,
                "gamemode": single_user.gamemode,
            }
        )
    return result


if __name__ == "__main__":
    GetUsers(1, 10)

