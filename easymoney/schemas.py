from datetime import datetime

from pydantic import BaseModel


class Operation(BaseModel):
    uid: int
    amount: int
    payment_date: datetime
    type_income_expenses: str
    category: str

    class Config:
        orm_mode = True


class User(BaseModel):
    uid: int
    name: str
    email: str | None
    tg_id: str

    class Config:
        orm_mode = True
