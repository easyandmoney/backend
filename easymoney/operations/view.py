from flask import Blueprint, request

from easymoney.errors import BadRequestError
from easymoney.operations.storage import OperationsStorage
from easymoney.schemas import Operation
from datetime import date

user_operations_view = Blueprint('user_operations', __name__)

storage = OperationsStorage()


@user_operations_view.post('/')
def add(user_id: int):
    try:
        payload = request.json
    except BadRequestError as badrequest_err:
        return badrequest_err

    if not payload:
        raise BadRequestError('Empty user data!')

    payload['uid'] = -1
    operation = Operation(**payload)

    new_operation = storage.add(
        category=operation.name,
        amount=operation.amount,
        user_id=user_id,
        type_income_expenses=operation.type_income_expenses,
    )

    operation = Operation.from_orm(new_operation)
    return operation.dict(), 201


@user_operations_view.get('/')
def get_all(user_id: int):
    user_operations = storage.get_for_user(user_id)
    return [Operation.from_orm(operation).dict() for operation in user_operations]


@user_operations_view.get('/<int:uid>')
def get_by_uid(user_id: int, uid: int):
    entity = storage.get_by_uid(user_id=user_id, uid=uid)
    operation = Operation.from_orm(entity)
    return operation.dict()


@user_operations_view.get('/<date:day>')
def get_by_date(user_id: int, day: date):
    entity = storage.get_by_date(user_id=user_id, day=day)
    operation = Operation.from_orm(entity)
    return operation.dict()


@user_operations_view.put('/<int:uid>')
def update(user_id: int, uid: int):
    try:
        payload = request.json
    except BadRequestError as badrequest_err:
        return badrequest_err

    if not payload:
        raise BadRequestError('Empty payload!')

    payload['uid'] = -1
    operation = Operation(**payload)

    update_operation = storage.update(
        user_id=user_id,
        uid=uid,
        category=operation.name,
        amount=operation.amount,
        type_income_expenses=operation.type_income_expenses,
    )

    operation = Operation.from_orm(update_operation)
    return operation.dict(), 200


@user_operations_view.delete('/<int:uid>')
def delete(user_id: int, uid: int):
    storage.delete(user_id=user_id, uid=uid)
    return {}, 404
