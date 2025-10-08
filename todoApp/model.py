from database import base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index = True)
    email = Column(String, unique = True)
    username = Column(String, unique = True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)
    role = Column(String)



class Todos(base):
    __tablename__ = 'todos'

    ID = Column(Integer,  primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    Priority = Column(Integer)
    Complete = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey("users.id"))






