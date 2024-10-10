import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from config import Config
from flask.cli import with_appcontext
import click

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
admin_manager = Admin(template_mode='bootstrap3')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    admin_manager.init_app(app)

    from app.models import User
    from app.routes import main, auth, raffle
    from app.routes.admin import admin_bp as custom_admin_bp
    from app.admin import views as admin_views

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(raffle.bp)
    app.register_blueprint(custom_admin_bp)

    admin_views.init_admin_views(admin_manager)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.cli.command("reset-db")
    @with_appcontext
    def reset_db_command():
        """Reset the database."""
        from app.db_utils import reset_database
        reset_database()
        click.echo('Database has been reset.')

    return app