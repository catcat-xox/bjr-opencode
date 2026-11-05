from flask import jsonify

from app.errors import AppError
from app.routes.item_routes import bp as item_bp
from app.routes.loan_routes import bp as loan_bp


def register_routes(app):
    """Register all API blueprints."""
    app.register_blueprint(item_bp)
    app.register_blueprint(loan_bp)


def register_error_handlers(app):
    """Return consistent JSON errors for domain and HTTP errors."""

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
