from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

storage = {}

@app.route('/')
def hello():
    return "Hello world"

@app.get('/api/v1/users/')
def get_all():
    return list(storage.values())

@app.get('/api/v1/users/<string:uid>')
def get_by_id(uid: str):
    return storage[uid]

@app.post('/api/v1/users/')
def add():
    uid = uuid4().hex
    user = request.json
    user["uid"] = uid
    storage[uid] = user
    return user, 201




@app.put('/api/v1/users/<string:uid>')
def update(uid: str):
    new_user = request.json
    new_user['uid'] = uid
    storage[uid] = new_user
    return storage[uid]

@app.delete('/api/v1/users/<string:uid>')
def delete(uid: str):
    storage.pop(uid)
    return {}, 204

def main():
    app.run()



if __name__ == "__main__":
    main()

