from models import Operation

operation = Operation.query.first()
print(f"""Название: {operation.name}
Сумма: {operation.amount}
""")
