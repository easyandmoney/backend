from db import db_session
from models import Operation

operation = Operation.query.first()
operation.amount = 5000
db_session.commit()
