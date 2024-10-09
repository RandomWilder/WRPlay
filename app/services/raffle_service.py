from app import db
from app.models.raffle import Raffle
from app.models.ticket import Ticket
from datetime import datetime

class RaffleService:
    @staticmethod
    def create_raffle(name, total_tickets, ticket_price, draw_date):
        new_raffle = Raffle(name=name, total_tickets=total_tickets, ticket_price=ticket_price, draw_date=draw_date)
        db.session.add(new_raffle)
        db.session.commit()
        return new_raffle

    @staticmethod
    def get_active_raffles():
        return Raffle.query.filter_by(is_active=True).all()

    @staticmethod
    def conduct_raffle_draw(raffle_id):
        raffle = Raffle.query.get(raffle_id)
        if not raffle or not raffle.is_active:
            return None

        winning_ticket = Ticket.query.filter_by(raffle_id=raffle_id).order_by(db.func.random()).first()
        if winning_ticket:
            winning_ticket.is_winner = True
            raffle.is_active = False
            db.session.commit()

        return winning_ticket