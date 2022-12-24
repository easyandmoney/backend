from flask import Flask

from easymoney.operations.cloperations import user_operations_view
from easymoney.user.view import users_view


def main():
    app = Flask(__name__)
    app.register_blueprint(users_view, url_prefix='/api/v1/users')
    app.register_blueprint(
        user_operations_view,
        url_prefix='/api/v1/users/<int:user_id>/operations',
    )
    app.run()


if __name__ == '__main__':
    main()
