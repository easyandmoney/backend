from db import db_session
from models import Operation

operation = Operation(name='Income', amount=100)
db_session.add(operation)
db_session.commit()
