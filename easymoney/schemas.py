from datetime import date

from pydantic import BaseModel


class Operation(BaseModel):
    uid: int
    name: str
    amount: int
    day: date
    type_income_expenses: str

    class Config:
        orm_mode = True


class User(BaseModel):
    uid: int
    name: str
    email: str | None
    tg_id: str

    class Config:
        orm_mode = True
