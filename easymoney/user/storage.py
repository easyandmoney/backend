from easymoney.db import db_session
from easymoney.errors import NotFoundError
from easymoney.models import User


class UsersStorage:
    def __init__(self):
        self.storage: dict[str, User] = {}

    def get_all(self) -> list[User]:
        return User.query.all()

    def get_by_uid(self, uid: int) -> User:
        return User.query.filter(User.uid == uid).first()

    def get_by_tg_id(self, tg_id: str) -> User:
        user = User.query.filter(User.tg_id == tg_id).first()
        if not user:
            raise NotFoundError('user.tg_id', tg_id)
        return user

    def add(self, name: str, email: str, tg_id: str) -> User:
        new_user = User(name=name, email=email, tg_id=tg_id)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    def update(self, uid: int, tg_id: str, name: str, email: str) -> User:
        user = User.query.filter(User.uid == uid).first()
        user.name = name
        user.email = email
        user.tg_id = tg_id
        db_session.commit()
        return user

    def delete(self, uid: int) -> bool:
        user = User.query.filter(User.uid == uid).first()
        if not user:
            return False
        db_session.delete(user)
        db_session.commit()
        return True
