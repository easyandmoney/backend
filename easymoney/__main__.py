from flask import Flask
from pydantic import ValidationError

from easymoney.db import db_session
from easymoney.errors import AppError
from easymoney.operations.view import user_operations_view
from easymoney.user.view import users_view


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.code


def handle_validation_error(error: ValidationError):
    return {'message': str(error)}, 422


def handle_emptystring_error(error):
    return {'Empty data': str(error)}, 400


def main():
    app = Flask(__name__)
    app.register_blueprint(users_view, url_prefix='/api/v1/users')
    app.register_blueprint(
        user_operations_view,
        url_prefix='/api/v1/users/<int:user_id>/operations',
    )
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(400, handle_emptystring_error)  # noqa: WPS432

    app.teardown_appcontext(shutdown_session)

    app.run()


def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    main()
