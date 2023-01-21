from datetime import datetime

from sqlalchemy import func, desc
from sqlalchemy.exc import IntegrityError

from easymoney.db import db_session
from easymoney.errors import ConflictError, NotFoundError
from easymoney.models import Operation


class OperationsStorage:
    def get_all(self) -> list[Operation]:
        return Operation.query.all()

    def get_by_date(self, user_id: int, payment_date: datetime) -> list[Operation]:
        query = Operation.query.filter(Operation.user_id == user_id)
        return query.filter(Operation.payment_date > payment_date).all()

    def get_by_uid(self, user_id: int, uid: int) -> Operation:
        query = Operation.query.filter(Operation.user_id == user_id)
        operation = query.filter(Operation.uid == uid).first()
        if not operation:
            raise NotFoundError('operations', uid)
        return operation

    def get_total(self, user_id: int, payment_date: datetime | None) -> int:
        query = db_session.query(func.sum(Operation.amount))
        query = query.filter(Operation.user_id == user_id)
        if payment_date:
            query = query.filter(Operation.payment_date > payment_date)
        return query.scalar()

    def get_total_per_cat(
        self,
        user_id: int,
        payment_date: datetime | None,
    ) -> list[tuple[str, int]]:
        query = db_session.query(Operation.category, func.sum(Operation.amount))
        query = query.group_by(Operation.category)
        query = query.filter(Operation.user_id == user_id)
        if payment_date:
            query = query.filter(Operation.payment_date > payment_date)
        categories = query.all()
        return [(category[0], category[1]) for category in categories]

    def add(
        self,
        category: str,
        amount: int,
        user_id: int,
        type_income_expenses: str,
        payment_date: datetime,
    ) -> Operation:
        new_operation = Operation(
            category=category,
            amount=amount,
            user_id=user_id,
            type_income_expenses=type_income_expenses,
            payment_date=payment_date,
        )
        db_session.add(new_operation)

        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('operations', new_operation.uid)

        return new_operation

    def update(
        self,
        user_id: int,
        uid: int,
        category: str,
        amount: int,
        type_income_expenses: str,
        payment_date: datetime,
    ) -> Operation:
        query = Operation.query.filter(Operation.user_id == user_id)
        query = query.filter(Operation.uid == uid)
        operation = query.first()

        if not operation:
            raise NotFoundError('operations', uid)

        operation.category = category
        operation.amount = amount
        operation.type_income_expenses = type_income_expenses
        operation.payment_date = payment_date

        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('operations', uid)

        return operation

    def delete(self, user_id: int, uid: int) -> bool:
        query = Operation.query.filter(Operation.user_id == user_id)
        query = query.filter(Operation.uid == uid)
        operation = query.first()
        if not operation:
            raise NotFoundError('operations', uid)
        db_session.delete(operation)
        db_session.commit()
        return True

    def delete_last_operation(self, user_id: int) -> bool:
        query = Operation.query.filter(Operation.user_id == user_id)
        operation = query.order_by(desc(Operation.uid)).first()
        db_session.delete(operation)
        db_session.commit()
        return True

    def get_for_user(self, user_id: int) -> list[Operation]:
        return Operation.query.filter(Operation.user_id == user_id)
