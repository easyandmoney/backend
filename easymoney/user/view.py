from flask import Blueprint, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from easymoney.schemas import User
from easymoney.user.storage import UsersStorage

users_view = Blueprint('users', __name__)
users_storage = UsersStorage()


@users_view.get('/')
def get_all():
    users = users_storage.get_all()
    all_users = []
    for user in users:
        all_users.append({
            'uid': user.uid,
            'tg_id': user.tg_id,
            'name': user.name,
            'email': user.email,
        })
    return all_users


@users_view.get('/<string:uid>')
def get_by_id(uid: int):
    entity = users_storage.get_by_uid(uid)
    user = User.from_orm(entity)
    return user.dict()


@users_view.post('/')
def add():
    payload = request.json
    if not payload:
        return {'message', 'Empty payload'}, 400

    try:
        payload['uid'] = -1
        user = User(**payload)
    except ValidationError as err:
        return {'message': str(err)}, 400

    try:
        new_user = users_storage.add(name=user.name, email=user.email)
    except IntegrityError as error:
        return {'message': str(error)}, 409

    user = User.from_orm(new_user)
    return user.dict(), 201


@users_view.put('/<string:uid>')
def update(uid: int):
    payload = request.json
    if not payload:
        return {'message': 'Empty payload'}, 400
    try:
        payload['uid'] = -1
        user = User(**payload)
    except ValidationError as err:
        return {'message': str(err)}, 400

    update_user = users_storage.update(
        uid=uid,
        tg_id=user.tg_id,
        name=user.name,
        email=user.email,
    )
    user = User.from_orm(update_user)
    return user.dict(), 201


@users_view.delete('/<string:uid>')
def delete(uid: int):
    if not users_storage.delete(uid):
        return {}, 404
    return {}, 204
