from sqlalchemy import Column, Integer, String, ForeignKey
from easymoney.db import Base, engine
from sqlalchemy.orm import relationship

class Operation(Base):
    __tablename__ = 'operations'
    uid = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False)

    user = relationship("User", back_populates="operations")

    def __repr__(self):
        return f'<Operation {self.name} {self.amount}>'



class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String(120), unique=True)

    operations = relationship("Operation", back_populates="user")

    def __repr__(self):
        return f'<User {self.name} {self.email}>'



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
