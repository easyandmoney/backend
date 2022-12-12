from flask import Flask, request
#нененирует случайные id уникальные, всегда разные
from uuid import uuid4

app = Flask(__name__)

storage = []

@app.route('/')
def hello():
    return "Hello world"

@app.get('/api/v1/users/')
def get_all():
    return storage

@app.post('/api/v1/users/')
def add():
    #hex преобразование в строчку
    uid = uuid4().hex
    user = request.json
    #добавляем новый ключ в словарь
    user["uid"] = uid
    storage.append(user)
    return user, 201



def main():
    app.run()



if __name__ == "__main__":
    main()

