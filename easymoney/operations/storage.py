from easymoney.db import db_session
from easymoney.models import Operation


class OperationsStorage:
    def get_all(self) -> list[Operation]:
        return Operation.query.all()

    def get_by_uid(self, user_id: int, uid: int) -> Operation:
        query = Operation.query.filter(Operation.user_id == user_id)
        query = query.filter(Operation.uid == uid)
        return query.first()

    def add(self, category: str, amount: int, user_id: int, type_income_expenses: str) -> Operation:
        new_operation = Operation(name=category, amount=amount, user_id=user_id, type_income_expenses=type_income_expenses)
        db_session.add(new_operation)
        db_session.commit()
        return new_operation

    def update(self, user_id: int, uid: int, category: str, amount: int, type_income_expenses: str) -> Operation:
        query = Operation.query.filter(Operation.user_id == user_id)
        query = query.filter(Operation.uid == uid)
        operation = query.first()
        operation.category = category
        operation.amount = amount
        operation.type_income_expenses = type_income_expenses
        db_session.commit()
        return operation

    def delete(self, uid: int) -> bool:
        operation = Operation.query.filter(Operation.uid == uid).first()
        if not operation:
            return False
        db_session.delete(operation)
        db_session.commit()
        return True

    def get_for_user(self, user_id: int) -> list[Operation]:
        return Operation.query.filter(Operation.user_id == user_id)
