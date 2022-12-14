from flask import Flask
from easymoney.operations.view import operations_view

def main():
    app = Flask(__name__)
    app.register_blueprint(operations_view, url_prefix='/api/v1/operations')
    app.run()

if __name__ == "__main__":
    main()
