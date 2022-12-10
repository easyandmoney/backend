from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

storage = []



@app.route('/')
def hello():
    return 'Hello, World!'

@app.get('/api/v1/operations/')
def get_all():
    return storage

@app.get('/api/v1/operations/')
def get_by_id(uid):
    return

@app.post('/api/v1/operations/')
def add():
    uid = uuid4().hex
    operation = request.json
    operation['uid'] = uid
    storage.append(operation)
    return operation, 201


def main():
    app.run()

if __name__ == "__main__":
    main()
