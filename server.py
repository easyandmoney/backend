from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

storage = {}


@app.route('/')
def hello():
    return 'Hello, World!'

@app.get('/api/v1/operations/')
def get_all():
    return list(storage.values())

@app.get('/api/v1/operations/<string:uid>')
def get_by_id(uid: str):
    return storage[uid]


@app.post('/api/v1/operations/')
def add():
    uid = uuid4().hex
    operation = request.json
    operation['uid'] = uid
    storage[uid] = operation
    return operation, 201

@app.put('/api/v1/operations/<string:uid>')
def update(uid: str):
    new_operation = request.json
    new_operation['uid'] = uid
    storage[uid] = new_operation
    return storage[uid]

@app.delete('/api/v1/operations/<string:uid>')
def delete(uid: str):
    storage.pop(uid)
    return {}, 204


def main():
    app.run()

if __name__ == "__main__":
    main()
