import os

from flask import Flask


def register_route(app):
    from .views import contents

    app.register_blueprint(contents.bp)


def create_app(test_config=None):
    app = Flask(__name__)
    register_route(app)
    return app
