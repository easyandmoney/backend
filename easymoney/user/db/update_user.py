from db import db_session
from models import User

user = User.query.first()
user.name = "Peter"
db_session.commit()
