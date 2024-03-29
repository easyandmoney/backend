import logging
from datetime import datetime, timedelta

import orjson
from flask import Blueprint, request

from easymoney.errors import BadRequestError
from easymoney.operations.storage import OperationsStorage
from easymoney.operations.total import user_total_view
from easymoney.schemas import Operation

logger = logging.getLogger(__name__)
user_operations_view = Blueprint('user_operations', __name__)
user_operations_view.register_blueprint(
    user_total_view,
    url_prefix='/total',
)
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
        category=operation.category,
        amount=operation.amount,
        user_id=user_id,
        type_income_expenses=operation.type_income_expenses,
        payment_date=operation.payment_date,
    )

    operation = Operation.from_orm(new_operation)
    return operation.json(), 201


@user_operations_view.get('/')
def get_all(user_id: int):
    user_operations = storage.get_for_user(user_id)
    return orjson.dumps([Operation.from_orm(operation).dict() for operation in user_operations])


@user_operations_view.get('/<int:uid>')
def get_by_uid(user_id: int, uid: int):
    entity = storage.get_by_uid(user_id=user_id, uid=uid)
    operation = Operation.from_orm(entity)
    return operation.dict()


@user_operations_view.delete('/last')
def delete_last_operation(user_id: int):
    storage.delete_last_operation(user_id=user_id)
    return {}, 204


@user_operations_view.get('/today')
def get_today_operations(user_id: int):
    payment_date = datetime.today() - timedelta(hours=24)

    entities = storage.get_by_date(user_id=user_id, payment_date=payment_date)
    return orjson.dumps([Operation.from_orm(operation).dict() for operation in entities])


@user_operations_view.get('/month')
def get_month_operations(user_id: int):
    payment_date = datetime.today() - timedelta(days=30)

    entities = storage.get_by_date(user_id=user_id, payment_date=payment_date)
    return orjson.dumps([Operation.from_orm(operation).dict() for operation in entities])


@user_operations_view.get('/year')
def get_year_operations(user_id: int):
    payment_date = datetime.today() - timedelta(days=365)

    entities = storage.get_by_date(user_id=user_id, payment_date=payment_date)
    return orjson.dumps([Operation.from_orm(operation).dict() for operation in entities])


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
        category=operation.category,
        amount=operation.amount,
        type_income_expenses=operation.type_income_expenses,
        payment_date=operation.payment_date,
    )

    operation = Operation.from_orm(update_operation)
    return operation.json(), 200


@user_operations_view.delete('/<int:uid>')
def delete(user_id: int, uid: int):
    storage.delete(user_id=user_id, uid=uid)
    return {}, 204
