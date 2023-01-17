from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from easymoney.db import Base, engine


class Operation(Base):
    __tablename__ = 'operations'
    uid = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)
    type_income_expenses = Column(String)
    payment_date = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('users.uid'), nullable=False)
    user = relationship('User', back_populates='operations')
    category = Column(String)

    def __repr__(self):
        return f'<Operation {self.name} {self.amount}>'


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    tg_id = Column(String)
    name = Column(String)
    email = Column(String(120), unique=True)  # noqa: WPS432
    operations = relationship('Operation', back_populates='user')

    def __repr__(self):
        return f'<User {self.name} {self.email}>'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
