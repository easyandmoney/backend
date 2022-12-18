from dataclasses import asdict
from flask import request, Blueprint
from easymoney.operations.storage import OperationsStorage
from easymoney.schemas import Operation
from pydantic import ValidationError

operations_view = Blueprint('operations', __name__)

operations_storage = OperationsStorage()

@operations_view.get('/')
def get_all():
    operations = operations_storage.get_all()
    return [{'uid': operation.uid, 'category': operation.name, 'amount': operation.amount} for operation in operations]

@operations_view.get('/<string:uid>')
def get_by_uid(uid: str):
    operation = operations_storage.get_by_uid(uid)
    return {'uid': operation.uid, 'category': operation.name, 'amount': operation.amount}

@operations_view.post('/')
def add():
    try:
        payload = request.json
        payload['uid'] = -1
        operation = Operation(**payload)
    except ValidationError as err:
        return {'message': str(err)}, 400
    new_operation = operations_storage.add(category=operation.name, amount=operation.amount)
    operation = Operation.from_orm(new_operation)
    return operation.dict(), 201

@operations_view.put('/<string:uid>')
def update(uid: str):
    operation_category = request.json["category"]
    operation_amount = request.json["amount"]
    update_operation = operations_storage.update(uid=uid, category=operation_category, amount=operation_amount)
    return {'uid': update_operation.uid, 'category': update_operation.name, 'amount': update_operation.amount}, 200

@operations_view.delete('/<string:uid>')
def delete(uid):
    if not operations_storage.delete(uid):
        return {}, 404
    return {}, 204
