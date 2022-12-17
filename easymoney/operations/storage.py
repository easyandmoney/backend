from easymoney.models import Operation
from easymoney.db import db_session

class OperationsStorage:
    def __init__(self):
        self.storage: dict[str, Operation] = {}

    def get_all(self):
        operations = Operation.query.all()
        return operations

    def get_by_uid(self, uid):
        operation = Operation.query.filter(Operation.uid == uid).first()
        return operation

    def add(self, category, amount):
        new_operation = Operation(name=category, amount=amount)
        db_session.add(new_operation)
        db_session.commit()
        return new_operation

    def update(self, uid, category, amount):
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
