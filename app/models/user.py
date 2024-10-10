from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base, db

class User(UserMixin, Base):
    __tablename__ = 'users'

    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=0.0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_funds(self, amount):
        self.balance += amount
        db.session.commit()

    def deduct_funds(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            db.session.commit()
            return True
        return False