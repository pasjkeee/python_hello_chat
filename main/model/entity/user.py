from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, DateTime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(String(36), primary_key=True, comment='Уникальный идентификатор записи')
    login = Column(String(255), unique=True, comment='Логин пользователя')
    age = Column(Integer(), nullable=False)
    gender = Column(String(20), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
