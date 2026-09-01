from flask import Flask, jsonify
import config

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    from app.auth.routes import auth_bp
    from app.pages.routes import pages_bp
    from app.api.dsa import api_dsa_bp
    from app.api.companies import api_company_bp
    from app.api.notes import api_note_bp
    from app.api.dashboard import api_dashboard_bp
    from app.api.search import api_search_bp
    from app.api.profile import api_profile_bp
    from app.api.password import api_password_bp
    from app.api.goals import api_goals_bp

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.exception(e)
        return jsonify({"success": False, "error": "An unexpected error occurred"}), 500

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_dsa_bp)
    app.register_blueprint(api_company_bp)
    app.register_blueprint(api_note_bp)
    app.register_blueprint(api_dashboard_bp)
    app.register_blueprint(api_search_bp)
    app.register_blueprint(api_profile_bp)
    app.register_blueprint(api_password_bp)
    app.register_blueprint(api_goals_bp)

    return app