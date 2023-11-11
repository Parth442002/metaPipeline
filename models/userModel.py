from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base
from connectors.dbConnector import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
