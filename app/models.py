from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    draw_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raffle_id = db.Column(db.Integer, db.ForeignKey('raffle.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_winner = db.Column(db.Boolean, default=False)

    raffle = db.relationship('Raffle', backref=db.backref('tickets', lazy=True))
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))