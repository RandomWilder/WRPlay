from app import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raffle_id = db.Column(db.Integer, db.ForeignKey('raffle.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_winner = db.Column(db.Boolean, default=False)

    raffle = db.relationship('Raffle', backref=db.backref('tickets', lazy=True))
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))