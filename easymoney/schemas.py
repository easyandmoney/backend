from pydantic import BaseModel


class Operation(BaseModel):
    uid: int
    name: str
    amount: int

    class Config:
        orm_mode=True



