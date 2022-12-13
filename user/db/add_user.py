from db import db_session
from models import User

user = User(name = "p", email = "ur@gmail.com")
db_session.add(user)
db_session.commit()
