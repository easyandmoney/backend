from flask import request,Blueprint
from dataclasses import asdict
from easymoney.user.storage import UsersStorage


users_view = Blueprint('users', __name__)

users_storage = UsersStorage()

@users_view.get('/')
def get_all():
    users = users_storage.get_all()
    return [asdict(user) for user in users]

@users_view.get('/<string:uid>')
def get_by_id(uid: str):
    return asdict(users_storage.get_by_uid(uid))

@users_view.post('/')
def add():
    user = request.json
    user_name = request.json["name"]
    user_email = request.json["email"]
    users_storage.add(name=user_name, email=user_email)
    return user, 201

@users_view.put('/<string:uid>')
def update(uid: str):
    user_name = request.json["name"]
    user_email = request.json["email"]
    update_user = users_storage.update(uid=uid, name=user_name, email=user_email)
    return asdict(update_user)

@users_view.delete('/<string:uid>')
def delete(uid: str):
    if users_storage.delete(uid):
        return {}, 204


