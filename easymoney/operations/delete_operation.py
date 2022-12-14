from db import db_session
from models import Operation

operation = Operation.query.first()
db_session.delete(operation)
db_session.commit()
