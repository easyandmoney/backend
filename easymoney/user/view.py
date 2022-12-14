from flask import request,Blueprint
from uuid import uuid4


users_view = Blueprint('users', __name__)

storage = {}

@users_view.get('/')
def get_all():
    return list(storage.values())

@users_view.get('/<string:uid>')
def get_by_id(uid: str):
    return storage[uid]

@users_view.post('/')
def add():
    uid = uuid4().hex
    user = request.json
    user["uid"] = uid
    storage[uid] = user
    return user, 201

@users_view.put('/<string:uid>')
def update(uid: str):
    new_user = request.json
    new_user['uid'] = uid
    storage[uid] = new_user
    return storage[uid]

@users_view.delete('/<string:uid>')
def delete(uid: str):
    storage.pop(uid)
    return {}, 204


