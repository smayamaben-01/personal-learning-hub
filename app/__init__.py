from flask import Flask
import config

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    from app.auth.routes import auth_bp
    from app.pages.routes import pages_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)

    return app