from easymoney.db import db_session
from easymoney.models import Operation


class OperationsStorage:
    def get_all(self) -> list[Operation]:
        return Operation.query.all()

    def get_by_uid(self, uid: int) -> Operation:
        return Operation.query.filter(Operation.uid == uid).first()

    def add(self, category: str, amount: int) -> Operation:
        new_operation = Operation(name=category, amount=amount)
        db_session.add(new_operation)
        db_session.commit()
        return new_operation

    def update(self, uid: int, category: str, amount: int) -> Operation:
        operation = Operation.query.filter(Operation.uid == uid).first()
        operation.category = category
        operation.amount = amount
        db_session.commit()
        return operation

    def delete(self, uid: int) -> bool:
        operation = Operation.query.filter(Operation.uid == uid).first()
        if not operation:
            return False
        db_session.delete(operation)
        db_session.commit()
        return True
