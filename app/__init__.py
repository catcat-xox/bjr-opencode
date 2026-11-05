import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "lab_equipment.db"),
    )

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from app import database

    database.init_app(app)

    with app.app_context():
        database.init_db()

    from app.routes import register_error_handlers, register_routes

    register_routes(app)
    register_error_handlers(app)

    return app
