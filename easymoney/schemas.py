from pydantic import BaseModel


class Operation(BaseModel):
    uid: int
    name: str
    amount: int

    class Config:
        orm_mode = True


class User(BaseModel):
    uid: int
    name: str
    email: str

    class Config:
        orm_mode = True
