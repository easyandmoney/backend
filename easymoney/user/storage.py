from dataclasses import dataclass
from uuid import uuid4


@dataclass
class User:
    uid: str
    name: str
    email: str


class UsersStorage:
    def __init__(self):
        self.storage: dict[str, User] = {}


    def get_all(self):
        return list(self.storage.values())


    def get_by_uid(self, uid):
        return self.storage[uid]

    def add(self, name, email):
        uid = uuid4().hex
        new_user = User(uid=uid, name=name, email=email)
        self.storage[new_user.uid] = new_user
        return self.storage[new_user.uid]


    def update(self, uid, name, email):
        update_user = self.storage[uid]
        update_user.name = name
        update_user.email = email
        return update_user


    def delete(self, uid):
        del self.storage[uid]
        return {}, 204
