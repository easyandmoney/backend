from flask import Blueprint, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from easymoney.operations.storage import OperationsStorage
from easymoney.schemas import Operation

user_operations_view = Blueprint('user_operations', __name__)

storage = OperationsStorage()


@user_operations_view.post('/')
def add(user_id: int):
    payload = request.json
    if not payload:
        return {'message': 'Empty payload'}, 400

    try:
        payload['uid'] = -1
        operation = Operation(**payload)
    except ValidationError as err:
        return {'message': str(err)}, 400

    try:
        new_operation = storage.add(
            category=operation.name,
            amount=operation.amount,
            user_id=user_id,
            type_income_expenses=operation.type_income_expenses,
        )
    except IntegrityError as conflict_err:
        return {'message': str(conflict_err)}, 409

    operation = Operation.from_orm(new_operation)
    return operation.dict(), 201


@user_operations_view.get('/')
def get_all(user_id: int):
    user_operations = storage.get_for_user(user_id)
    return [Operation.from_orm(operation).dict() for operation in user_operations]


@user_operations_view.get('/<string:uid>')
def get_by_uid(user_id: int, uid: int):
    entity = storage.get_by_uid(user_id=user_id, uid=uid)
    operation = Operation.from_orm(entity)
    return operation.dict()


@user_operations_view.put('/<string:uid>')
def update(user_id: int, uid: int):
    payload = request.json
    if not payload:
        return {'message': 'Empty payload'}, 400

    try:
        payload = request.json
        payload['uid'] = -1
        operation = Operation(**payload)
    except ValidationError as err:
        return {'message': str(err)}, 400

    try:
        update_operation = storage.update(
            user_id=user_id,
            uid=uid,
            category=operation.name,
            amount=operation.amount,
            type_income_expenses=operation.type_income_expenses
        )
    except IntegrityError as conflict_err:
        return {'message': str(conflict_err)}, 409

    operation = Operation.from_orm(update_operation)
    return operation.dict(), 200
