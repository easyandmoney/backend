from models import User

user = User.query.first()
print(f""" Name {user.name}
Email {user.email}""")
