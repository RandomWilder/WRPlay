from app.models.base import Base, db

class Raffle(Base):
    __tablename__ = 'raffles'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    ticket_price = db.Column(db.Float, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    draw_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    tickets = db.relationship('Ticket', back_populates='raffle')