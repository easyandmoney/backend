from flask import request,Blueprint
from dataclasses import asdict
from easymoney.user.storage import UsersStorage


users_view = Blueprint('users', __name__)

users_storage = UsersStorage()

@users_view.get('/')
def get_all():
    users = users_storage.get_all()
    return [{"uid": user.uid, "name": user.name, "email": user.email} for user in users]

@users_view.get('/<string:uid>')
def get_by_id(uid: str):
    user = users_storage.get_by_uid(uid)
    return {"uid": user.uid, "name": user.name, "email": user.email}

@users_view.post('/')
def add():
    user_name = request.json["name"]
    user_email = request.json["email"]
    user = users_storage.add(name=user_name, email=user_email)
    return {"uid": user.uid, "name": user.name, "email": user.email}, 201

@users_view.put('/<string:uid>')
def update(uid: str):
    user_name = request.json["name"]
    user_email = request.json["email"]
    update_user = users_storage.update(uid=uid, name=user_name, email=user_email)
    return {"uid": update_user.uid, "name": update_user.name, "email": update_user.email}, 200

@users_view.delete('/<string:uid>')
def delete(uid):
    if not users_storage.delete(uid):
        return {}, 404
    return {}, 204


