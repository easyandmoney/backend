from flask import request
from uuid import uuid4
from flask import Blueprint

operations_view = Blueprint('operations', __name__)

storage = {}

@operations_view.get('/')
def get_all():
    return list(storage.values())

@operations_view.get('/<string:uid>')
def get_by_id(uid: str):
    return storage[uid]


@operations_view.post('/')
def add():
    uid = uuid4().hex
    operation = request.json
    operation['uid'] = uid
    storage[uid] = operation
    return operation, 201

@operations_view.put('/<string:uid>')
def update(uid: str):
    new_operation = request.json
    new_operation['uid'] = uid
    storage[uid] = new_operation
    return storage[uid]

@operations_view.delete('/<string:uid>')
def delete(uid: str):
    storage.pop(uid)
    return {}, 204
