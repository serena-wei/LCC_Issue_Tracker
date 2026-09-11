"""Flask application factory."""
from flask import Flask


def create_app():
    """Create and configure the LCC Issue Tracker Flask app."""
    app = Flask(__name__)

    # Anyone with access to this key can pretend to be signed in as any user.
    app.secret_key = 'Example Secret Key (CHANGE THIS TO YOUR OWN SECRET KEY!)'

    from app import connect, db
    from app.extensions import bcrypt

    db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)
    bcrypt.init_app(app)

    from app.blueprints.auth import auth_bp
    from app.blueprints.issues import issues_bp
    from app.blueprints.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(issues_bp)

    return app
