import logging
from datetime import datetime, timedelta

from flask import Blueprint

from easymoney.operations.storage import OperationsStorage

logger = logging.getLogger(__name__)
user_total_view = Blueprint('user_total', __name__)

storage = OperationsStorage()


@user_total_view.get('')
def get_total(user_id: int):
    return get_total_by_date(user_id, payment_date=None)


@user_total_view.get('/year')
def get_total_year(user_id: int):
    payment_date = datetime.today() - timedelta(days=365)
    return get_total_by_date(user_id, payment_date)


@user_total_view.get('/month')
def get_total_month(user_id: int):
    payment_date = datetime.today() - timedelta(days=30)
    return get_total_by_date(user_id, payment_date)


@user_total_view.get('/today')
def get_total_today(user_id: int):
    payment_date = datetime.today() - timedelta(hours=24)
    return get_total_by_date(user_id, payment_date)


def get_total_by_date(user_id: int, payment_date: datetime | None):
    total = storage.get_total(user_id=user_id, payment_date=payment_date)
    total_categories = storage.get_total_per_cat(user_id=user_id, payment_date=payment_date)
    categories = {category: cat_total for category, cat_total in total_categories}
    return {'total': total or 0, 'categories': categories}
