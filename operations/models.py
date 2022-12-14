from sqlalchemy import Column, Integer, String
from db import Base, engine

class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)

    def __repr__(self):
        return f'<Operation {self.name} {self.amount}>'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
