from flask import Flask

from easymoney.operations.view import operations_view
from easymoney.user.view import users_view


def main():
    app = Flask(__name__)
    app.register_blueprint(operations_view, url_prefix='/api/v1/operations')
    app.register_blueprint(users_view, url_prefix='/api/v1/users')
    app.run()


if __name__ == '__main__':
    main()
