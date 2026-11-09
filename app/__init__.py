import click
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please sign in to continue."
login_manager.session_protection = "strong"

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if len(app.config.get("SECRET_KEY") or "") < 32:
        raise RuntimeError("Configure SECRET_KEY with at least 32 random characters")
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.models import User
    from app.routes.auth import bp as auth_blueprint
    from app.routes.dashboard import bp as dashboard_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dashboard_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError):
            return None

    @app.get("/")
    def index():
        return redirect(url_for("dashboard.index"))

    @app.after_request
    def security_headers(response):
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        click.echo("Database initialized.")

    @app.cli.command("create-user")
    @click.argument("username")
    @click.password_option()
    def create_user(username, password):
        username = username.strip()
        if not username or len(username) > 50 or not 12 <= len(password) <= 256:
            raise click.ClickException("Use a username of 1–50 chars and a password of 12–256 chars")
        if User.query.filter_by(username=username).first():
            raise click.ClickException("Username already exists")
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo("User created.")

    return app
