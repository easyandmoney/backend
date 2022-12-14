from dataclasses import asdict
from flask import request, Blueprint
from easymoney.operations.storage import OperationsStorage

operations_view = Blueprint('operations', __name__)

operations_storage = OperationsStorage()

@operations_view.get('/')
def get_all():
    operations = operations_storage.get_all()
    return [asdict(operation) for operation in operations]


@operations_view.get('/<string:uid>')
def get_by_uid(uid: str):
    return asdict(operations_storage.get_by_uid(uid))


@operations_view.post('/')
def add():
    operation = request.json
    operation_category = request.json["category"]
    operation_amount = request.json["amount"]
    operations_storage.add(category=operation_category, amount=operation_amount)
    return operation, 201


@operations_view.put('/<string:uid>')
def update(uid: str):
    operation_category = request.json["category"]
    operation_amount = request.json["amount"]
    update_operation = operations_storage.update(uid=uid, category=operation_category, amount=operation_amount)
    return asdict(update_operation), 201



@operations_view.delete('/<string:uid>')
def delete(uid):
    if operations_storage.delete(uid):
        return {}, 204

