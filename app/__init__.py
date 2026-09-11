"""Flask application factory."""
from flask import Flask

from app.config import Config


def create_app(config_class=Config):
    """Create and configure the LCC Issue Tracker Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app import db
    from app.extensions import bcrypt

    db.init_db(
        app,
        app.config['DB_USER'],
        app.config['DB_PASSWORD'],
        app.config['DB_HOST'],
        app.config['DB_NAME'],
    )
    bcrypt.init_app(app)

    from app.blueprints.auth import auth_bp
    from app.blueprints.issues import issues_bp
    from app.blueprints.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(issues_bp)

    return app
