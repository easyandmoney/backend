from dataclasses import asdict
from flask import request, Blueprint
from easymoney.operations.storage import OperationsStorage

operations_view = Blueprint('operations', __name__)

operations_storage = OperationsStorage()

@operations_view.get('/')
def get_all():
    operations = operations_storage.get_all()
    return [{'uid': operation.id, 'category': operation.name, 'amount': operation.amount} for operation in operations]

@operations_view.get('/<string:uid>')
def get_by_uid(uid: str):
    operation = operations_storage.get_by_uid(uid)
    return {'uid': operation.id, 'category': operation.name, 'amount': operation.amount}

@operations_view.post('/')
def add():
    operation_category = request.json["category"]
    operation_amount = request.json["amount"]
    operation = operations_storage.add(category=operation_category, amount=operation_amount)
    return {'uid': operation.id, 'category': operation.name, 'amount': operation.amount}, 201

@operations_view.put('/<string:uid>')
def update(uid: str):
    operation_category = request.json["category"]
    operation_amount = request.json["amount"]
    update_operation = operations_storage.update(uid=uid, category=operation_category, amount=operation_amount)
    return {'uid': update_operation.id, 'category': update_operation.name, 'amount': update_operation.amount}, 200

@operations_view.delete('/<string:uid>')
def delete(uid):
    if not operations_storage.delete(uid):
        return {}, 404
    return {}, 204
