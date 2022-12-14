from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Operation:
    uid: str
    category: str
    amount: int


class OperationsStorage:
    def __init__(self):
        self.storage: dict[str, Operation] = {}


    def get_all(self):
        return list(self.storage.values())


    def get_by_uid(self, uid):
        return self.storage[uid]

    def add(self, category, amount):
        uid = uuid4().hex
        new_operation = Operation(uid=uid, category=category, amount=amount)
        self.storage[new_operation.uid] = new_operation
        return self.storage[new_operation.uid]


    def update(self, uid, category, amount):
        update_operation = self.storage[uid]
        update_operation.category = category
        update_operation.amount = amount
        return update_operation


    def delete(self, uid):
        del self.storage[uid]
        return {}, 204
