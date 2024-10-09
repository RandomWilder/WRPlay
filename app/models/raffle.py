from app import db
from datetime import datetime

class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    draw_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)