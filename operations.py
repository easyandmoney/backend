from dataclasses import asdict
from flask import Flask, request
from operationsclass import OperationsStorage


app = Flask(__name__)

operations_storage = OperationsStorage()

@app.get('/api/v1/operations/')
def get_all():
    operations = operations_storage.get_all()
    return [asdict(operation) for operation in operations]


@app.get('/api/v1/operations/<string:uid>')
def get_by_uid(uid: str):
    return asdict(operations_storage.get_by_uid(uid))



@app.post('/api/v1/operations/')
def add():
    operation = request.json
    operation_category = request.json["category"]
    operation_amount = request.json["amount"]
    operations_storage.add(category=operation_category, amount=operation_amount)
    return operation, 201


@app.put('/api/v1/operations/<string:uid>')
def update(uid: str):
    operation_category = request.json["category"]
    operation_amount = request.json["amount"]
    update_operation = operations_storage.update(uid=uid, category=operation_category, amount=operation_amount)
    return asdict(update_operation), 201



@app.delete('/api/v1/operations/<string:uid>')
def delete(uid):
    if operations_storage.delete(uid):
        return {}, 204



def main():
    app.run()

if __name__ == '__main__':
    main()
