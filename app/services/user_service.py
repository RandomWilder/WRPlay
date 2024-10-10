from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def create_user(username, password, is_admin=False, initial_balance=0.0):
        user = User(username=username, is_admin=is_admin, balance=initial_balance)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def update_user_balance(user_id, amount):
        user = User.query.get(user_id)
        if user:
            user.balance += amount
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_user_balance(user_id):
        user = User.query.get(user_id)
        return user.balance if user else None

    @staticmethod
    def deduct_user_balance(user_id, amount):
        user = User.query.get(user_id)
        if user and user.balance >= amount:
            user.balance -= amount
            db.session.commit()
            return True
        return False

    @staticmethod
    def change_password(user_id, new_password):
        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_users():
        return User.query.all()