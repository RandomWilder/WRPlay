from app.models.base import Base, db
from datetime import datetime

class Ticket(Base):
    __tablename__ = 'tickets'

    raffle_id = db.Column(db.Integer, db.ForeignKey('raffles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ticket_number = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_winner = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('tickets', lazy='dynamic'))
    raffle = db.relationship('Raffle', back_populates='tickets')

    def __repr__(self):
        return f'<Ticket {self.ticket_number} for Raffle {self.raffle_id}>'