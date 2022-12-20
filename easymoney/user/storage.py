from easymoney.db import db_session
from easymoney.models import User

class UsersStorage:
    def __init__(self):
        self.storage: dict[str, User] = {}

    def get_all(self):
        users = User.query.all()
        return users

    def get_by_uid(self, uid):
        user = User.query.filter(User.uid == uid).first()
        return user

    def add(self, name, email):
        new_user = User(name=name, email=email)
        db_session.add(new_user)
        db_session.commit()
        return new_user


    def update(self, uid, name, email):
        user = User.query.filter(User.uid == uid).first()
        user.name = name
        user.email = email
        db_session.commit()
        return user


    def delete(self, uid: int) -> bool:
        user = User.query.filter(User.uid == uid).first()
        if not user:
            return False
        db_session.delete(user)
        db_session.commit()
        return True
