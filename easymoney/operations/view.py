from flask import Blueprint, request
from pydantic import ValidationError

from easymoney.operations.storage import OperationsStorage
from easymoney.schemas import Operation

operations_view = Blueprint('operations', __name__)
operations_storage = OperationsStorage()


@operations_view.get('/')
def get_all():
    operations = operations_storage.get_all()
    all_operations = []
    for operation in operations:
        all_operations.append({
            'uid': operation.uid,
            'category': operation.name,
            'amount': operation.amount,
        })
    return all_operations


@operations_view.get('/<string:uid>')
def get_by_uid(uid: int):
    entity = operations_storage.get_by_uid(uid)
    operation = Operation.from_orm(entity)
    return operation.dict()


@operations_view.post('/')
def add():
    payload = request.json
    if not payload:
        return {'message': 'Empty payload'}, 400
    try:
        payload['uid'] = -1
        operation = Operation(**payload)
    except ValidationError as err:
        return {'message': str(err)}, 400
    new_operation = operations_storage.add(category=operation.name, amount=operation.amount)
    operation = Operation.from_orm(new_operation)
    return operation.dict(), 201


@operations_view.put('/<string:uid>')
def update(uid: int):
    payload = request.json
    if not payload:
        return {'message': 'Empty payload'}, 400
    try:
        payload = request.json
        payload['uid'] = -1
        operation = Operation(**payload)
    except ValidationError as err:
        return {'message': str(err)}, 400
    update_operation = operations_storage.update(
        uid=uid,
        category=operation.name,
        amount=operation.amount,
    )
    operation = Operation.from_orm(update_operation)
    return operation.dict(), 200


@operations_view.delete('/<string:uid>')
def delete(uid: int):
    if not operations_storage.delete(uid):
        return {}, 404
    return {}, 204
