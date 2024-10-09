from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
admin_manager = Admin(template_mode='bootstrap3')  # Renamed from 'admin' to 'admin_manager'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    admin_manager.init_app(app)  # Use the new name here

    from app.models import User
    from app.routes import main, auth, raffle, admin as admin_routes
    from app.admin import views as admin_views

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(raffle.bp)
    app.register_blueprint(admin_routes.bp)

    admin_views.init_admin_views(admin_manager)  # Pass the renamed admin_manager here

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app